from data_visualization.get_data import get_data
import plotly.express as px


def get_fig(subtopic: str):
    data = get_data()[["subtopic","subtopic_code"]]

    subject_code = data[data["subtoppic"]==subtopic]["subtopic_code"].iloc[0]

    subject_code
  
    # fig = px.bar(data,"year","count_subtopic",labels={
    #   "year":"Year",
    #   "count_subtopic":"Count of {}".format(subtopic)
    # })

    return fig
