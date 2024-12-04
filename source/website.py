from typing import Callable

import pandas as pd
import streamlit as st
import base_api as base_api
import data_visualization.language as language
import data_visualization.openaccess as openaccess
import data_visualization.city as city
st.title('Mineralytics')

if __name__=="__main__":
  @st.cache_data
  def load_all_data(transform: Callable[[str], pd.DataFrame]):
    return base_api.load_all_data(transform=transform)

  st.header("langauage")
  language_fig = language.get_fig()
  st.pyplot(language_fig)

  st.header("open access")
  openaccess_fig = openaccess.get_fig()
  st.plotly_chart(openaccess_fig)
  
  st.header("city")
  affiliation_fig = city.get_fig()
  st.plotly_chart(affiliation_fig)