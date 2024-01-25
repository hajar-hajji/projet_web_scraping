import pandas as pd
from utils.utils import *
from utils.nlp import *

df_cobalt_mine = pd.read_csv(get_data_path("cobalt_mine_comments_reddit.csv"))
df_cobalt_mine = df_cobalt_mine.drop_duplicates(subset=['Comment'])
# print(df_cobalt_mine.info())

df_nickel_mine = pd.read_csv(get_data_path("nickel_mine_comments_reddit.csv"))
df_nickel_mine = df_nickel_mine.drop_duplicates(subset=['Comment'])
# print(df_nickel_mine.info())

df_manganese_mine = pd.read_csv(get_data_path("manganese_mine_comments_reddit.csv"))
df_manganese_mine = df_manganese_mine.drop_duplicates(subset=['Comment'])
# print(df_manganese_mine.info())

def simplified_reputational_risk(df, sentiment_col):
    df[sentiment_col] = df[sentiment_col].astype(str)
    # Count the number of tweets with negative sentiment
    negative_tweets = df[df[sentiment_col] == 'Negative'].shape[0]
    # Calculate the Reputation Risk
    total_tweets = df.shape[0]
    reputational_risk = (negative_tweets / total_tweets) * 100
    return reputational_risk

def weighted_reputational_risk(df, sentiment_col, weights_col):
    # Count the number of tweets with negative sentiment, weighted by upvotes
    negative_weighted_tweets = (df[df[sentiment_col] == 'Negative'][weights_col]).sum()
    # Calculate the total sum of weights
    total_weights = df[weights_col].abs().sum()
    if total_weights != 0:
        reputational_risk = (negative_weighted_tweets / total_weights) * 100
    else:
        reputational_risk = 0
    return reputational_risk

def sophisticated_risk_reputation(df, polarity_score, weights_col):
    # Calculate the weighted sum of sentiment scores and the sum of weights (i.e likes, upvotes, etc)
    weighted_sum_sentiment = (df[polarity_score] * df[weights_col]).sum()
    sum_of_weights = df[weights_col].abs().sum()
    if sum_of_weights != 0:
        sophisticated_risk_reputation = (weighted_sum_sentiment / sum_of_weights) * 100
    else:
        sophisticated_risk_reputation = 0
    return sophisticated_risk_reputation

print(simplified_reputational_risk(df_cobalt_mine, "Sentiment"))
print(weighted_reputational_risk(df_cobalt_mine, "Sentiment", "Upvotes"))
print(sophisticated_risk_reputation(df_cobalt_mine, "Vader Polarity Score", "Upvotes"))
print(sophisticated_risk_reputation(df_cobalt_mine, "Blob Polarity Score", "Upvotes"))
print()
print(simplified_reputational_risk(df_nickel_mine, "Sentiment"))
print(weighted_reputational_risk(df_nickel_mine, "Sentiment", "Upvotes"))
print(sophisticated_risk_reputation(df_nickel_mine, "Vader Polarity Score", "Upvotes"))
print(sophisticated_risk_reputation(df_nickel_mine, "Blob Polarity Score", "Upvotes"))
print()
print(simplified_reputational_risk(df_manganese_mine, "Sentiment"))
print(weighted_reputational_risk(df_manganese_mine, "Sentiment", "Upvotes"))
print(sophisticated_risk_reputation(df_manganese_mine, "Vader Polarity Score", "Upvotes"))
print(sophisticated_risk_reputation(df_manganese_mine, "Blob Polarity Score", "Upvotes"))