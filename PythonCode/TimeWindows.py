# -*- coding: utf-8 -*-
"""
Created on Sat Jan 10 10:35:28 2015
Experiment a little bit with datetime function. Especially create moving time
windows. Consecutive and moving windows are considered
@author: TOSS
"""
import datetime as dt
import numpy as np

def timewindow(start, n=1, width = 6, overlap=True):
    """
    returns a list of n time windows starting at start. The windows are either \n
    overlapping (overlap=True) or not (overlap = False)
    """
    if overlap == False:
        return []
    else:
        return [(start + dt.timedelta(t), start + dt.timedelta(t)+dt.timedelta(width)) for t in np.arange(n)]
    
def slidingWindow(start, n=1, width=6):
    """
    returns a time window evevry time the function is called
    """
    for t in np.arange(n):
        beg = start + dt.timedelta(t)
        end = beg + dt.timedelta(width)
        yield(beg,end)
        
def sequenceWindow(start, n=1, width=2):
    for x in np.arange(0,n*width,width):
        beg = start + dt.timedelta(x)
        end = beg + dt.timedelta(width-1)
        yield(beg,end)
        
def timeWindow(start, n=1, width=6, sequential=False):
    """
    returns a sequential or silding time window starting at start
    """
    if sequential == False:
        for t in np.arange(n):
            beg = start + dt.timedelta(t)
            end = beg + dt.timedelta(width)
            if end > dt.datetime(2010,12,31):
                break
            else:
                yield(beg,end)
    else:
        for t in np.arange(0,n*width,width):
            beg = start + dt.timedelta(t)
            end = beg + dt.timedelta(width-1)
            if end > dt.datetime(2010,12,31):
                break
            else:
                yield(beg,end)        
    
def main():
    start = dt.datetime(2001,1,1)
    start2 = dt.datetime(2010,12,18)
#    print timewindow(start, n=1)
#    
    print 'This uses sliding window'
    tchunks = slidingWindow(start, n=3, width=7)
    for w in tchunks:
        print w
        
    print 'This is sequence window with width = 7'
    tchunks = sequenceWindow(start, n=3, width=7)
    for w in tchunks:
        print w

    print 'Using timeWindow sequential=False'
    tchunks = timeWindow(start2, n=8, width=7)
    for w in tchunks:
        print w

    print 'Using timeWindow sequential=True'
    tchunks = timeWindow(start2, n=8, width=7, sequential=True)
    for w in tchunks:
        print w
        
        
if __name__ == '__main__':
    main()
