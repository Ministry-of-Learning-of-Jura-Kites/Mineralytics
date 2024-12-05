import json
import pandas as pd
import source.base_api as base_api
import matplotlib.pyplot as plt
import streamlit as st

# Specify the column names
lang_column = "abstracts-retrieval-response.subject-areas.subject-area.@abbrev"
value_column = "abstracts-retrieval-response.subject-areas.subject-area.$"
year_column = "abstracts-retrieval-response.item.ait:process-info.ait:date-sort.@year"


def transform(file):
    # Load the JSON data
    data = json.load(file)
    
    # Extract the subject-areas and process-info sections
    subject_areas = data["abstracts-retrieval-response"]["subject-areas"]["subject-area"]
    year_data = data["abstracts-retrieval-response"]["item"]["ait:process-info"]["ait:date-sort"]["@year"]
    
    # Normalize the subject-areas data
    df_subjects = pd.json_normalize(subject_areas)
    
    # Add the year column to the DataFrame
    df_subjects["year"] = year_data
    
    return df_subjects


def get_data():
    return base_api.load_all_data(transform)


def language():
    # Get the transformed data
    df = get_data()
    
    # Aggregate data by subject area and year
    grouped = df.groupby([lang_column, "year"])[value_column].count().reset_index()
    
    # Plot the data
    fig, ax = plt.subplots(figsize=(10, 6))
    for key, grp in grouped.groupby("year"):
        ax.bar(
            grp[lang_column],
            grp[value_column],
            label=f"Year: {key}",
        )
    ax.set_yscale("log", base=2)
    ax.set_ylabel("Count")
    ax.set_xlabel("Subject Area")
    ax.legend(title="Year")
    return fig


# Run the function to get and print the data (for debugging)
data = get_data()
print(data[[lang_column, value_column, "year"]])
