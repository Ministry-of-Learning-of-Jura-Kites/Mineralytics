import pandas as pd
from data_visualization.get_data import get_data
import plotly.express as px


def get_fig(subtopic: str , model=None):
    data = get_data()[["subtopic","year"]]

    data = data[data["subtopic"] == subtopic]
    data = (
        data[data.columns]
        .groupby(data.columns.tolist())
        .size()
        .reset_index(name="count_subtopic")
        .sort_values(by="year", ascending=True)
    )
    data.dropna(subset="year", inplace=True)
    if model :
      
      predicted_data = pd.DataFrame({
          "subtopic": [subtopic, subtopic],
          "year": [2024, 2025],
          "count_subtopic": [
          model.predict([[2024]])[0],
          model.predict([[2025]])[0], 
          ],
      })
      data = pd.concat([data, predicted_data])
    #create bar
    fig = px.bar(data,"year","count_subtopic",labels={
      "year":"Year",
      "count_subtopic":"Count of {}".format(subtopic)
    })
    fig.update_traces(marker_color=data['year'].apply(lambda x: 'green' if x in [2024, 2025] else 'blue'))
    return fig
