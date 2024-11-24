import json
import pandas as pd
import source.base_api as base_api

def transform(file):
    data = json.load(file)
    affiliation_data = data["abstracts-retrieval-response"]["affiliation"]
    
    df = pd.json_normalize(affiliation_data)
    
    df = df[["affiliation-city", "affilname", "affiliation-country"]]
    df = df.rename(columns={
        "affiliation-city": "city",
        "affilname": "institution_name",
        "affiliation-country": "country"
    })
    
    return df  

if __name__ == "__main__":
    
    df = base_api.load_all_data(transform)
    
    if isinstance(df, list):
        df = pd.concat(df, ignore_index=True)

    df.to_json("affiliation.json", orient="records", lines=True)
