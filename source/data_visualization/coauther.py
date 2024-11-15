import source.base_api as base_api
import pandas as pd
import json

def transform(file):
    data = json.load(file)
    # for elem in data['abstracts-retrieval-response']['item']['bibrecord']['head']:
    #   if len(elem['author-group'])==0:
    #     elem.update({'author-group':{'author':None}})
    if isinstance(data['abstracts-retrieval-response']['item']['bibrecord']['head']['author-group'],list):
      for elem in data['abstracts-retrieval-response']['item']['bibrecord']['head']['author-group']:
        if 'author' not in elem:
          elem['author']=None
    else:
      elem = data['abstracts-retrieval-response']['item']['bibrecord']['head']['author-group']
      if 'author' not in elem:
          elem['author']=None
    df = pd.json_normalize(data,['abstracts-retrieval-response','item','bibrecord','head','author-group','author'],errors="ignore")
    df= df.drop(
        columns=df.columns.difference(
            ["preferred-name.ce:indexed-name"]
        )
    )
    return df

df = base_api.load_data_of_year(
    2018,
    transform,
    max=1000,
)
# with open(base_api.relative_to_abs(["data","2018","201800259"]), "r", encoding="utf-8") as file:
#   df = transform(file)
print(df['preferred-name.ce:indexed-name'])
