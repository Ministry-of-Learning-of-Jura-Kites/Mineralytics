import json
import faiss
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
import torch
from source import base_api


def transform(file_content: str, relative_file_path: str):
    # relative_file_path should look like ["data","2021/201204202"]
    
    data = json.load(file_content)

    abstracts = data["abstracts-retrieval-response"]["item"]["bibrecord"]["head"][
        "abstracts"
    ]

    return (
        pd.DataFrame({"abstracts": [abstracts], "file_path": relative_file_path[1]})
        if abstracts != None
        else None
    )


def get_data():
    data = base_api.load_all_data(transform)

    # data = base_api.load_data_of_year(2018, transform, 10)

    return data


def model_training():
    df = get_data()
    model = SentenceTransformer("all-MiniLM-L6-v2")
    df["abstracts"].dropna(inplace=True)
    embeddings = model.encode(df["abstracts"].tolist(),show_progress_bar=True, convert_to_tensor=True)
    df = df.drop("abstracts", axis="columns")

    torch.save(embeddings, base_api.relative_to_abs(["data", "embeddings"]))
    # np.save(base_api.relative_to_abs(["data", "embeddings"]),embeddings)
    with open(base_api.relative_to_abs(["data", "file_index.json"]), "w") as f:
        f.write(json.dumps(df["file_path"].to_list()))


model_training()
