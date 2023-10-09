import pandas as pd
import streamlit as st

from src import load, sidebar, processing, visualization

# load dataset
data = load.load_preaggregated()

# initialize sidebar
sidebar_filters, sidebar_visual_choices = sidebar.setup_sidebar(data)

# filter and aggregate dataset
data = processing.filter_sales_data(data, sidebar_filters)
data = processing.group_sales_data(data, sidebar_visual_choices)

# create avg and std
data = processing.compute_average_and_std(data, sidebar_visual_choices)
#st.write(data)
# visualize
visualization.create_visualization(data, sidebar_visual_choices)