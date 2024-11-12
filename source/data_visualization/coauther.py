
from source.base_api import base_api

df = base_api.load_data_of_year(
    2018,
    lambda df: df.drop(
        columns=df.columns.difference(
            ["bibrecord.head.author-group"]
        )
    ),
    max=1,
)
print(df)