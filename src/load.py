import os

import pandas as pd
import streamlit as st

from config import config
from . import preprocessing

@st.cache_data
def load_preaggregated():
    # define filepath
    preprocessed_file = os.path.join(config.DATA_FOLDER, config.PREPROCESSED_FILE)
    
    # if file doesn't exist, run preprocessing script to create it
    if not os.path.exists(preprocessed_file):
        preprocessing.preprocess_dataset()
    
    # return preprocessed dataset
    return pd.read_parquet(preprocessed_file)