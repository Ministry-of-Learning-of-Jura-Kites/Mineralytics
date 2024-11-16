import source.base_api as base_api
import pandas as pd
import json
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse import triu
import pickle


def transform(file):
    data = json.load(file)
    if isinstance(
        data["abstracts-retrieval-response"]["item"]["bibrecord"]["head"][
            "author-group"
        ],
        list,
    ):
        for elem in data["abstracts-retrieval-response"]["item"]["bibrecord"]["head"][
            "author-group"
        ]:
            if "author" not in elem:
                elem["author"] = None
    else:
        elem = data["abstracts-retrieval-response"]["item"]["bibrecord"]["head"][
            "author-group"
        ]
        if "author" not in elem:
            elem["author"] = None
    df = pd.json_normalize(
        data,
        [
            "abstracts-retrieval-response",
            "item",
            "bibrecord",
            "head",
            "author-group",
            "author",
        ],
        [["abstracts-retrieval-response", "coredata"]],
        errors="ignore",
    )
    df["abstracts-retrieval-response.coredata"] = df[
        "abstracts-retrieval-response.coredata"
    ].apply(lambda row: row["eid"])
    df = df.rename(
        columns={
            "preferred-name.ce:indexed-name": "indexed-name",
            "abstracts-retrieval-response.coredata": "eid",
        }
    )
    df = df.drop(columns=df.columns.difference(["indexed-name", "eid"]))
    return df


if __name__ == "__main__":
    df = base_api.load_all_data(
        transform,
    )

    # df = base_api.load_data_of_year(
    #     2018,
    #     transform,
    #     100,
    # )

    # with open(
    #     base_api.relative_to_abs(["data", "2018", "201800000"]), "r", encoding="utf-8"
    # ) as file:
    #     df = transform(file)

    df = df.drop_duplicates()
    df = df[
        df["indexed-name"].isin(df["indexed-name"].value_counts().nlargest(20).index)
    ]

    df = pd.get_dummies(
        df, prefix="", prefix_sep="", columns=["indexed-name"], drop_first=True
    ).set_index("eid")
    df = df.groupby("eid").agg(lambda series: series.any())
    adj = df.T @ df
    np.fill_diagonal(adj.values, 0)

    adj_sparse = csr_matrix(adj.values)

    G = nx.from_scipy_sparse_array(triu(adj_sparse))
    G = nx.from_pandas_adjacency(adj)
    d = dict(G.degree)
    the_base_size = 100
    nx.draw(
        G,
        with_labels=True,
        node_size=[len(v) ** 1.5 * the_base_size for v in G.nodes()],
        font_size=5,
    )

    plt.show()

    pickle.dump(
        G, open(base_api.relative_to_abs(["archrive", "coauther.pickle"]), "wb")
    )
