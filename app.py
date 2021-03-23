# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.
import os
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime
from datetime import date

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
app.config.suppress_callback_exceptions = True

# Dummy graph for shuttle bus | SAMPLE DATA
df = pd.read_csv('./data/bus_data/new_bus_arrival_18121_14.csv')
df["date"] = pd.to_datetime(df["date"], format="%d/%m/%Y")
df = df.groupby(["date", "first_next_bus_load"], as_index=False).size()
shutfig = px.bar(df, x=df["date"], y=df["size"], color=df["first_next_bus_load"])

# Taxi Availability Graph
df_taxi = pd.read_csv('./data/taxi_data/relevant_taxi_availability.csv')
df_taxi["date"] = pd.to_datetime(df_taxi["date"], format="%m/%d/%Y")
df_taxi = df_taxi.groupby(["date", "count"], as_index=False).size()
fig3 = px.bar(df_taxi, x=df_taxi["date"], y=df_taxi["size"], color=df_taxi["count"], barmode="relative")

#set content of tab1
tab1_content = dbc.Card(
    dbc.CardBody(
        [
            dbc.Row(
                [
                    dbc.Col([
                        html.Div("Bus Stop", className="card-header"),
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
                        dcc.RadioItems(
                            id="radioitems",
                            options=[
                                {"label": "Show All Days", "value": "all_day"},
                                {"label": "Show All Hours", "value": "all_hour"},
                                {"label": "Show Selected Day", "value": "select_day"},
                            ],
                            value="all_day",
                            labelStyle = {"display": "block"}
                        ),
                        dcc.DatePickerSingle(
                            id='date_picker',
                            style={"margin-top":10},
                        ),
                        html.Div(id='output-container-date-picker-single')
                    ]),
                    dbc.Col([
                        html.Div("Bus Number", className="card-header"),
                        dcc.Dropdown(id="tab1_bus_no")
                    ]),
                ]),

            dbc.Row(
                [
                    dbc.Col([
                        html.Div("Bus Load Count on a Daily Basis", className="card-header", style={"margin-top":10}),
                        html.Div([
                            html.P("SEA - Seats Available | SDA - Standing Available | LSD - Limited Standing", className="card-text", style={"textAlign":"center"}),
                            dcc.Graph(id="tab1_bus_graph"),
                        ]),
                    ],
                    # className="card border-primary mb-3"
                    ),
                ]),

            dbc.Row(
                [
                    dbc.Col([
                        html.Div("Shuttle Bus Dispatch Count on a Daily Basis", className="card-header"),
                        html.Div([
                            dcc.Graph(figure=shutfig),
                        ]),
                    ],
                    # className="card border-primary mb-3"
                    ),
                ]),
        ]
    ),
    className="mt-3"
)

##########################################################################################################################
#TAB 1

# Choose bus stop
@app.callback(
    Output("tab1_bus_no", "options"),
    Output("tab1_bus_no", "value"),
    Input("tab1_bus_stop_no", "value")
)
def select_bus_stop(bus_stop_no):
    df = pd.read_csv(f"./data/bus_data/new_bus_arrival_{bus_stop_no}_2nd.csv")
    all_buses = df["bus_number"].unique()
    options = [{"label": bus_no, "value": bus_no} for bus_no in all_buses]
    value = all_buses[0] #default to first option

    return options, value

# Choose bus no
@app.callback(
    Output("date_picker", "min_date_allowed"),
    Output("date_picker", "max_date_allowed"),
    Output("date_picker", "date"),
    Input("tab1_bus_stop_no", "value"),
    Input("tab1_bus_no", "value")
)
def select_bus_no(bus_stop_no, bus_no):
    df = pd.read_csv(f"./data/bus_data/new_bus_arrival_{bus_stop_no}_2nd.csv")
    df = df[df["bus_number"]==bus_no]
    min_date_allowed = df["date"].unique()[0]
    max_date_allowed = df["date"].unique()[-1]
    date_arr = min_date_allowed.split("/")
    date_default = date(int(date_arr[2]), int(date_arr[0]), int(date_arr[1])) #default to first allowed date

    return min_date_allowed, max_date_allowed, date_default

# Date Picker
@app.callback(
    Output('output-container-date-picker-single', 'children'),
    Output('tab1_bus_graph', 'figure'),
    Output("date_picker", "disabled"),
    Input('date_picker', 'date'),
    Input('tab1_bus_stop_no', 'value'),
    Input('tab1_bus_no', 'value'),
    Input("radioitems", "value")
)

def update_output(date_value, bus_stop_no, bus_no, radioitem):
    if radioitem == "all_day":
        df = pd.read_csv(f"./data/bus_data/new_bus_arrival_{bus_stop_no}_2nd.csv")
        df = df[df["bus_number"]==bus_no]
        df["date"] = pd.to_datetime(df["date"], format="%m/%d/%Y")
        df = df.groupby(["date", "first_next_bus_load"], as_index=False).size()
        fig = px.bar(df, x=df["date"], y=df["size"], color=df["first_next_bus_load"], barmode="group")

        return None, fig, True

    if radioitem == "all_hour":
        df = pd.read_csv(f"./data/bus_data/new_bus_arrival_{bus_stop_no}_2nd.csv")
        df = df[df["bus_number"]==bus_no]
        #df["date"] = pd.to_datetime(df["date"], format="%m/%d/%Y")
        df = df.groupby(["Hour", "first_next_bus_load"], as_index=False).size()
        fig = px.bar(df, x=df["Hour"], y=df["size"], color=df["first_next_bus_load"], barmode="group")

        return None, fig, True
    
    if radioitem == "select_day":
        string_prefix = 'You have selected: '
        date_object = date.fromisoformat(date_value)
        date_string = date_object.strftime('%B %d, %Y')
        df = pd.read_csv(f"./data/bus_data/new_bus_arrival_{bus_stop_no}_2nd.csv")
        df = df[df["bus_number"]==bus_no]
        df["date"] = pd.to_datetime(df["date"], format="%m/%d/%Y")
        test = date_object.strftime("%#m/%#d/%Y")
        df = df.groupby(["date", 'Hour', "first_next_bus_load"], as_index=False).size()
        df = df[df["date"]==test]
        fig = px.bar(df, x=df["Hour"], y=df["size"], color=df["first_next_bus_load"], barmode="group")

        return string_prefix + date_string, fig, False




