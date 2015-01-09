# -*- coding: utf-8 -*-
"""
Created on Mon Jan  5 08:45:28 2015
Work with time functions
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
    Gibt einen dateframe für den Zeitraum [start,end] zurück.
    
    Eingabeparameter
    df      : Dateframe aus dem der Ausschnitt gebildet werden soll
              df muss sortiert sein.
    start   : Startdatum (datetime.date Objekt)
    end     : Enddatum (datetime.date Objekt)
    
    return:
    Ausschnitt 
    """
    return df[start:end]
    
def readDataFile(fn):
    """
    Read the data file with the trade contacts between premises.
    
    Eingabeparameter:
    fn      : File Name mit den zeitaufgelösten handelsaktivitäten zwischen Betrieben
    Rückgabewert:
    ud      : Sortiereter DatenFrame
    """
    ud = pd.read_csv(fn, sep=',', parse_dates=['Date'], index_col='Date')
    #
    # DataFrame nach Datum sortieren
    ud = ud.sort()
    
    return ud

def createGraph(df):
    """
    df is the raw edgelist
    """
    #
    # aggregate edgelist for dates. the edgelist must be sorted see 
    # readDataFile() above
    adf = pd.pivot_table(df, index=['S', 'T'], values = 'VOL', aggfunc={"VOL":[len, np.sum]})
    adf.rename(colums={'len':'Freq', 'sum':'Vol'},inplace=True)
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
    
    
    return nx.read_edgelist(df, create_using=nx.DiGraph())
#
# main entry point
def main():
    # uncomment next line for full data set
    # fn = "/Users/TOSS/Documents/Projects/CattleTVG/Edgelist/elri.csv"

    # this is a sample data set. Comment if full data set is used
    fn = "/Users/TOSS/Documents/Projects/CattleTVG/Edgelist/elri20.csv"
    
    data = readDataFile(fn)
    G = createGraph(data)
    
if __name__ == '__main__':
    main()