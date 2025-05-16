# src/eda_runner.py
from utils.utils import *
class EDAOrchestrator:
    def __init__(self, file_path, timestamp_col, key_columns):
        self.file_path = file_path
        self.timestamp_col = timestamp_col
        self.key_columns = key_columns
        self.df = None
    def run(self):
        self.df = load_data(self.file_path)
        self.df = clean_data(self.df, self.key_columns)     
        plot_time_series(self.df, self.timestamp_col, ['GHI', 'DNI', 'DHI', 'Tamb'])
        plot_correlations(self.df, self.key_columns + ['TModA', 'TModB'])


