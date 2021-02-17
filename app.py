# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd


df = pd.read_csv('./data/clean_csv_data/new_bus_arrival_18051.csv')

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])

#set content of tab1
tab1_content = dbc.Card(
    dbc.CardBody(
        [
            html.P("This is tab 1!", className="card-text"),
            dbc.Button("Click here", color="success"),
        ]
    ),
    className="mt-3",
)

#set content of tab2
tab2_content = dbc.Card(
    dbc.CardBody(
        [
            html.P("This is tab 2!", className="card-text"),
            dbc.Button("Don't click here", color="danger"),
        ]
    ),
    className="mt-3",
)

#set app layour
app.layout = html.Div([

    dbc.Container(
        [
            html.H1("Hello", className="display-3"),
            html.P("Welcome to my Dashboard, my name is hululuhuhu", className="lead"),
            html.Hr(className="my-4"),

            html.Div(
                [
                    dbc.Tabs(
                        [
                            dbc.Tab(label="Tab 1", tab_id="tab-1"),
                            dbc.Tab(label="Tab 2", tab_id="tab-2")
                        ],
                        id="tabs",
                        active_tab="tab-1"
                    ),
                    html.Div(id="content")
                ]
            )
        ],
        className="jumbotron"
    )
])

@app.callback(
    Output("content", "children"),
    [Input("tabs", "active_tab")]
)
def switch_tab(at):
    if at == "tab-1":
        return tab1_content
    elif at == "tab-2":
        return tab2_content

if __name__ == '__main__':
    app.run_server(debug=True)