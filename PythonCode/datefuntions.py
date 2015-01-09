# -*- coding: utf-8 -*-
"""
Created on Mon Jan  5 08:45:28 2015
Work with time functions
@author: TOSS
"""

import datetime as dt
import numpy as np
today = dt.date.today()
print today
oneweeklater = today + dt.timedelta(7)
print oneweeklater

# increment the dates
for d in np.arange(0,365,1):
    startdate = today + dt.timedelta(d)
    enddate = startdate + dt.timedelta(7)
    print startdate, enddate

