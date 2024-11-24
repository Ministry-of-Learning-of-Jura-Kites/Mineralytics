import json
import pandas as pd
import source.base_api as base_api
import plotly.express as px

def transform(file):

    data = json.load(file)
    
    publisher_data = data["abstracts-retrieval-response"]["item"]["bibrecord"]["head"]["source"].get("publisher", {})
    publishername = publisher_data.get("publishername", None)
    coredata = data["abstracts-retrieval-response"].get("coredata", {})
    coredata_openaccess = coredata.get("openaccess", None)

    df = pd.DataFrame(
        [{
            "publishername": publishername,
            "coredata_openaccess": coredata_openaccess
        }]
    )

    return df

if __name__ == "__main__":
    
    df = base_api.load_all_data(transform)
    df['coredata_openaccess'] = pd.to_numeric(df['coredata_openaccess'], errors='coerce')
    df['openaccess'] = df['coredata_openaccess'].map({
        1: 'Open Access',
        0: 'Closed Access',
        2: 'Unknown/Hybrid',
        None: 'Unknown/Hybrid'
    })

    open_access_summary = df.groupby(['publishername', 'openaccess']).size().unstack(fill_value=0)
    open_access_summary['open_access_percentage'] = (
        open_access_summary['Open Access'] / open_access_summary.sum(axis=1) * 100
    )

    def get_range_label(value):
        ranges = list(range(0, 101, 10))
        for i in range(len(ranges)-1):
            if ranges[i] <= value < ranges[i+1]:
                return f"{ranges[i]}-{ranges[i+1]}%"
        return "90-100%"  
    
    open_access_summary = open_access_summary.reset_index()
    
    open_access_summary['percentage_range'] = open_access_summary['open_access_percentage'].apply(get_range_label)
    
    range_summary = (
        open_access_summary.groupby('percentage_range')
        .agg({
            'publishername': lambda x: ', '.join(x),
            'open_access_percentage': 'count'
        })
        .reset_index()
    )

    range_order = [f"{i}-{i+10}%" for i in range(0, 100, 10)]
    range_summary['range_order'] = pd.Categorical(range_summary['percentage_range'], categories=range_order, ordered=True)
    range_summary = range_summary.sort_values('range_order', ascending=True)
    
    fig = px.bar(
        range_summary,
        y='percentage_range',
        x='open_access_percentage',
        title="Number of Publishers by Open Access Percentage Range",
        labels={
            'open_access_percentage': 'Number of Publishers',
            'percentage_range': 'Open Access Range'
        },
        orientation='h',
    )
    
    fig.update_layout(
        xaxis=dict(
            gridwidth=1,
            gridcolor='lightgray',
            showgrid=True,
            title="Number of Publishers"
        ),
        yaxis=dict(
            title="Open Access Range",
            automargin=True,
            tickmode='linear',
            tickfont=dict(size=12),
            linecolor='black',
            linewidth=1,
            showline=True
        ),
        title_x=0.5,
        plot_bgcolor="white",
        margin=dict(l=120, r=40, t=80, b=50),
        showlegend=False,
        height=500
    )

    fig.update_yaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor='lightgray',
        showline=True,
        linewidth=1,
        linecolor='black'
    )
    
    fig.update_traces(
        texttemplate='%{x}',
        textposition='outside',
        marker_line_color='rgb(8,48,107)',
        marker_line_width=1.5
    )

    fig.update_traces(
        hovertemplate="<br>".join([
            "Range: %{y}",
            "Number of Publishers: %{x}",
            "Publishers: %{customdata[0]}"
        ]),
        customdata=range_summary[['publishername']].values
    )
    
    fig.show()