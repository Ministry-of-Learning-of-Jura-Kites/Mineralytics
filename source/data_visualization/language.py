import json
import pandas as pd
import base_api as base_api
from data_visualization.get_data import get_data
import matplotlib.pyplot as plt
import streamlit as st

lang_column = "lang"

def get_fig():
    series = get_data()[lang_column]
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

    value_counts = series.value_counts()
    fig, ax = plt.subplots()
    ax.bar(
        value_counts.index.to_list(),
        value_counts.values,
    )
    ax.set_yscale("log", base=2)
    ax.set_ylabel("count")
    ax.set_xlabel("language")
    return fig
