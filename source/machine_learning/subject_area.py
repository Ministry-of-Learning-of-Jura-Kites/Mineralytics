import json
import pickle
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error , r2_score
from sklearn.model_selection import train_test_split
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
        # print(year_data)
        # Normalize the subject-areas data
        df_subjects = pd.json_normalize(subject_areas)
        
        # Add the year column to the DataFrame
        df_subjects["year"] = year_data
        
        return df_subjects


def get_data():
    data = base_api.load_all_data(transform)
    filter_data = data[['$', '@abbrev', 'year']].groupby(['$', '@abbrev', 'year']).size().reset_index(name='count').sort_values(by='year' , ascending=True)

    filter_data.dropna(subset='year' , inplace=True)
    return pd.get_dummies(filter_data ,columns=['@abbrev' , '$'])


if __name__ == '__main__' : 
    get_data()
    
    

    
        
