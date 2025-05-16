import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Load CSV data with optional datetime column
def load_data(file_path, timestamp_col=None):
    df = pd.read_csv(file_path)
    if timestamp_col and timestamp_col in df.columns:
        df[timestamp_col] = pd.to_datetime(df[timestamp_col], errors='coerce')
        df = df.dropna(subset=[timestamp_col])
    return df

# Clean outliers using Z-score and impute missing with median
def clean_data(df, key_columns):
    df = df.copy()
    z_scores = (df[key_columns] - df[key_columns].mean()) / df[key_columns].std()
    outliers = (z_scores.abs() > 3)
    df[key_columns] = df[key_columns].mask(outliers)
    df[key_columns] = df[key_columns].fillna(df[key_columns].median())
    return df


# Get summary and missing report
def generate_summary(df):
    summary = df.describe()
    missing = pd.DataFrame({
        "missing_count": df.isna().sum(),
        "missing_percent": df.isna().sum() / len(df) * 100
    })
    missing = missing[missing["missing_count"] > 0]
    return summary, missing
# Plot time series for selected columns
def plot_time_series(df, time_col, value_columns):
    df.set_index(time_col)[value_columns].plot(figsize=(14, 5), title=f"{', '.join(value_columns)} Over Time")
    plt.tight_layout()
    plt.show()

# Plot correlation heatmap for numeric columns

def plot_correlations(df, columns):
    corr = df[columns].corr()
    sns.heatmap(corr, annot=True, cmap='coolwarm')
    plt.title("Correlation Heatmap")
    plt.show()

# Plot scatter and optional bubble plot
def plot_scatter(df, x, y, bubble_size_col=None):
    sns.scatterplot(data=df, x=x, y=y, alpha=0.5)
    plt.title(f"{x} vs {y}")
    plt.show()

    if bubble_size_col and bubble_size_col in df.columns:
        sns.scatterplot(data=df, x=x, y=y, size=bubble_size_col, sizes=(20, 200), alpha=0.5)
        plt.title(f"{x} vs {y} (Bubble size = {bubble_size_col})")
        plt.show()

# Histogram
def plot_histogram(df, column):
    df[column].hist(bins=50)
    plt.title(f"Distribution of {column}")
    plt.xlabel(column)
    plt.ylabel("Frequency")
    plt.show()

# Export cleaned CSV
def export_cleaned(df, output_path):
    df.to_csv(output_path, index=False)
    print(f"[✓] Exported cleaned data to {output_path}")
