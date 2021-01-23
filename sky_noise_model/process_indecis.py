#!/usr/bin/env python

"""process_indecis.py: utility module fetch years of geophysical parameters and overwtite the data file processed by process_batch_data.py"""

__author__ = "Chakraborty, S."
__copyright__ = "Copyright 2020, SuperDARN@VT"
__credits__ = []
__license__ = "MIT"
__version__ = "1.0."
__maintainer__ = "Chakraborty, S."
__email__ = "shibaji7@vt.edu"
__status__ = "Research"

import pandas as pd

def geomagnetic_quiet_days_by_Kp(start, end):
    """ 
        Identify 5 QDCs of a month using Kp.
        ------------------------------------
        International most quiet and most disturbed days of each month are deduced from the 
        Kp indices on the basis of three criteria for each day:
           1. The sum of the eight Kp values.
           2. The sum of squares of the eight Kp values.
           3. The maximum of the eight Kp values.

        According to each of these criteria, a relative order number is assigned to each day of
        the month, the three order numbers are averaged and the days with the lowest and the highest
        mean order numbers are selected as the five (respectively ten) quietest and the five most 
        disturbed days.

        It should be noted that these selection criteria give only a relative indication of the character
        of the selected days with respect to the other days of the same month. As the general disturbance
        level may be quite different for different years and also for different months of the same year, 
        the selected quietest days of a month may sometimes be rather disturbed or vice versa.
        
        In order to indicate such a situation, selected days which do not satisfy certain 
        absolute criteria are marked as follows.
            1. A selected quiet day is considered "not really quiet" and is marked by the
            letter A if Ap > 6, or marked by the letter K if Ap ≤ 6 and either one Kp 
            value > 3 or two Kp values > 2+.
            2. A selected disturbed day is considered "not really disturbed" and marked by
            an asterisk (*) if Ap < 20.

        More specific and detailed information may be found on the GFZ website devoted to Kp 
        and related geomagnetic indices.
    """
    return

def geomagnetic_quiet_days_by_AE(start, end, th=100.):
    """ 
        Identify QDCs of a month using AE, threshold (< 100 nT).
    """
    return

def geomagnetic_quiet_days_by_proton_flux(start, end, th=10):
    """ 
        Identify QDCs of a month using GOES proton flux, threshold (< 10 pfu).
    """
    return

def geomagnetic_quiet_days_by_solar_flux(start, end, th=1e-5):
    """ 
        Identify QDCs of a month using GOES solar soft X-ray flux, threshold (< M-class).
    """
    return