##########################################################################################################################

#set content of tab2
tab2_content = dbc.Card(
    dbc.CardBody(
        [
            dbc.Row(
                [
                    dbc.Col(html.Div([
                        html.Div("Bus Stop", className="card-header"),
                        dcc.Dropdown(
                            id="tab2_bus_stop_no",
                            options=[
                                {'label': 'Ayer Rajah Ave (one-north Stn)', 'value': '18051'},
                                {'label': 'Ayer Rajah Ave (Opp one-north Stn)', 'value': '18059'},
                                {'label': 'Portsdown Rd (one-north Stn/Galaxis)', 'value': '18159'},
                                {'label': 'Portsdown Rd (Opp one-north Stn/Galaxis)', 'value': '18151'},
                                {'label': 'Buona Vista Flyover (Opp Ayer Rajah Ind Est)', 'value': '18121'},
                                {'label': 'Buona Vista Flyover (Ayer Rajah Ind Est)', 'value': '18129'},
                            ],
                            value='18051'
                        ),
                    ]),
                    ),
                    dbc.Col(html.Div([
                        html.Div("Bus Number", className="card-header"),
                        dcc.Dropdown(id="tab2_bus_no"),
                    ]),
                    ),
                ]),

            dbc.Row(
                [
                    dbc.Col(html.Div([
                            html.Div("Bus Late Count on a Daily Basis", className="card-header", style={"margin-top":10}),
                            html.Div([dcc.Graph(id="tab2_bus_graph")], className="card-body")],
                            # className="card border-primary mb-3"
                        ),
                        ),
                ]
            ),
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
                                autoPlay=True,
                                src='/static/taxi_time_series.mp4'
                            ),
                        ],
                        className="card border-primary mb-3"
                        )),
                ]),

                dbc.Col(html.Div(
                        [
                            html.Div("Taxi Availability Count on a Daily Basis", className="card-header"),
                            # html.Div([
                            #     dcc.Dropdown(
                            #         id='busstop_dropdown',
                            #         options=[
                            #             {'label': 'Ayer Rajah Ave (one-north Stn)', 'value': '18051'},
                            #             {'label': 'Ayer Rajah Ave (Opp one-north Stn)', 'value': '18059'},
                            #             {'label': 'Portsdown Rd (one-north Stn/Galaxis)', 'value': '18159'},
                            #             {'label': 'Portsdown Rd (Opp one-north Stn/Galaxis)', 'value': '18151'},
                            #             {'label': 'Buona Vista Flyover (Opp Ayer Rajah Ind Est)', 'value': '18121'},
                            #             {'label': 'Buona Vista Flyover (Ayer Rajah Ind Est)', 'value': '18129'},
                            #         ],
                            #         value='busstop'
                            #     ),
                            #     html.Div(id='dd-output-container')
                            # ]),
                            html.Div(
                                [
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
                            dbc.Tab(label="Survey & Sentiments", tab_id="tab-4")
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


#TAB 2
@app.callback(
    Output("tab2_bus_no", "options"),
    Output("tab2_bus_no", "value"),
    Input("tab2_bus_stop_no", "value")
)
def select_bus_stop(bus_stop_no):
    df = pd.read_csv(f"./data/bus_data/new_bus_arrival_{bus_stop_no}.csv")
    all_buses = df["bus_number"].unique()
    options = [{"label": bus_no, "value": bus_no} for bus_no in all_buses]
    value = all_buses[0]

    return options, value

@app.callback(
    Output("tab2_bus_graph", "figure"),
    Input("tab2_bus_stop_no", "value"),
    Input("tab2_bus_no", "value")
)
def select_bus_no(bus_stop_no, bus_no):
    df = pd.read_csv(f"./data/bus_data/new_bus_arrival_{bus_stop_no}.csv")
    df = df[df["bus_number"]==bus_no]
    df["date"] = pd.to_datetime(df["date"], format="%d/%m/%Y")
    df = df.groupby(["date", "Late_By"], as_index=False).size()
    fig = px.bar(df, x=df["date"], y=df["size"], color=df["Late_By"], )
    # barmode="group"

    return fig



if __name__ == '__main__':
    app.run_server(debug=True)


# PAST CODES
# # Graph 1 Bar Chart of Bus Loads vs Size
# df = pd.read_csv('./data/bus_data/new_bus_arrival_18121_14.csv')
# df["date"] = pd.to_datetime(df["date"], format="%d/%m/%Y")

# load_df = df.groupby(["date", "first_next_bus_load"], as_index=False).size()
# fig1 = px.bar(load_df, x=load_df["date"], y=load_df["size"], color=load_df["first_next_bus_load"], barmode="group")

# # Graph 2 S
# load_df2 = df.groupby(["date", "Late_By"], as_index=False).size()
# fig2 = px.bar(load_df2, x=load_df2["date"], y=load_df2["size"], color=load_df2["Late_By"], barmode="group")