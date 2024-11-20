import json
import pandas as pd 
import source.base_api as base_api
lang_column = "abstracts-retrieval-response.language.@xml:lang"
def transform(file) :
    data = json.load(file)
    df = pd.json_normalize(data)
    print(df.columns)
    return df.drop(columns=df.columns.difference([lang_column]))


if __name__ == "__main__":
    df = base_api.load_all_data(transform)
    print(df)