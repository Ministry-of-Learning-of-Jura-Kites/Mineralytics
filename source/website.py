from typing import Callable

import pandas as pd
import streamlit as st
import base_api as base_api
import data_visualization.language as language
st.title('Mineralytics')

if __name__=="__main__":
  @st.cache_data
  def load_all_data(transform: Callable[[str], pd.DataFrame]):
    return base_api.load_all_data(transform=transform)

  st.text("langauage")
  language_fig = language.language()
  st.pyplot(language_fig)