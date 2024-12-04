import json
import pandas as pd
import base_api as base_api
import matplotlib.pyplot as plt
import streamlit as st

lang_column = "abstracts-retrieval-response.language.@xml:lang"


def transform(file):
    data = json.load(file)
    df = pd.json_normalize(data)
    return df.drop(columns=df.columns.difference([lang_column]))


# if __name__ == "__main__":
@st.cache_data
def get_data():
    return base_api.load_all_data(transform)


def language():
    df = get_data()
    # for testing
    # df = base_api.load_data_of_year(
    #     2018,
    #     lambda df: df.drop(
    #         columns=df.columns.difference(
    #             ["abstracts-retrieval-response.language.@xml:lang"]
    #         )
    #     ),
    #     100,
    # )

    value_counts = df[lang_column].value_counts()
    fig, ax = plt.subplots()
    ax.bar(
        value_counts.index.to_list(),
        value_counts.values,
    )
    ax.set_yscale("log", base=2)
    ax.set_ylabel("count")
    ax.set_xlabel("language")
    return fig
