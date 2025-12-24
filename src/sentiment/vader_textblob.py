import pandas as pd # pyright: ignore[reportMissingModuleSource]
from nltk.sentiment.vader import SentimentIntensityAnalyzer # pyright: ignore[reportMissingImports]
from textblob import TextBlob # pyright: ignore[reportMissingImports]
import nltk # pyright: ignore[reportMissingImports]


# download vader lexican (only first time)
nltk.download('vader_lexicon')

# load dataset
df=pd.read_csv('data/processed/all_reviews_clean.csv')

# apply vader sentiment

vader_sentiment=SentimentIntensityAnalyzer()
def vader_sentiment_scores(text):
    scores=vader_sentiment.polarity_scores(str(text))
    return pd.Series({
        "vader_neg":scores['neg'],
        "vader_neu":scores['neu'],
        "vader_pos":scores['pos'],
        "vader_compound":scores['compound']
    })
df = df.join(df['review'].apply(vader_sentiment_scores))

def textblob_sentiment(text):
    blob=TextBlob(str(text))
    return pd.Series({
        "tb_polarity":blob.sentiment.polarity,
        "tb_subjectivity":blob.sentiment.subjectivity
    })
df=df.join(df['review'].apply(textblob_sentiment))

agg = df.groupby(["bank", "rating"]).agg({
    "vader_neg": "mean",
    "vader_neu": "mean",
    "vader_pos": "mean",
    "vader_compound": "mean",
    "tb_polarity": "mean",
    "tb_subjectivity": "mean"
}).reset_index()
print(agg)

# Save outputs
df.to_csv("data/processed/reviews_with_sentiment.csv", index=False)
agg.to_csv("data/processed/sentiment_summary.csv", index=False)

print("\nSaved detailed sentiment → data/processed/reviews_with_sentiment.csv")
print("Saved aggregated bank sentiment → data/processed/sentiment_summary.csv")


