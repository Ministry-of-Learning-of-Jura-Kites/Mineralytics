import json
import pandas as pd
import source.base_api as base_api
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
from nltk.stem import WordNetLemmatizer
import nltk
import enchant

abstract_column = "abstracts-retrieval-response.item.bibrecord.head.abstracts"
nltk.download('wordnet')

def transform(file):
    data = json.load(file)
    df = pd.json_normalize(data)
    return df.drop(columns=df.columns.difference([abstract_column]))


if __name__ == "__main__":
    df = base_api.load_all_data(transform)

    # # for testing
    # df = base_api.load_data_of_year(
    #     2018,
    #     transform,
    #     100,
    # )

    def to_words(data):
        return data.split(" ")

    df.dropna(inplace=True)
    df.reset_index(drop=True, inplace=True)
    df[abstract_column] = df[abstract_column].apply(to_words)
 
    df = df[abstract_column].explode()
    
    lemmatizer = WordNetLemmatizer()
    df = df.apply(lambda word: lemmatizer.lemmatize(word))
    # df = df.apply(lambda word: word.lower())
    d = enchant.Dict("en_US")
    df = df[df.apply(d.check)]
    stopwords = set(STOPWORDS)
    wordcloud = WordCloud(
        stopwords=stopwords, collocations=False, background_color="white"
    ).generate_from_frequencies(
        {
            word: frequency
            for word, frequency in zip(df, df.value_counts())
            if word not in stopwords
        }
    )

    plt.imshow(wordcloud, interpolation="bilinear")
    plt.show(block=False)
    input()
    plt.close("all")
    # print(df.loc[1].value_counts())
