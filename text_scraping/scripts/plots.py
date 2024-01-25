import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from utils.utils import *

df_cobalt_mine = pd.read_csv(get_data_path("cobalt_mine_comments_reddit.csv"))
df_cobalt_mine = df_cobalt_mine.drop_duplicates(subset=['Comment'])

df_nickel_mine = pd.read_csv(get_data_path("nickel_mine_comments_reddit.csv"))
df_nickel_mine = df_nickel_mine.drop_duplicates(subset=['Comment'])

df_manganese_mine = pd.read_csv(get_data_path("manganese_mine_comments_reddit.csv"))
df_manganese_mine = df_manganese_mine.drop_duplicates(subset=['Comment'])

def plot_distribution(df, column_):
    """
    Plot the polarity score
    """
    df[column_] = pd.to_numeric(df[column_], errors='coerce')
    plt.figure(figsize=(8, 6))
    sns.histplot(df[column_].dropna(), bins=20, kde=True)
    plt.title(f'Distribution of {column_}')
    plt.xlabel(column_)
    plt.ylabel('Frequency')
    plt.show()

def plot_sentiment(df, col_, plot_title="Class Distribution"):
    """
    Plot the distribution of classes
    """
    counts = df[col_].value_counts()
    # plt.bar(counts.index, counts.values)
    sns.barplot(x=counts.index, y=counts.values, width=0.4, alpha=0.4)
    plt.xlabel('Classes')
    plt.ylabel('Number of Occurrences')
    plt.title(plot_title)
    plt.show()

def plot_sentiment_ts(df, date_col, score_col):
    """
    Plot polarity score over time
    """
    df[date_col] = pd.to_datetime(df[date_col])
    plt.figure(figsize=(12, 6))
    sns.lineplot(x=date_col, y=score_col, data=df)
    plt.title(f'{score_col} over time')
    plt.xlabel('Date')
    plt.ylabel(f'{score_col}')
    plt.show()

plot_distribution(df_cobalt_mine, "Vader Polarity Score")
plot_distribution(df_cobalt_mine, "Blob Polarity Score")
plot_sentiment(df_cobalt_mine, "Sentiment")
plot_sentiment_ts(df_cobalt_mine, "Publication Date", "Vader Polarity Score")
plot_sentiment_ts(df_cobalt_mine, "Publication Date", "Blob Polarity Score")