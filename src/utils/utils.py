import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import seaborn as sns

# Load CSV data with optional datetime column
def load_data(file_path, timestamp_col=None):
    """"
    Loads the csv using file path
    Args:
        file path: The location of the csv
    Returns:
        dataframe
    """
    df = pd.read_csv(file_path)
    if timestamp_col and timestamp_col in df.columns:
        df[timestamp_col] = pd.to_datetime(df[timestamp_col], errors='coerce')
        df = df.dropna(subset=[timestamp_col])
    return df

# Clean outliers using Z-score and impute missing with median
def clean_data(df, key_columns):
    """
    Imputes missing values in specified columns using the median strategy.
    Args:
        df (pd.DataFrame): The input DataFrame to clean.
        columns (list): List of column names to check and impute.
    Returns:
        pd.DataFrame: A cleaned DataFrame.
    """
    df = df.copy()
    z_scores = (df[key_columns] - df[key_columns].mean()) / df[key_columns].std()
    outliers = (z_scores.abs() > 3)
    df[key_columns] = df[key_columns].mask(outliers)
    df[key_columns] = df[key_columns].fillna(df[key_columns].median())
    return df


# Get summary and missing report
def generate_summary(df):
    """"
    Generates a summary of the dataframe
     Args:
        df (pd.DataFrame): The input DataFrame to clean.
    Returns:
        pd.DataFrame: with description of summary and missing
    """
    summary = df.describe()
    missing = pd.DataFrame({
        "missing_count": df.isna().sum(),
        "missing_percent": df.isna().sum() / len(df) * 100
    })
    missing = missing[missing["missing_count"] > 0]
    return summary, missing


def detect_outliers_zscore(df, columns, threshold):
    """
    Detect and optionally remove rows with outliers using Z-score.

    Args:
        df (pd.DataFrame): Input DataFrame.
        columns (list): Columns to check for outliers.
        threshold (float): Z-score threshold to identify outliers.

    Returns:
        pd.DataFrame: DataFrame with outliers removed.
    """
    df_clean = df.copy()
    outlier_counts = {}

    for col in columns:
        if df_clean[col].dtype not in [np.float64, np.int64]:
            continue
        z_scores = (df_clean[col] - df_clean[col].mean()) / df_clean[col].std()
        outliers = z_scores.abs() > threshold
        outlier_counts[col] = outliers.sum()
        df_clean = df_clean[~outliers]  # Drop outliers

    print("Outliers removed per column:")
    for col, count in outlier_counts.items():
        print(f"{col}: {count} rows")

    return df_clean
# Plot time series for selected columns
def plot_time_series(df, time_col, value_columns):
    """"
    Plots the time series of time vs metric values

    Args:
        df -> The Dataframe
        time_col -> The time axis
        value_columns -> The target cols
    Returns: 
        Time series plot
    """
    df.set_index(time_col)[value_columns].plot(figsize=(14, 5), title=f"{', '.join(value_columns)} Over Time")
    plt.tight_layout()
    plt.show()

# Plot correlation heatmap for numeric columns

def plot_correlations(df, columns):
    """"
    plots correlation of columns against each other

    Args:
        df -> The Dataframe
        columns -> The target columns
    Returns:
        Correlation plot
    """
    corr = df[columns].corr()
    sns.heatmap(corr, annot=True, cmap='coolwarm')
    plt.title("Correlation Heatmap")
    plt.show()

# Plot scatter and optional bubble plot
def plot_scatter(df, x, y, bubble_size_col=None):
    """"
    plots scatter plot

    Args:
        df -> The Dataframe
        x -> x coordinate
        y -> y coordinate
    Returns:
        Scatter plot
    """
    sns.scatterplot(data=df, x=x, y=y, alpha=0.5)
    plt.title(f"{x} vs {y}")
    plt.show()

    if bubble_size_col and bubble_size_col in df.columns:
        sns.scatterplot(data=df, x=x, y=y, size=bubble_size_col, sizes=(20, 200), alpha=0.5)
        plt.title(f"{x} vs {y} (Bubble size = {bubble_size_col})")
        plt.show()

# Histogram
def plot_histogram(df, column):
    """"
    plots histogram

    Args:
        df -> The Dataframe
        column -> target cols
    Returns:
        Histogram

    """
    df[column].hist(bins=50)
    plt.title(f"Distribution of {column}")
    plt.xlabel(column)
    plt.ylabel("Frequency")
    plt.show()

def plot_bivariate_scatters(df, pairs, hue=None):
    """
    Plots scatter plots for each column pair in `pairs`.

    Args:
        df (pd.DataFrame): Input data
        pairs (list of tuples): List of (x_col, y_col) pairs to plot
        hue (str, optional): Column to color by
    """
    for x_col, y_col in pairs:
        plt.figure(figsize=(6, 4))
        sns.scatterplot(data=df, x=x_col, y=y_col, hue=hue)
        plt.title(f"{x_col} vs. {y_col}")
        plt.tight_layout()
        plt.show()


def plot_univariate_histograms(df, numeric_cols, bins=30):
    """
    Plots histograms with KDE for each numeric column in the DataFrame.

    Args:
        df (pd.DataFrame): Input data
        numeric_cols (list): List of column names to plot
        bins (int): Number of histogram bins
    """
    for col in numeric_cols:
        plt.figure(figsize=(6, 4))
        sns.histplot(df[col], kde=True, bins=bins)
        plt.title(f"{col} Distribution")
        plt.xlabel(col)
        plt.ylabel("Count")
        plt.tight_layout()
        plt.show()
# Export cleaned CSV
def export_cleaned(df, output_path):
    """"
    cleans us the csv

    Args:
        df -> Dataframe
        output -> Directory path
    Return 
        cleaned up csv
    """
    df.to_csv(output_path, index=False)
    print(f"[✓] Exported cleaned data to {output_path}")
