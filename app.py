# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])

# filepath = "./data/bus_data/new_bus_arrival_"

# Graph 1 Bar Chart of Bus Loads vs Size
df = pd.read_csv('./data/bus_data/new_bus_arrival_18121_14.csv')
df["date"] = pd.to_datetime(df["date"], format="%d/%m/%Y")

load_df = df.groupby(["date", "first_next_bus_load"], as_index=False).size()
fig1 = px.bar(load_df, x=load_df["date"], y=load_df["size"], color=load_df["first_next_bus_load"], barmode="group")

# Graph 2 S
load_df2 = df.groupby(["date", "Late_By"], as_index=False).size()
fig2 = px.bar(load_df2, x=load_df2["date"], y=load_df2["size"], color=load_df2["Late_By"], barmode="group")

# Graph 3 Taxi Availability
df_taxi = pd.read_csv('./data/taxi_data/relevant_taxi_availability.csv')
df_taxi["date"] = pd.to_datetime(df["date"], format="%d/%m/%Y")

load_df_taxi = df_taxi.groupby(["date", "count"], as_index=False).size()
fig3 = px.bar(load_df_taxi, x=load_df_taxi["date"], y=load_df_taxi["size"], color=load_df_taxi["count"], barmode="group")

#set content of tab1
tab1_content = dbc.Card(
    dbc.CardBody(
        [
            dbc.Row(
                [
                    #dbc.Col(html.Div("First column")),
                    #dbc.Col(html.Div("Second column")),
                    #dbc.Col(html.Div("Third column"))
                    dbc.Col(html.Div(
                        [
                            html.Div("Bus Load Count on a Daily Basis", className="card-header"),

                            html.Div(
                                [
                                    html.P("SEA - Seats Available | SDA - Standing Available | LSD - Limited Standing", className="card-text"),
                                    dcc.Graph(figure=fig1)
                                ],
                                className="card-body"
                            ),
                        ],
                        className="card border-primary mb-3"
                    ))
                ]
            ),

            dbc.Row(
                [
                    #dbc.Col(html.Div("First column")),
                    #dbc.Col(html.Div("Second column")),
                    #dbc.Col(html.Div("Third column"))
                    dbc.Col(html.Div(
                        [
                            html.Div("Shuttle Bus Dispatch Count on a Daily Basis", className="card-header"),
                            html.Div(
                                [
                                    # html.P("", className="card-text"),
                                    dcc.Graph(figure=fig1)
                                ],
                                className="card-body"
                            ),
                        ],
                        className="card border-primary mb-3"
                    )),
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
            dbc.Row(
                [
                    #dbc.Col(html.Div("First column")),
                    #dbc.Col(html.Div("Second column")),
                    #dbc.Col(html.Div("Third column"))
                    dbc.Col(html.Div(
                        [
                            html.Div("Bus Late Count on a Daily Basis", className="card-header"),
                            html.Div([
                                dcc.Dropdown(
                                    id='busstop_dropdown',
                                    options=[
                                        {'label': 'Ayer Rajah Ave (one-north Stn)', 'value': '18051'},
                                        {'label': 'Ayer Rajah Ave (Opp one-north Stn)', 'value': '18059'},
                                        {'label': 'Portsdown Rd (one-north Stn/Galaxis)', 'value': '18159'},
                                        {'label': 'Portsdown Rd (Opp one-north Stn/Galaxis)', 'value': '18151'},
                                        {'label': 'Buona Vista Flyover (Opp Ayer Rajah Ind Est)', 'value': '18121'},
                                        {'label': 'Buona Vista Flyover (Ayer Rajah Ind Est)', 'value': '18129'},
                                    ],
                                    value='busstop'
                                ),
                                html.Div(id='dd-output-container')
                            ]),
                            html.Div(
                                [
                                    # html.P("SEA - Seats Available | SDA - Standing Available | LSD - Limited Standing", className="card-text"),
                                    dcc.Graph(figure=fig2)
                                ],
                                className="card-body"
                            ),
                        ],
                        className="card border-primary mb-3"
                    ))
                ]
            ),
            dbc.Button("Don't click here", color="danger"),
        ]
    ),
    className="mt-3",
)

tab3_content = dbc.Card(
    dbc.CardBody(
        [
            dbc.Row(
                [
                    dbc.Col(html.Div(
                        [
                            html.Div("Taxi Temporal Video", className="card-header"),
                            html.Video(
                                controls = True,
                                # # id = 'movie_player',
                                autoPlay=True,
                                src='/static/taxi_time_series.mp4'
                            ),
                        ],
                        className="card border-primary mb-3"
                        )),
                ]),

                dbc.Col(html.Div(
                        [
                            html.Div("Bus Late Count on a Daily Basis", className="card-header"),
                            html.Div([
                                dcc.Dropdown(
                                    id='busstop_dropdown',
                                    options=[
                                        {'label': 'Ayer Rajah Ave (one-north Stn)', 'value': '18051'},
                                        {'label': 'Ayer Rajah Ave (Opp one-north Stn)', 'value': '18059'},
                                        {'label': 'Portsdown Rd (one-north Stn/Galaxis)', 'value': '18159'},
                                        {'label': 'Portsdown Rd (Opp one-north Stn/Galaxis)', 'value': '18151'},
                                        {'label': 'Buona Vista Flyover (Opp Ayer Rajah Ind Est)', 'value': '18121'},
                                        {'label': 'Buona Vista Flyover (Ayer Rajah Ind Est)', 'value': '18129'},
                                    ],
                                    value='busstop'
                                ),
                                html.Div(id='dd-output-container')
                            ]),
                            html.Div(
                                [
                                    # html.P("SEA - Seats Available | SDA - Standing Available | LSD - Limited Standing", className="card-text"),
                                    dcc.Graph(figure=fig3)
                                ],
                                className="card-body"
                            ),
                        ],
                        className="card border-primary mb-3"
                    ))
        ]    
    )
)


tab4_content = dbc.Card(
    dbc.CardBody(
        [
            dbc.Row(
                [
                    dbc.Col(html.Div(
                        [
                            html.Div("Age", className="card-header"),
                            html.Img(
                                src='/static/Age.png',
                                style={'height':'100%', 'width':'100%'}
                            ),
                        ],
                        className="card border-primary mb-3"
                    )),
                    dbc.Col(html.Div(
                        [
                            html.Div("Ideal Transport in Rainy Weather", className="card-header"),
                            html.Img(
                                src='/static/if_rain_transport.png',
                                style={'height':'100%', 'width':'100%'}
                            ),
                        ],
                        className="card border-primary mb-3"
                    ))
                ]
            ),

            dbc.Row(
                [
                    dbc.Col(html.Div(
                        [
                            html.Div("Reasonable waiting time for Taxi(or other hailing services)", className="card-header"),
                            html.Img(
                                src='/static/taxi_waiting_time.png',
                                style={'height':'100%', 'width':'100%'}
                            ),
                        ],
                        className="card border-primary mb-3"
                    )),
                    dbc.Col(html.Div(
                        [
                            html.Div("Willingness to wait for buses past the estimated arrival time", className="card-header"),
                            html.Img(
                                src='/static/bus_waiting_time.png',
                                style={'height':'100%', 'width':'100%'}
                            ),
                        ],
                        className="card border-primary mb-3"
                    )),
                ]
            ),

            dbc.Row(
                [
                    dbc.Col(html.Div(
                        [
                            html.Div("Topic Modelling", className="card-header"),
                            html.Img(
                                src='/static/tm_clean.jpg'
                            ),
                        ],
                        className="card border-primary mb-3"
                    )),
                    dbc.Col(html.Div(
                        [
                            html.Div("Word Cloud", className="card-header"),
                            html.Img(
                                src='/static/twitterwordcloud_cleaneddata.png'
                            ),
                        ],
                        className="card border-primary mb-3"
                    )),
                ]
            ),

            
        ]
    ),
    className="mt-3",
)

#set app layour
app.layout = html.Div([
    dbc.Container(
        [
            html.H3("Transport Efficiency at One-North", className="display-3"),
            html.P("On this dashboard, we aim to provide a visualisation of the data that we have collected and processed over the past 2 months.", className="lead"),
            html.P("Data Collection Phase: 24 Dec 2020 - 26 Jan 2021", className="lead"),
            html.Hr(className="my-4"),

            html.Div(
                [
                    dbc.Tabs(
                        [
                            dbc.Tab(label="Bus Sufficiency", tab_id="tab-1"),
                            dbc.Tab(label="Bus Punctuality", tab_id="tab-2"),
                            dbc.Tab(label="Taxi Availability", tab_id="tab-3"),
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

# @app.callback(
#     dash.dependencies.Output('dd-output-container', 'children'),
#     [dash.dependencies.Input('busstop_dropdown', 'value')])

# def update_output(value):
#     return 'You have selected "{}"'.format(value)

def switch_tab(at):
    if at == "tab-1":
        return tab1_content
    elif at == "tab-2":
        return tab2_content
    elif at == "tab-3":
        return tab3_content
    elif at == "tab-4":
        return tab4_content

if __name__ == '__main__':
    app.run_server(debug=True)