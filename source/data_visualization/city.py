import pandas as pd
import json
import streamlit as st
import plotly.express as px
import json
import pandas as pd
import base_api as base_api
from data_visualization.get_data import get_data


# def transform(file):
#     data = json.load(file)
#     affiliation_data = data["abstracts-retrieval-response"]["affiliation"]

#     df = pd.json_normalize(affiliation_data)

#     df = df[["affiliation-city", "affilname", "affiliation-country"]]
#     df = df.rename(
#         columns={
#             "affiliation-city": "city",
#             "affilname": "institution_name",
#             "affiliation-country": "country",
#         }
#     )

#     return df


# @st.cache_data
# def get_data():
#     return base_api.load_all_data(transform)


def get_fig():
    df = get_data()
    if isinstance(df, list):
        df = pd.concat(df, ignore_index=True)

    country_counts = df["country"].value_counts().reset_index()
    country_counts.columns = ["country", "Count"]

    st.subheader("Country Frequency Data")
    st.dataframe(country_counts)
    st.subheader("Country Frequency Heat Map")
    fig = px.choropleth(
        country_counts,
        locations="country",
        locationmode="country names",
        color="Count",
        hover_name="country",
        color_continuous_scale=["rgba(255,0,0,0.1)", "rgba(255,0,0,1)"],
        title="Country Frequency Visualization",
        projection="natural earth",
    )

    fig.update_layout(
        geo=dict(
            showframe=False, showcoastlines=True, projection_type="equirectangular"
        ),
        width=900,
        height=500,
    )

    return fig
