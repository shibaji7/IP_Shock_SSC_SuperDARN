#!/usr/bin/env python

"""process_batch_data.py: utility module fetch years of data and bin them by (radar, beam, frequency). Time resolution is T=(5n) min."""

__author__ = "Chakraborty, S."
__copyright__ = "Copyright 2020, SuperDARN@VT"
__credits__ = []
__license__ = "MIT"
__version__ = "1.0."
__maintainer__ = "Chakraborty, S."
__email__ = "shibaji7@vt.edu"
__status__ = "Research"

import os
import numpy as np
import datetime as dt
import argparse
import dateutil

from get_fit_data import FetchData
import pandas as pd
import fetch_data as fd

def parse_dataframe(df):
    o = df.copy()
    o["time_of_day"] = [x.minute+(60*x.hour) for x in o.time.tolist()]
    o["tfreq"] = np.rint(np.array(o["tfreq"])/1e3)
    o["noise.sky"] = np.round(o["noise.sky"], 3)
    _ox = pd.DataFrame()
    for bm in np.unique(df.bmnum):
        time_of_day, tfreq, nsky, bmnum, rsep = [], [], [], [], []
        _x = pd.DataFrame()
        for i in range(288):
            x = o[(o.bmnum==bm) & (o.time_of_day >= i*5) & (o.time_of_day < (i+1)*5)]
            time_of_day.append(i*5)
            tfreq.append(np.max(x["tfreq"]))
            nsky.append(np.min(x["noise.sky"]))
            bmnum.append(bm)
            rsep.append(np.min(x["rsep"]))
        _x["time_of_day"], _x["tfreq"], _x["nsky"], _x["bmnum"], _x["rsep"] =\
        time_of_day, tfreq, nsky, bmnum, rsep
        _ox = pd.concat([_ox, _x])
    return _ox

def batch_process_sky_noise_data(rad, start, end):
    dn = start
    conn = fd.get_session()
    while dn <= end:
        fname = "sd/{rad}.{dn}.csv".format(rad=rad, dn=dn.strftime("%Y-%m-%d"))
        if not conn.chek_remote_file_exists(fname + ".gz"):
            print("\n Process file: ", fname)
            fdata = FetchData( rad, [dn, dn + dt.timedelta(days=1)] )
            beams, _ = fdata.fetch_data(by="beam")
            df = fdata.convert_to_pandas(beams, s_params=["bmnum", "noise.sky", "tfreq", "scan", "nrang", "time", "rsep"])
            df = parse_dataframe(df)
            df.to_csv(fname, header=True, index=False)
            os.system("gzip " + fname)
            conn.to_remote_FS(fname + ".gz", True)
        dn = dn + dt.timedelta(days=1)
    conn.close()
    return

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--rad", default="bks", help="SuperDARN radar code (default bks)")
    parser.add_argument("-s", "--start", default=dt.datetime(2011,1,1), help="Start date (default 2011-01-01)", 
            type=dateutil.parser.isoparse)
    parser.add_argument("-e", "--end", default=dt.datetime(2011,1,1), help="End date (default 2011-01-01)", 
            type=dateutil.parser.isoparse)
    parser.add_argument("-v", "--verbose", action="store_false", help="Increase output verbosity (default True)")
    args = parser.parse_args()
    if args.verbose:
        print("\n Parameter list for simulation ")
        for k in vars(args).keys():
            print("     ", k, "->", vars(args)[k])
    batch_process_sky_noise_data(args.rad, args.start, args.end)
    pass
