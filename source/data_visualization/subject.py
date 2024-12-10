import pandas as pd
from data_visualization.get_data import get_data
import plotly.express as px


def get_fig(subject: str, model=None):
    data = get_data()[["subject", "year"]]

    data = data[data["subject"] == subject]
    data = (
        data[data.columns]
        .groupby(data.columns.tolist())
        .size()
        .reset_index(name="count_subject")
        .sort_values(by="year", ascending=True)
    )
    data.dropna(subset="year", inplace=True)
    if model:

        predicted_data = pd.DataFrame(
            {
                "subject": [subject, subject],
                "year": [2024, 2025],
                "count_subject": [
                    model.predict([[2024]])[0],
                    model.predict([[2025]])[0],
                ],
            }
        )
        data = pd.concat([data, predicted_data])
    # create bar
    fig = px.bar(
        data,
        "year",
        "count_subject",
        labels={"year": "Year", "count_subject": "Count of {}".format(subject)},
    )
    fig.update_traces(
        marker_color=data["year"].apply(
            lambda x: "green" if x in [2024, 2025] else "blue"
        )
    )
    return fig
