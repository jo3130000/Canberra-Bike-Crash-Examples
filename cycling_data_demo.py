#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Provides functions to demonstrate the contents and functionality available
in the loaded datasets.

@author:  tarney
@uid:     u7378856
@created: Sun Sep 19 13:57:28 2021
"""

import pandas as pd

from cycling_load_data import *

##############################################################################
#                               HELPER FUNCTIONS                             #
##############################################################################

def suburb_demo(suburb, data):
    """
    Demonstrates the Suburb class and how it may be used to take a point
    given by latitude and longitude and return the suburb and district
    that point falls within

    Parameters
    ----------
    suburb : Suburb
        A Suburb object instantiated with GIS data.
    data : dict
        A dictionary of all the data loaded by the system.

    Returns
    -------
    None.

    """
    
    print()
    print('It stores all the geospatial data which allows a particular point,')
    print('given by a lat and long, to be located by suburb and district.')
    print()
    print('For example:')
    
    for station in data['rainfall']:
        name = data['rainfall'][station].get_station_name()
        print()
        print(f"Weather station '{name}' is located within:")
        
        lat = data['rainfall'][station].get_station_lat()
        long = data['rainfall'][station].get_station_long()
        located = suburb.locate(lat, long)
        
        for level, area in located.items():
            print(f"  {level.title()}: {area}")
        

def rainfall_demo(rainfall):
    """
    Demonstrates the Rainfall class and how it may be used to take a point
    given by latitude and longitude and return the distance of that point
    from the weather station, as well as the rainfall measurements taken by 
    the station.
    

    Parameters
    ----------
    rainfall : Rainfall
        A Rainfall object instantiated with rainfall data.

    Returns
    -------
    None.

    """
    
    print()
    print('Attributes are:')
    station_id = rainfall.get_station_id()
    station_name = rainfall.get_station_name()
    station_lat = rainfall.get_station_lat()
    station_long = rainfall.get_station_long()
    station_height = rainfall.get_station_height()
    print(f'  Station ID: {station_id}')
    print(f'  Station Name: {station_name}')
    print(f'  Station Latitude: {station_lat}')
    print(f'  Station Longitude: {station_long}')
    print(f'  Station Height: {station_height}')
    
    print()
    print('It can also calculate the distance from another point...')
    print()
    lat = -35.308056
    long = 149.124444
    print(f'For example, Parliament House is located at ({lat:.2f}, {long:.2f}),')
    distance = rainfall.distance_from_station(lat, long)
    print(f'the distance from the station is: {distance:.2f}km')
    
    print()
    print('It also contains a pandas dataframe...')
    df = rainfall.get_data()
    
    dataframe_demo(df)


def dataframe_demo(df):
    """
    Outputs a summary of a pandas DataFrame in terms of the dimensions of the 
    data, the attributes of the data, whether the attributes include a datetime
    and/or latitude and longitude, and outputs a sample of the data.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame to summarise.

    Returns
    -------
    None.

    """
    
    print()
    
    rows, cols = df.shape
    print(f'The dataframe consists of {rows:,} rows and {cols} columns')
    
    columns = list(df.columns)
    print()
    print('Columns are:')
    for i, column in enumerate(columns):
        print(f'  {i+1}: {column}')
    
    if 'date_time' in df or 'lat' in df:
        print()
        print('Note:')
        if 'date_time' in df:
            print(" - column 'date_time' contains datetime objects")
            
        if 'lat' in df:
            print(" - columns 'lat' and 'long' contain floating point values")
            
    print()
    print("Here's a sample of the data:")
    print()        
    print(df)


##############################################################################
#                               CENTRAL FUNCTION                             #
##############################################################################

def data_demo(data, suburb_type):
    """
    Takes a dictionary of datasets, as generated by the 'load_data' module
    and iterates over each to provide a summary of the data and any built in
    functionality available.

    Parameters
    ----------
    data : dict
        Dictionary of datasets.

    Returns
    -------
    None.

    """
    
    # print()
    # print('############################################################################')
    # print('#                                DATA DEMO                                 #')
    # print('############################################################################')
    
    for key, value in data.items():
        print()
        
        if isinstance(value, pd.core.frame.DataFrame):
            line_length = len(key) + 8
            print(f"data['{key}']")
            print('-' * line_length)
            print("Is a pandas dataframe")
            dataframe_demo(value)
            # tdf = value
            print()
        
        if isinstance(value, dict):
            for sub_key, sub_value in data[key].items():
                line_length = len(key) + len(sub_key) + 12
                print(f"data['{key}']['{sub_key}']")
                print('-' * line_length)
                print("Is a Rainfall object")
                rainfall_demo(sub_value)
                print()
                
        if isinstance(value, suburb_type):
            line_length = len(key) + 8
            print(f"data['{key}']")
            print('-' * line_length)
            print("Is a Suburb object")
            suburb_demo(value, data)
            print()