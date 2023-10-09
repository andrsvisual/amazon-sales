import seaborn as sns

DATA_FOLDER = "data"
RAW_DATA_FILE = "Amazon Sale Report.csv"
PREPROCESSED_FILE = "preaggregated_sales.parquet"

DATA_PATH = 'data'
PREAGGREGATED_SALES_FILE = 'preaggregated_sales.parquet'

METRICS = {
    'Qty': 'Quantity Sold',
    'Amount': 'Revenue'
}

DEFAULT_ROLLING_WINDOW = 14

AVERAGING_METHODS = ['SMA', 'WMA', 'EWM']

DEFAULT_START_DATE = '2022-04-01'
DEFAULT_END_DATE = '2022-06-28'

sns_palette = sns.color_palette("deep")
PALETTE = {
    'line_color': sns_palette[0],
    'scatter_color': sns_palette[3],
    'ci68_color': sns.dark_palette(sns_palette[0])[3],
    'ci95_color': sns.dark_palette(sns_palette[0])[2],
    'ci99_color': sns.dark_palette(sns_palette[0])[1],
}

PLOT_DIMENSIONS = (12, 6)