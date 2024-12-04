import source.base_api as base_api
import pandas as pd
import json
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse import triu


def transform(file):
    data = json.load(file)
    departments, facultys, universitys = [], [], []
    organizations = []
    author_groups = data["abstracts-retrieval-response"]["item"]["bibrecord"]["head"][
            "author-group"
        ]
    if isinstance(
        author_groups,
        list,
    ):
        for author_group in author_groups:
            if not "affiliation" in author_group:
              continue
            organization = author_group["affiliation"]["organization"]
            if isinstance(
                organization,
                list,
            ):
                organization = list(map(lambda x: x["$"], organization))
            else:
                organization = [organization["$"]]
            organizations.append(organization)
    # else:
    df = pd.DataFrame({"organization": organizations})

    return df


if __name__ == "__main__":
    # df = base_api.load_all_data(
    #     transform,
    # )

    df = base_api.load_data_of_year(
        2018,
        transform,
        2,
    )

    # with open(
    #     base_api.relative_to_abs(["data", "2018", "201800000"]), "r", encoding="utf-8"
    # ) as file:
    #     df = transform(file)

    print(df)

    # df = df.drop_duplicates()
    # df = df[
    #     df["indexed-name"].isin(df["indexed-name"].value_counts().nlargest(20).index)
    # ]

    # df = pd.get_dummies(
    #     df, prefix="", prefix_sep="", columns=["indexed-name"], drop_first=True
    # ).set_index("eid")
    # df = df.groupby("eid").agg(lambda series: series.any())
    # adj = df.T @ df
    # np.fill_diagonal(adj.values, 0)

    # adj_sparse = csr_matrix(adj.values)

    # G = nx.from_scipy_sparse_array(triu(adj_sparse))
    # G = nx.from_pandas_adjacency(adj)
    # d = dict(G.degree)
    # the_base_size = 100
    # nx.draw(
    #     G,
    #     with_labels=True,
    #     node_size=[len(v) ** 1.5 * the_base_size for v in G.nodes()],
    #     font_size=5,
    # )

    plt.show()
