# -*- coding: utf-8 -*-
"""
Created on Mon Jan  5 08:45:28 2015
Create and analyse CTVG
@author: TOSS
"""

import datetime as dt
import numpy as np
import pandas as pd
import networkx as nx
import TimeWindows as tw


def readDataFile(fn):
    """
    Read the data file with the trade contacts between premises.
    ----

    Input
    ----
    fn      : filename of data set containing trade activities per date
    Input file must have the following columns and column names:
    - Date
    - S
    - T
    - VOL
    
    Return
    ----
    ud      : sorted pandas dataframe with date as index
    """
    ud = pd.read_csv(fn, sep=',', parse_dates=['Date'], index_col=('Date'), 
                     dtype={'S': str, 'T': str}, engine='c')
    #
    # DataFrame nach Datum sortieren und resindex
    print 'Sort by date'
    ud.sort(inplace=True)
    #
    ud.reset_index(inplace=True)
    #
    # add frequency column to dataframe
    ud['Freq'] = pd.Series(np.ones(len(ud['S'])), index=ud.index)
    return ud


def dfslice(df, start, end):
    """
    Returns pandas dataframe for the time slice [start,end].
    --------

    Input
    ----
    df      : Dateframe for which the time silced object is created
    
    start   : start date (datetime.date Objekt)
    
    end     : end date (datetime.date Objekt)

    Return
    ----
    the sliced dataframe

    """
    df.set_index('Date', inplace=True)
    sdf = df[start:end]
    df.reset_index(inplace=True)
    sdf.reset_index(inplace=True)
    return sdf
    
    
def selectArea(df, aS=None, aT=None, link='and'):
    """
    Select aras for analysis.
    ----
    
    Input:
    ----
    S : string (list) containing the area to which sources belong to 
    
    T : string (list) containing the area to which targets belong to
    
    link: how are the conditions linked (if not AND then OR)
    
    Return:
    ----
    dataframe with S and T belonging to areas specified
    """
    if aT == None and aS != None:
        pattern = '|'.join(aS)
        sel = df.S.str.contains(pattern)
        return df(sel)
        
    


def AUAgg(df, level = 'M'):
    """
    AUAgg aggregate for adiminstrative units:
    
    Input:
    ----
    df : raw data as dateframe 
    
    level : administrative unit
    
        M - municipality level 
        
        D - district level
        
        F - federal states level
        
    Return:
    ----
    df : dataframe aggregated for admininistrative units: 
    """
    cdf = df.copy()
    if level == 'M':
        cdf['Sagg'] = df['S'].map(lambda x: x[3:-4])
        cdf['Tagg'] = df['T'].map(lambda x: x[3:-4])
    elif level == 'D':
        cdf['Sagg'] = df['S'].map(lambda x: x[3:-7])
        cdf['Tagg'] = df['T'].map(lambda x: x[3:-7])
    else:
        cdf['Sagg'] = df['S'].map(lambda x: x[3:5])
        cdf['Tagg'] = df['T'].map(lambda x: x[3:5])
    
    adf = pd.pivot_table(cdf, index = ['Date','Sagg','Tagg'],
                         values=['VOL','Freq'], aggfunc={'VOL': np.sum, 
                         'Freq': np.sum})
                         
    adf.reset_index(inplace=True)                         
    adf.rename(columns={'Sagg': 'S', 'Tagg': 'T'}, inplace=True)

    return adf
    
    
def toEdgeList(df):
    """
    Transform edgelist in the dataframe to an edgelist that can be passes to 
    networkx graph.
    
    Input
    -------
    df : the edgelist as pandas dataframe
    
    Return 
    -------
    edgelist with edges and attributes as dict
    """
    aeldf = pd.pivot_table(df, index = ['S','T'], values=['VOL','Freq'], 
                           aggfunc={'VOL': np.sum, 'Freq': np.sum})
                         
    edges = list(aeldf.index.values)
    attributes = aeldf.to_dict('records')

    ael =  [edges[x] + (attributes[x],) for x in np.arange(len(edges))]
    return ael


#
# main entry point
def main():
    # uncomment next line for full data set
    fn = "/Users/TOSS/Documents/Projects/CattleTVG/Edgelist/rawelri.csv"

    # this is a sample data set. Comment if full data set is used
    #fn = "/Users/TOSS/Documents/Projects/CattleTVG/Edgelist/elri1000.csv"

#
    #create a dataframe object of the raw edgelist
    print 'read the data'
    df_data = readDataFile(fn)
    print df_data.head()

    # set the time horizon for this analysis
    startdate = dt.datetime(2001,1,1)
    enddate   = dt.datetime(2010,12,31)
    obsperiod = dfslice(df_data, startdate, enddate)
    # print dfsliced.head()
    
    #
    # setup graph
    G = nx.DiGraph()
    # use sequential time windows
    tchunks = tw.timeWindow(startdate, enddate, n=520, width=7, sequential=True)
    for w in tchunks:
        start,end = w
        movements = dfslice(obsperiod,start,end)
        amove = AUAgg(movements, level='M')
        G.clear()
        G.add_edges_from(toEdgeList(amove))
        Gcc=sorted(nx.strongly_connected_component_subgraphs(G), key = len, reverse=True)
        print start.date(), len(Gcc[0]), G.number_of_nodes()


if __name__ == '__main__':
    main()