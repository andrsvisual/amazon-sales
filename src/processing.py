import numpy as np
import pandas as pd
import streamlit as st

@st.cache_data
def filter_sales_data(data, sidebar_filters):
    # apply data filters from the sidebar
    filtered_data = data[
        (data['Category'].isin(sidebar_filters['categories'])) & 
        (data['Size'].isin(sidebar_filters['sizes'])) & 
        (data['Date'] >= pd.Timestamp(sidebar_filters['start_date'])) & 
        (data['Date'] <= pd.Timestamp(sidebar_filters['end_date']))
    ]
    return filtered_data

@st.cache_data
def group_sales_data(data, sidebar_visual_choices):
    # group chosen metric (qty/revenue) by days
    return data.groupby('Date').agg({sidebar_visual_choices['metric']: 'sum'}).reset_index()


@st.cache_data
def compute_average_and_std(data, sidebar_visual_choices):
    # compute the moving average and standard deviation using the chosen method

    if sidebar_visual_choices['method'] == 'SMA':
        # simple moving average
        data['Average'] = data[sidebar_visual_choices['metric']].rolling(window=sidebar_visual_choices['rolling_window'], min_periods=1).mean()
        data['Std'] = data[sidebar_visual_choices['metric']].rolling(window=sidebar_visual_choices['rolling_window'], min_periods=1).std()

    elif sidebar_visual_choices['method'] == 'WMA':
        # weighted moving average
        weights = np.arange(1, sidebar_visual_choices['rolling_window'] + 1)
        # define aggregate function for average
        def compute_weighted_avg(values):
            return np.dot(values, weights[:len(values)]) / weights[:len(values)].sum()

        data['Average'] = data[sidebar_visual_choices['metric']].rolling(window=sidebar_visual_choices['rolling_window'], min_periods=1).apply(compute_weighted_avg, raw=True)
        
        # define aggregate function for standard deviation
        def compute_weighted_std(values):
            wmean = np.dot(values, weights[:len(values)])/weights[:len(values)].sum()
            return np.sqrt(np.dot(weights[:len(values)], (values - wmean)**2)/weights[:len(values)].sum())

        data['Std'] = data[sidebar_visual_choices['metric']].rolling(window=sidebar_visual_choices['rolling_window'], min_periods=1).apply(compute_weighted_std, raw=True)

    elif sidebar_visual_choices['method'] == 'EWM':
        # exponentioally weighted moving average
        data['Average'] = data[sidebar_visual_choices['metric']].ewm(span=sidebar_visual_choices['rolling_window'], adjust=False).mean()
        data['Std'] = data[sidebar_visual_choices['metric']].ewm(span=sidebar_visual_choices['rolling_window'], adjust=False).std()

    # give the first day the same std as the second day
    data.at[0, 'Std'] = data.at[1, 'Std']
    
    return data