# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

dbc.Row(
                [
                    dbc.Col(html.Div([
                        html.Div("Filters", className="card-header"),
                        dcc.Dropdown(
                            id="tab1_bus_stop_no",
                            options=[
                                {'label': 'Ayer Rajah Ave (one-north Stn)', 'value': '18051'},
                                {'label': 'Ayer Rajah Ave (Opp one-north Stn)', 'value': '18059'},
                                {'label': 'Portsdown Rd (one-north Stn/Galaxis)', 'value': '18159'},
                                {'label': 'Portsdown Rd (Opp one-north Stn/Galaxis)', 'value': '18151'},
                                {'label': 'Buona Vista Flyover (Opp Ayer Rajah Ind Est)', 'value': '18121'},
                                {'label': 'Buona Vista Flyover (Ayer Rajah Ind Est)', 'value': '18129'},
                            ],
                            value="18051"
                        ),
                    )         


# dbc.Col(html.Div([
                    #     dcc.Dropdown(id="tab1_bus_no", style={"margin-top":30}),
                    # ])

                    


                    # dbc.Col(html.Div([
                    #     html.Div("Bus Load Count on a Daily Basis", className="card-header"),
                    #     html.Div([
                    #         html.P("SEA - Seats Available | SDA - Standing Available | LSD - Limited Standing", className="card-text"),
                    #         dcc.Graph(id="tab1_bus_graph")], className="card-body")
                    #         ],
                    #     className="card border-primary mb-3"
                    # ),
                    # width=9
                    # ),
                    # ],
                    # className="form-group"),
                    # width=3,
                    # className="card border-primary mb-3",
                    # style={"textAlign":"center"}
                    # )
                    
            ),
            dbc.Row(
                [
                    dbc.Col(html.Div([
                        html.Div("Shuttle Bus Dispatch Count on a Daily Basis | To be received", className="card-header"),
                        html.Div([dcc.Graph(figure=shutfig)], className="card-body")],
                        className="card border-primary mb-3"
                    ),
                    width=12
                    )
                ]
            )




























import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime
import os

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
app.config.suppress_callback_exceptions = True

#dummy graph for shuttle bus
df = pd.read_csv('./data/bus_data/new_bus_arrival_18121_14.csv')
df["date"] = pd.to_datetime(df["date"], format="%d/%m/%Y")
df = df.groupby(["date", "first_next_bus_load"], as_index=False).size()
shutfig = px.bar(df, x=df["date"], y=df["size"], color=df["first_next_bus_load"], barmode="group")

#set content of tab1
tab1_content = dbc.Card(
    dbc.CardBody(
        [
            dbc.Row(
                [
                    dbc.Col(html.Div([
                        html.Div("Bus Load Count on a Daily Basis", className="card-header"),
                        html.Div([
                            html.P("SEA - Seats Available | SDA - Standing Available | LSD - Limited Standing", className="card-text"),
                            dcc.Graph(id="tab1_bus_graph")], className="card-body")
                            ],
                        className="card border-primary mb-3"
                    ),
                    width=9
                    ),

                    dbc.Col(html.Div([
                        html.Div("Filters", className="card-header"),
                        dcc.Dropdown(id="bus_stop_no", options=[{"label": filename, "value": filename} for filename in os.listdir("./data/clean_csv_data/")], value=os.listdir("./data/clean_csv_data/")[0], style={"margin-top":30}),
                        dcc.Dropdown(id="bus_no", style={"margin-top":30}),
                        #dcc.RadioItems(id="period", options=)
                    ],
                    className="form-group"),
                    width=3,
                    className="card border-primary mb-3",
                    style={"textAlign":"center"}
                    )
                ]
            ),

            dbc.Row(
                [
                    dbc.Col(html.Div([
                        html.Div("Shuttle Bus Dispatch Count on a Daily Basis", className="card-header"),
                        html.Div([dcc.Graph(id="tab1_shutbus_graph")], className="card-body")],
                        className="card border-primary mb-3"
                    ),
                    width=12
                    )
                ]
            )
        ]
    ),
    className="mt-3"
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

tab3_content = dbc.Card(
    dbc.CardBody(
        [
            html.P("This is tab 3!", className="card-text"),
            dbc.Button("Don't click here", color="danger"),
        ]
    ),
    className="mt-3",
)

tab4_content = dbc.Card(
    dbc.CardBody(
        [
            html.P("This is tab 4!", className="card-text"),
            dbc.Button("Don't click here", color="danger"),
        ]
    ),
    className="mt-3",
)

#set app layour
app.layout = html.Div([

    dbc.Container(
        [
            html.H3("Transport Efficiency at One-North", className="display-3"),
            html.P("On this dashboard, we will ", className="lead"),
            html.Hr(className="my-4"),

            html.Div(
                [
                    dbc.Tabs(
                        [
                            dbc.Tab(label="Sufficiency", tab_id="tab-1"),
                            dbc.Tab(label="Punctuality", tab_id="tab-2"),
                            dbc.Tab(label="GIS Visualisation", tab_id="tab-3"),
                            dbc.Tab(label="Threshold & Sentiments", tab_id="tab-4")
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
    elif at == "tab-3":
        return tab3_content
    elif at == "tab-4":
        return tab4_content

@app.callback(
    Output("bus_no", "options"),
    Output("bus_no", "value"),
    Input("bus_stop_no", "value")
)
def select_bus_stop(bus_stop_no):
    df = pd.read_csv(f"./data/clean_csv_data/{bus_stop_no}")
    all_buses = df["bus_number"].unique()
    options = [{"label": bus_no, "value": bus_no} for bus_no in all_buses]
    value = all_buses[0]

    return options, value

@app.callback(
    Output("tab1_bus_graph", "figure"),
    Input("bus_stop_no", "value"),
    Input("bus_no", "value")
)
def select_bus_no(bus_stop_no, bus_no):
    df = pd.read_csv(f"./data/clean_csv_data/{bus_stop_no}")
    df = df[df["bus_number"]==bus_no]
    df["date"] = pd.to_datetime(df["date"], format="%d/%m/%Y")
    df = df.groupby(["date", "first_next_bus_load"], as_index=False).size()
    fig1 = px.bar(df, x=df["date"], y=df["size"], color=df["first_next_bus_load"], barmode="group")

    return fig1


if __name__ == '__main__':
    app.run_server(debug=True)