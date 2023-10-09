import streamlit as st

from config import config
from . import utils

def setup_sidebar(sales_data):
    # dictionaries for storing the choices from the sidebar
    sidebar_filters = {}
    sidebar_visual_choices = {}

    # sidebar title
    st.sidebar.header("Configurations")
    # switch sales quantity / revenue
    sidebar_visual_choices['metric'] = st.sidebar.radio("Display", ['Qty', 'Amount'], format_func=lambda x: config.METRICS.get(x))
    # choose size of rolling average window
    sidebar_visual_choices['rolling_window'] = st.sidebar.slider("Choose Window Size for Rolling Averages", 1, 90, config.DEFAULT_ROLLING_WINDOW)
    # choose type of average: simple moving avg, weighted moving avg, exponential avg
    sidebar_visual_choices['method'] = st.sidebar.radio("Method", config.AVERAGING_METHODS)
    # choose time frame of analysis
    sidebar_filters['start_date'], sidebar_filters['end_date'] = st.sidebar.date_input(
        "Choose Date Range (2022/04/01 – 2022/06/28)",
        [sales_data['Date'].min().date(), sales_data['Date'].max().date()])
    # choose categories
    sorted_categories = sorted(sales_data['Category'].unique().tolist(), key=utils.sort_alpha_digit)
    sidebar_filters['categories'] = st.sidebar.multiselect("Choose Categories", options=sorted_categories, default=sorted_categories)
    # choose sizes
    sorted_sizes = utils.get_sorted_sizes(sales_data)
    sidebar_filters['sizes'] = st.sidebar.multiselect("Choose Sizes", options=sorted_sizes, default=sorted_sizes)
    # checkboxes for confidence interval
    sidebar_visual_choices['show_CI68'] = st.sidebar.checkbox('Show CI68', True)
    sidebar_visual_choices['show_CI95'] = st.sidebar.checkbox('Show CI95', True)
    sidebar_visual_choices['show_CI99'] = st.sidebar.checkbox('Show CI99.7', True)

    return sidebar_filters, sidebar_visual_choices
