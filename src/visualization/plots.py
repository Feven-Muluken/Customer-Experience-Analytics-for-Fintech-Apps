import matplotlib.pyplot as plt # pyright: ignore[reportMissingModuleSource]
import seaborn as sns # pyright: ignore[reportMissingModuleSource]

# Sentiment distribution per bank
sns.boxplot(x='bank', y='vader_compound', data=df)
plt.title("Sentiment Distribution per Bank")
plt.show()

# Rating distribution
sns.countplot(x='rating', hue='bank', data=df)
plt.title("Rating Distribution per Bank")
plt.show()

# Keyword cloud (optional)
from wordcloud import WordCloud
text = " ".join(df['review'].dropna())
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()
