from data_visualization.get_data import get_data
import plotly.express as px


def get_fig(subtopic: str):
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

    fig = px.bar(data,"year","count_subtopic",labels={
      "year":"Year",
      "count_subtopic":"Count of {}".format(subtopic)
    })

    return fig
