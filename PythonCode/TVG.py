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

#today = dt.date.today()
#print today
#oneweeklater = today + dt.timedelta(7)
#print oneweeklater

# increment the dates
#for d in np.arange(0,365,1):
#    startdate = today + dt.timedelta(d)
#    enddate = startdate + dt.timedelta(7)
#    print startdate, enddate

def dfslice(df, start, end):
    """
    Returns pandas dataframe for the time slice [start,end].
    
    Input
    df      : Dateframe for which the time silced object is created
    start   : start date (datetime.date Objekt)
    end     : end date (datetime.date Objekt)
    
    return  : sliced dataframe 
    """
    return df[start:end]
    
def readDataFile(fn):
    """
    Read the data file with the trade contacts between premises.
    
    Input
    fn      : filename of data set containing trade activities per date
    
    Return
    ud      : sorted pandas dataframe with date as index 
    """
    ud = pd.read_csv(fn, sep=',', parse_dates=['Date'], index_col='Date')
    #
    # DataFrame nach Datum sortieren
    ud = ud.sort()
    
    return ud

def createGraph(df):
    """
    Input
    df is the raw edgelist
    
    Output
    networkx directed graph
    """
    #
    # aggregate edgelist for dates. the edgelist must be sorted see 
    # readDataFile() above
    adf = pd.pivot_table(df, index=['S','T'], values = 'VOL', aggfunc={"VOL":[len,np.sum]})
    adf.rename(columns={'len':'Freq', 'sum':'Vol'}, inplace=True)
    #
    # seperate edges and attributes and recombine to attribute edgelist
    edges = list(adf.index.values)
    attributes = adf.to_dict('records')
    ael =  [edges[x] + (attributes[x],) for x in np.arange(len(edges))] 
    #
    # create the net
    G = nx.DiGraph()
    G.add_edges_from(ael)
    
    return G

#
# main entry point
def main():
    # uncomment next line for full data set
    # fn = "/Users/TOSS/Documents/Projects/CattleTVG/Edgelist/elri.csv"

    # this is a sample data set. Comment if full data set is used
    fn = "/Users/TOSS/Documents/Projects/CattleTVG/Edgelist/elri.csv"
    
#
    #create a dataframe object of the raw edgelist
    print 'read the data'
    data = readDataFile(fn)
    #
    # set start and end data for time slice
    startdate = dt.datetime(2001,1,1) # January 1st, 2001
    enddate = startdate+dt.timedelta(6) # one week interval
    #
    # slice the data
    print 'slice the data'
    df_sliced = dfslice(data,startdate,enddate)
    
    print 'create the graph'
    G = createGraph(df_sliced)
    
    print startdate, G.number_of_nodes(), nx.density(G)
    
if __name__ == '__main__':
    main()