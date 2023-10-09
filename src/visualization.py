import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import seaborn as sns
import streamlit as st

from config import config

# use entire space of the page
st.set_page_config(layout="wide")

# plot the confidence intervals as colored areas
def plot_confidence_intervals(ax, data, sidebar_visual_choices):
    if sidebar_visual_choices['show_CI68']:
        ax.fill_between(
            data['Date'], data['Average'] - data['Std'], 
            data['Average'] + data['Std'], 
            color=config.PALETTE['ci68_color'], 
            alpha=0.4, label='CI68'
            )
    if sidebar_visual_choices['show_CI95']:
        ax.fill_between(
            data['Date'], data['Average'] - 2*data['Std'], 
            data['Average'] + 2*data['Std'], 
            color=config.PALETTE['ci95_color'], 
            alpha=0.2, label='CI95'
            )
    if sidebar_visual_choices['show_CI99']:
        ax.fill_between(
            data['Date'], data['Average'] - 3*data['Std'], 
            data['Average'] + 3*data['Std'], 
            color=config.PALETTE['ci99_color'], 
            alpha=0.2, label='CI99.7'
            )

# define the plot title, labels, etc
def set_plot_titles_labels(ax, data, sidebar_visual_choices):
    ax.set_title('Amazon Sales Over Time with Rolling Average', 
                 fontsize=16, fontweight='bold')
    ax.set_xlabel('Date', fontsize=14)
    ax.set_ylabel(config.METRICS[sidebar_visual_choices['metric']], fontsize=14)
    ax.set_ylim(0, data[sidebar_visual_choices['metric']].max() * 1.1)
    ax.set_xlim(data['Date'].min(), data['Date'].max())
    ax.legend(loc='lower right')
    ax.grid(color='gray', linestyle='-', linewidth=0.2, which='both')

# create label formatter that minimizes plot size change when switching metric
def custom_formatter(x, _):
    if x >= 1e6:
        return f'{x*1e-6:,.1f}M'
    elif x >= 1e4:
        return f'{x*1e-3:,.0f}k'
    else:
        return f'{x:,.0f}'


def create_visualization(data, sidebar_visual_choices):
    # initialize plot
    fig, ax = plt.subplots(figsize=config.PLOT_DIMENSIONS)
    # plot actual sales data
    sns.scatterplot(x='Date', y=sidebar_visual_choices['metric'], 
                    data=data, color=config.PALETTE['scatter_color'], 
                    label='Daily Sales', s=50, edgecolor="black", ax=ax)
    # plot average sales
    #sns.lineplot(x='Date', y='Average', data=data, color=config.PALETTE['line_color'], 
    #             linewidth=2.5, label='Rolling Average', ax=ax)
    # plot confidence intervals
    plot_confidence_intervals(ax, data, sidebar_visual_choices)
    # set titles and labels
    set_plot_titles_labels(ax, data, sidebar_visual_choices)
    # format y-axis
    ax.yaxis.set_major_formatter(FuncFormatter(custom_formatter))
    # display the plot
    st.pyplot(fig)
