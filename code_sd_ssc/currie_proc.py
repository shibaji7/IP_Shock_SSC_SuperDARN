#!/usr/bin/env python

"""currie_proc.py: module is dedicated to process all data from Currie et al. 2016."""

__author__ = "Chakraborty, S."
__copyright__ = "Copyright 2020, SuperDARN@VT"
__credits__ = []
__license__ = "MIT"
__version__ = "1.0."
__maintainer__ = "Chakraborty, S."
__email__ = "shibaji7@vt.edu"
__status__ = "Research"

import sys
import os
import glob
import pandas as pd
import datetime as dt

import glob
from get_sd_data import FetchData
from plot_utils import *

def dat2fitacf(f="../data/currie.csv", rad="tig"):
    """ Convert to fitacf files """
    df = pd.read_csv(f)
    df["dn_start"] = [dt.datetime(y,m,d) for y, m, d in zip(df.Year,df.S_Month,df.S_Day)]
    df["dn_end"] = [dt.datetime(y,m,d) for y, m, d in zip(df.Year,df.R_Month,df.R_Day)]
    j = 0
    for s, e in zip(df["dn_start"].tolist(), df["dn_end"].tolist()):
        d = s
        while d <= e:
            name = "/sd-data/{y}/dat/{r}/{du}*.dat.bz2".format(y=d.year, r=rad, du=d.strftime("%Y%m%d"))
            files = glob.glob(name)
            for dat_zip in files:
                print(" Proc:", dat_zip)
                if j==0: os.chdir("../data/fitacf/%s"%rad)
                os.system("cp {fn} .".format(fn=dat_zip))
                local = dat_zip.split("/")[-1]
                os.system("bzip2 -dk " + local)
                dat = local.replace(".bz2", "")
                rawacf, fitacf = dat.replace(".dat", ".rawacf"), dat.replace(".dat", ".fitacf")
                os.system("dattorawacf {i} > {o}".format(i=dat, o=rawacf) )
                os.system("make_fit {i} > {o}".format(i=rawacf, o=fitacf) )
                if os.path.exists(fitacf + ".bz2"): os.system("rm " + fitacf + ".bz2")
                os.system("bzip2 -z " + fitacf)
                os.system("rm " + dat + " " + rawacf + " " + local)
                j += 1
            d = d + dt.timedelta(days=1)
    return

def plot_figure2(rad, bm, fname="figure2.png"):
    files = glob.glob("../data/fitacf/%s/20021001*"%rad)
    files.extend(glob.glob("../data/fitacf/%s/20021002*"%rad))
    fd = FetchData(rad, [dt.datetime(2002,10,1), dt.datetime(2002,10,3)], files=files)
    beams, _ = fd.fetch_data()
    rec = fd.convert_to_pandas(beams)
    rec = rec.sort_values(by=["time"])
    print(" Total records: ", len(rec))
    rti = RangeTimePlot(80, "", num_subplots=1)
    rti.addPlot(rec, bm, param="v", title="", pmax=200, step=50, xlabel="Time UT")
    rti.save("../figures/currie/"+fname)
    return

def _del_():
    import os
    os.system("rm -rf __pycache__/")
    return

if __name__ == "__main__":
    case = 2
    if case == 0: dat2fitacf()
    elif case == 1: plot_figure2("tig", 14)
    elif case == 2: plot_figure2("kod", 7, "figure8.png")
    _del_()
