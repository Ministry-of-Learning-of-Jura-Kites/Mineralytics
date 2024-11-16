import json
import pandas as pd
import source.base_api as base_api
import matplotlib.pyplot as plt

lang_column = "abstracts-retrieval-response.language.@xml:lang"


def transform(file):
    data = json.load(file)
    df = pd.json_normalize(data)
    return df.drop(columns=df.columns.difference([lang_column]))


if __name__ == "__main__":
    df = base_api.load_all_data(transform)

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
    plt.bar(
        value_counts.index.to_list(),
        value_counts.values,
    )
    plt.yscale("log", base=2)
    plt.ylabel("count")
    plt.xlabel("language")
    plt.show()
