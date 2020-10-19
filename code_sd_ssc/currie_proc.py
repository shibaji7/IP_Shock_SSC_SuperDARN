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

def dat2fitacf(f="../data/currie.csv", rad="kod"):
    """ Convert to fitacf files """
    df = pd.read_csv(f)
    df["dn"] = [dt.datetime(y,m,d) for y, m, d in zip(df.Year,df.S_Month,df.S_Day)]
    j = 0
    for d in df["dn"].tolist():
        name = "/sd-data/{y}/dat/{r}/{du}*.dat.bz2".format(y=d.year, r=rad, du=d.strftime("%Y%m%d"))
        files = glob.glob(name)
        for dat_zip in files:
            print(" Proc:", dat_zip)
            if j==0: os.chdir("../data/fitacf/")
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
    return


if __name__ == "__main__":
    dat2fitacf()
