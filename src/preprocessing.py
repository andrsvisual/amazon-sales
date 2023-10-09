import os
import pandas as pd
import streamlit as st

from config import config

INPUT_FILE = os.path.join(config.DATA_FOLDER, config.RAW_DATA_FILE)
OUTPUT_FILE = os.path.join(config.DATA_FOLDER, config.PREPROCESSED_FILE)

def preprocess_dataset():
    # read raw dataset
    try:
        df = pd.read_csv(INPUT_FILE)
    except FileNotFoundError:
        st.error(f"```\n\
Error: the file containing the dataset was not found. \n\
Please download the raw sales data at https://www.kaggle.com/datasets/thedevastator/unlock-profits-with-e-commerce-sales-data \n\
place '{config.RAW_DATA_FILE}' in the '{config.DATA_FOLDER}' folder and run again.")

    # parse dates
    df['Date'] = pd.to_datetime(df['Date'], format='%m-%d-%y')

    # remove first and last day, since they are not complete
    first_day, last_day = df['Date'].min(), df['Date'].max()

    # manually selected list of statuses
    valid_shipping_statuses = ['Shipped - Delivered to Buyer', 'Shipped', 'Shipped - Out for Delivery',
                            'Shipped - Picked Up', 'Shipping']

    # filter NA values, dates, and shipping statuses
    df = df[
        (df['Date'] != first_day) & (df['Date'] != last_day) &
        (df['Status'].isin(valid_shipping_statuses)) &
        (df['Qty'] > 0) &
        (df['Amount'].notna()) &
        (df['currency'].notna()) &
        (df['ship-country'].notna())
    ]

    # preaggregate data by date, category, and size to reduce file size
    df_grouped = df.groupby(['Date', 'Category', 'Size']).agg({'Qty': 'sum', 'Amount': 'sum'}).reset_index()
    # save to parquet
    df_grouped.to_parquet(OUTPUT_FILE)