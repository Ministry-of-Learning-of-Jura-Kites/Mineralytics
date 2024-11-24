import pandas as pd
import json
import streamlit as st
import plotly.express as px

st.title("Country Frequency Map")
uploaded_file = st.file_uploader("Choose a JSON file", type="json")

if uploaded_file is not None:
    file_contents = uploaded_file.getvalue().decode("utf-8")
    
    data = []
    for line in file_contents.splitlines():
        if line.strip():  
            data.append(json.loads(line)) 

    all_countries = []
    
    for item in data:
        if 'country' in item:
            all_countries.append(item['country'])
    
    country_counts = pd.Series(all_countries).value_counts().reset_index()
    country_counts.columns = ['country', 'Count']
    
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
        projection="natural earth"
    )
    
    fig.update_layout(
        geo=dict(
            showframe=False,
            showcoastlines=True,
            projection_type='equirectangular'
        ),
        width=900,  
        height=500   
    )

    st.plotly_chart(fig)

else:
    st.info("Please upload a JSON file to proceed.")