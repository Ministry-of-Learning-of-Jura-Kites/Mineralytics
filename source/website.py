from typing import Callable

import pandas as pd
import streamlit as st
import base_api as base_api
import data_visualization.language as language
import data_visualization.openaccess as openaccess
import data_visualization.city as city
import data_visualization.subtopic as subtopic
from data_visualization.get_data import get_data
st.title('Mineralytics')

if __name__=="__main__":
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
  selected_subtopic = st.selectbox(
      "Subtopic",
      get_data()["subtopic"].dropna().unique(),
      index=None,
      placeholder="Select subtopic",
  )
  subtopic_fig = subtopic.get_fig(selected_subtopic)
  st.plotly_chart(subtopic_fig)