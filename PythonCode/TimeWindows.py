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
        
def twindow(wstart, wend=dt.datetime(2010,12,31), n=1, width=7, sequential=False):
    """
    returns a sequential or silding time window starting at start 
    ---
    
    Input:
    ----
    wstart: The starting date of the time window
    
    wend : The end of the observational period. The end of the timewindow is lesser
    of equal to endofTW.
    
    width: width of the time window 
    
    n : number of slices
    
    sequential (bool): 
    
    **False**: the window is sliding i.r. [t,t+width], [t+1,t,width+1]
    
    **True**: the window is sequential i.e. [t,t+width],[t+width+1,t+2 width+1]]
    
    yield:
    iterator object
    """
    if sequential == False:
        for t in np.arange(n):
            beg = wstart + dt.timedelta(t)
            end = beg + dt.timedelta(width-1)
            if end > wend:
                break
            else:
                yield(beg,end)
    else:
        for t in np.arange(0,n*width,width):
            beg = wstart + dt.timedelta(t)
            end = beg + dt.timedelta(width-1)
            if end > wend:
                break
            else:
                yield(beg,end)     
                
                
def expandingWindow(start, endofTW=dt.datetime(2010,12,31), n=1, width=7):
    """
    return expanding time window stating at start.
    ----
    
    Input:
    ----
        + start: start date (datetime object) for the expanding window
        + endofTW : end date of the expanding time window could not be longer that 2010-12-31
        + n : number of times the window is expanded
        + width : the width (days) of expansion
    Return:
    ----
    yield: iterator object
        
    
    Example:
    ----
    Let `d` denote the start date and `n` is set to 3. The the first, second 
    and third time windows ranges from `d` to `d+6`, to `d+12` and to `d+18` 
    respectively.
    """
    for t in np.arange(width,(n+1)*width,width):
        # print t
        end = start + dt.timedelta(t-1)
        if end > endofTW:
            break
        else:
            yield(start,end) 
    
def main():
    start = dt.datetime(2001,1,1)
    start2 = dt.datetime(2010,12,18)
    start3 = dt.datetime(2010,12,19)
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
    tchunks = twindow(start2, n=8, width=7)
    for w in tchunks:
        print w

    print 'Using timeWindow sequential=True'
    tchunks = twindow(start2, n=8, width=7, sequential=True)
    for w in tchunks:
        print w
        
        
if __name__ == '__main__':
    main()
