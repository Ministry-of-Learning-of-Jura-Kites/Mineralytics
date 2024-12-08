from typing import Callable

import pandas as pd
import streamlit as st
import base_api as base_api
import data_visualization.language as language
import data_visualization.openaccess as openaccess
import data_visualization.city as city
import data_visualization.subtopic as subtopic
from data_visualization.get_data import get_data
import os
import pickle
import glob

st.title('Mineralytics')

def get_trained_subtopics(path_to_models):
    absolute_path = base_api.relative_to_abs(path_to_models)
    pkl_files = glob.glob(os.path.join(absolute_path, "Subtopic_*.pkl"))
    trained_subtopics = [os.path.splitext(os.path.basename(f))[0].split("_")[1] for f in pkl_files]
    return trained_subtopics


def load_pickle(path_to_pickle , file_name) :
  absolute_path = base_api.relative_to_abs(path_to_pickle)
  if file_name.endswith('.pkl'):
      file_path = os.path.join(absolute_path, file_name)
      try:
          with open(file_path, 'rb') as file:
              load_object = pickle.load(file)
          return load_object
      except FileNotFoundError:
            return None 
  return None
  

if __name__=="__main__":
  data = get_data()
  
  st.header("langauage")
  language_fig = language.get_fig()
  st.pyplot(language_fig)

  st.header("open access")
  openaccess_fig = openaccess.get_fig()
  st.plotly_chart(openaccess_fig)
  
  st.header("city")
  affiliation_fig = city.get_fig()
  st.plotly_chart(affiliation_fig)  
  
  st.header("subtopic")
  subtopic_list = data["subtopic"].dropna().unique().tolist()
  trained_subtopics = get_trained_subtopics(["source", "machine_learning", "model", "subtopic"])
  sorted_subtopics = sorted(
        subtopic_list,
        key=lambda x: (
            -1 if data.loc[data["subtopic"] == x, "subtopic_code"].values[0] in trained_subtopics else 1
        )
    )
  selected_subtopic = st.selectbox(
    "Subtopic",
    ["-- Select subtopic --"] + sorted_subtopics,
    placeholder="Select subtopic",
)
  if selected_subtopic and selected_subtopic != "-- Select subtopic --":
    subtopic_code = data.loc[data["subtopic"] == selected_subtopic, "subtopic_code"].values[0]
    choose = "Subtopic_" + subtopic_code + ".pkl"
    model = load_pickle(
            ["source", "machine_learning", "model", "subtopic"],
            choose
        )
        
    if model:  
        subtopic_fig = subtopic.get_fig(selected_subtopic, model)
        st.plotly_chart(subtopic_fig)
    else:
        subtopic_fig = subtopic.get_fig(selected_subtopic)
        st.plotly_chart(subtopic_fig)
    