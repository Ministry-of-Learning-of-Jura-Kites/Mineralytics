import pandas as pd
import json
import streamlit as st
import base_api as base_api


def transform(file):
    data = json.load(file)

    # lang
    lang_df = None
    if data["abstracts-retrieval-response"]["language"] != None:
        lang_df = pd.DataFrame(
            {
                "lang": pd.Series(
                    data["abstracts-retrieval-response"]["language"]["@xml:lang"]
                )
            }
        )

    # open access
    publisher_data = data["abstracts-retrieval-response"]["item"]["bibrecord"]["head"][
        "source"
    ].get("publisher", {})
    publishername = publisher_data.get("publishername", None)
    coredata = data["abstracts-retrieval-response"].get("coredata", {})
    coredata_openaccess = coredata.get("openaccess", None)

    openaccess_df = pd.DataFrame(
        [{"publishername": publishername, "coredata_openaccess": coredata_openaccess}]
    )

    # city
    affiliation_data = data["abstracts-retrieval-response"]["affiliation"]

    city_df = pd.json_normalize(affiliation_data)

    city_df = city_df[["affiliation-city", "affilname", "affiliation-country"]]
    city_df = city_df.rename(
        columns={
            "affiliation-city": "city",
            "affilname": "institution_name",
            "affiliation-country": "country",
        }
    )

    subject_areas = data["abstracts-retrieval-response"]["subject-areas"][
        "subject-area"
    ]
    year_data = data["abstracts-retrieval-response"]["item"]["ait:process-info"][
        "ait:date-sort"
    ]["@year"]
    subjects_df = pd.json_normalize(subject_areas)

    subjects_df["year"] = year_data

    subjects_df = subjects_df.rename(
        {"$": "subtopic", "@abbrev": "subject", "@code": "subtopic_code"},
        axis="columns",
    )

    return pd.concat([lang_df, city_df, openaccess_df, subjects_df])


@st.cache_data
def get_data():
    return base_api.load_all_data(transform)
