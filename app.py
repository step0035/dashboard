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
from pandas.api.types import CategoricalDtype
import plotly.graph_objects as go

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
                                {'label': 'Ayer Rajah Ave (one-north Stn) - 18051', 'value': '18051'},
                                {'label': 'Ayer Rajah Ave (Opp one-north Stn) - 18059', 'value': '18059'},
                                {'label': 'Portsdown Rd (one-north Stn/Galaxis) - 18159', 'value': '18159'},
                                {'label': 'Portsdown Rd (Opp one-north Stn/Galaxis) - 18151', 'value': '18151'},
                                {'label': 'Buona Vista Flyover (Opp Ayer Rajah Ind Est) - 18121', 'value': '18121'},
                                {'label': 'Buona Vista Flyover (Ayer Rajah Ind Est) - 18129', 'value': '18129'},

                                # Newly Added
                                {'label': 'BUONA VISTA STN EXIT C - 11361', 'value': '11361'},
                                {'label': 'BUONA VISTA STN EXIT D - 11369', 'value': '11369'},
                                {'label': 'OPP GEMPLUS - 18021', 'value': '18021'},
                                {'label': 'TEMPCO MFG - 18029', 'value': '18029'},
                                {'label': 'BLK 71 - 18061', 'value': '18061'},
                                {'label': 'OPP BLK 71 - 18069', 'value': '18069'},
                                {'label': 'BLK 55 - 18081', 'value': '18081'},
                                {'label': 'SINGAPORE POST - 18089', 'value': '18089'},
                                {'label': 'AYER RAJAH BUS PK - 18099', 'value': '18099'},
                                {'label': 'BEF JLN HANG JEBAT (now Infinite Studios) - 18211', 'value': '18211'},
                                {'label': 'MEDIA CAMPUS - 18201', 'value': '18201'},
                                {'label': 'AFT WHITCHURCH RD - 18199', 'value': '18199'},
                                {'label': 'BEF WHITCHURCH RD - 18191', 'value': '18191'},
                                {'label': 'RAEBURN PK SCH (now is Tanglin Trust Sch) - 18189', 'value': '18189'},
                                {'label': 'OPP RAEBURN PK SCH - 18181', 'value': '18181'},
                                {'label': 'OPP WEYHILL CL - 18179', 'value': '18179'},
                                {'label': 'BEF WEYHILL CL - 18171', 'value': '18171'},
                                {'label': 'ESSEC BUSINESS SCH - 18149', 'value': '18149'},
                                {'label': 'AFT ANGLO-CHINESE JC - 18141', 'value': '18141'},
                            ],
                            value="18051"
                        ),
                        html.Div("Visualization Options", className="card-header", style={"margin-top":0}),
                        dcc.Dropdown(
                            id="tab1_viz_option",
                            options=[
                                {"label": "Show All Dates", "value": "all_dates"},
                                {"label": "Show All Hours", "value": "all_hour"},
                                {"label": "Show by Day of Week", "value": "day_week"},
                                {"label": "Filter by Weekday", "value": "weekday"},
                                {"label": "Show Selected Day", "value": "select_day"}
                            ],
                            value="all_dates"
                        ),
                        
                        html.Div(id='tab1_output-container-date-picker-single')
                    ]),
                    dbc.Col([
                        html.Div("Bus Number", className="card-header"),
                        dcc.Dropdown(id="tab1_bus_no"),

                        html.Div("Only Available if you have selected 'Day of Week'", className="card-header"),
                        dcc.Dropdown(
                            id="tab1_weekdays",
                            options=[
                                {"label": "Monday", "value": "Monday"},
                                {"label": "Tuesday", "value": "Tuesday"},
                                {"label": "Wednesday", "value": "Wednesday"},
                                {"label": "Thursday", "value": "Thursday"},
                                {"label": "Friday", "value": "Friday"},
                                {"label": "Saturday", "value": "Saturday"},
                                {"label": "Sunday", "value": "Sunday"}
                            ],
                            value = "Monday"
                        ),

                        html.Div("Only Available if you have selected 'Show Selected Day'", className="card-header"),
                        dcc.DatePickerSingle(
                            id='tab1_date_picker',
                        ),
                        
                    ]),
                ]),

            dbc.Row(
                [
                    dbc.Col([
                        html.Div("Bus Load Count", className="card-header", style={"margin-top":10}),
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
                        html.Div("Shuttle Bus Dispatch Count - Dummy Data", className="card-header"),
                        html.Div([
                            dcc.Graph(figure=shutfig),
                        ]),
                    ],
                    # className="card border-primary mb-3"
                    ),
                ]),

                dbc.Row(
                [
                    dbc.Col(html.Div(
                        [
                            html.Div("Bus 91 (High Load) Accumulative Capture", className="card-header"),
                            html.Video(
                                controls = True,
                                autoPlay=True,
                                src='/static/Bus91SDA_Accumulate.mp4'
                            ),
                        ],
                        className="card border-primary mb-3"
                        )),
                ]),

                dbc.Row(
                [
                    dbc.Col(html.Div(
                        [
                            html.Div("Bus 91 Temporal Capture", className="card-header"),
                            html.Video(
                                controls = True,
                                autoPlay=True,
                                src='/static/Bus91Temporal.mp4'
                            ),
                        ],
                        className="card border-primary mb-3"
                        )),
                ]),

                dbc.Row(
                [
                    dbc.Col(html.Div(
                        [
                            html.Div("Bus 91 Temporal Capture", className="card-header"),
                            html.Video(
                                controls = True,
                                autoPlay=True,
                                src='/static/Bus191SDA_Accumulate.mp4'
                            ),
                        ],
                        className="card border-primary mb-3"
                        )),
                ]),

                dbc.Row(
                [
                    dbc.Col(html.Div(
                        [
                            html.Div("Bus 91 Temporal Capture", className="card-header"),
                            html.Video(
                                controls = True,
                                autoPlay=True,
                                src='/static/Bus191Temporal.mp4'
                            ),
                        ],
                        className="card border-primary mb-3"
                        )),
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
    df = pd.read_csv(f"./data/bus_data/new_bus_arrival_{bus_stop_no}.csv")
    all_buses = df["bus_number"].unique()
    options = [{"label": bus_no, "value": bus_no} for bus_no in all_buses]
    value = all_buses[0] #default to first option

    return options, value

# Choose bus no
@app.callback(
    Output("tab1_date_picker", "min_date_allowed"),
    Output("tab1_date_picker", "max_date_allowed"),
    Output("tab1_date_picker", "date"),
    Input("tab1_bus_stop_no", "value"),
    Input("tab1_bus_no", "value")
)
def select_bus_no(bus_stop_no, bus_no):
    df = pd.read_csv(f"./data/bus_data/new_bus_arrival_{bus_stop_no}.csv")
    df = df[df["bus_number"]==bus_no]
    min_date_allowed = df["date"].unique()[0]
    max_date_allowed = df["date"].unique()[-1]
    date_arr = min_date_allowed.split("/")
    date_default = date(int(date_arr[2]), int(date_arr[0]), int(date_arr[1])) #default to first allowed date

    return min_date_allowed, max_date_allowed, date_default

# Filters
@app.callback(
    Output('tab1_output-container-date-picker-single', 'children'),
    Output('tab1_bus_graph', 'figure'),
    Output("tab1_date_picker", "disabled"),
    Output('tab1_weekdays', 'disabled'),
    Input('tab1_date_picker', 'date'),
    Input('tab1_bus_stop_no', 'value'),
    Input('tab1_bus_no', 'value'),
    Input("tab1_viz_option", "value"),
    # Input("tab1_radioitems", "value"),
    Input("tab1_weekdays", "value")
)

def update_output(date_value, bus_stop_no, bus_no, radioitem, weekday):
    if radioitem == "all_dates":
        df = pd.read_csv(f"./data/bus_data/new_bus_arrival_{bus_stop_no}.csv")
        df = df[df["bus_number"]==bus_no]
        df["date"] = pd.to_datetime(df["date"], format="%m/%d/%Y")
        df = df.groupby(["date", "first_next_bus_load"], as_index=False).size()
        fig = px.bar(df, x=df["date"], y=df["size"], color=df["first_next_bus_load"], barmode="group", labels={
                    "size": "Frequency | Occurences",
                    "date": "Date",
                    "first_next_bus_load": "Bus Load"
                },)

        return None, fig, True, True

    if radioitem == "all_hour":
        df = pd.read_csv(f"./data/bus_data/new_bus_arrival_{bus_stop_no}.csv")
        df = df[df["bus_number"]==bus_no]
        #df["date"] = pd.to_datetime(df["date"], format="%m/%d/%Y")
        df = df.groupby(["Hour", "first_next_bus_load"], as_index=False).size()
        fig = px.bar(df, x=df["Hour"], y=df["size"], color=df["first_next_bus_load"], barmode="group", labels={
                    "size": "Frequency | Occurences",
                    "date": "Hour (24h)",
                    "first_next_bus_load": "Bus Load"
                },)

        return None, fig, True, True

    if radioitem == "day_week":
        df = pd.read_csv(f"./data/bus_data/new_bus_arrival_{bus_stop_no}.csv")
        df = df[df["bus_number"]==bus_no]
        cats = [ 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        cat_type = CategoricalDtype(categories=cats, ordered=True)
        df["date"] = pd.to_datetime(df["date"], format="%m/%d/%Y")
        df["Weekday"] = df["date"].dt.day_name()
        df['Weekday']=df['Weekday'].astype(cat_type)
        df = df.groupby(["Weekday", "first_next_bus_load"], as_index=False).size()
        fig = px.bar(df, x=df["Weekday"], y=df["size"], color=df["first_next_bus_load"], barmode="group", labels={
                    "size": "Frequency | Occurences",
                    "Weekday": "Day",
                    "first_next_bus_load": "Bus Load"
                },)

        return None, fig, True, True

    if radioitem == "weekday":
        df = pd.read_csv(f"./data/bus_data/new_bus_arrival_{bus_stop_no}.csv")
        df = df[df["bus_number"]==bus_no]
        cats = [ 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        cat_type = CategoricalDtype(categories=cats, ordered=True)
        df["date"] = pd.to_datetime(df["date"], format="%m/%d/%Y")
        df["Weekday"] = df["date"].dt.day_name()
        df['Weekday']=df['Weekday'].astype(cat_type)
        df = df.groupby(["Weekday", "Hour", "first_next_bus_load"], as_index=False).size()
        df = df[df["Weekday"] == weekday]
        fig = px.bar(df, x=df["Hour"], y=df["size"], color=df["first_next_bus_load"], barmode="group", labels={
                    "size": "Frequency | Occurences",
                    "Hour": "Hour",
                    "first_next_bus_load": "Bus Load"
                },)

        return None, fig, True, False
    
    if radioitem == "select_day":
        string_prefix = 'You have selected: '
        date_object = date.fromisoformat(date_value)
        date_string = date_object.strftime('%B %d, %Y')
        df = pd.read_csv(f"./data/bus_data/new_bus_arrival_{bus_stop_no}.csv")
        df = df[df["bus_number"]==bus_no]
        df["date"] = pd.to_datetime(df["date"], format="%m/%d/%Y")
        df = df.groupby(["date", 'Hour', "first_next_bus_load"], as_index=False).size()
        df = df[df["date"]==date_object.strftime("%#m/%#d/%Y")]
        fig = px.bar(df, x=df["Hour"], y=df["size"], color=df["first_next_bus_load"], barmode="group", labels={
                    "size": "Frequency | Occurences",
                    "Hour": "Hour",
                    "first_next_bus_load": "Bus Load"
                },)

        return string_prefix + date_string, fig, False, True

##########################################################################################################################

#set content of tab2
tab2_content = dbc.Card(
    dbc.CardBody(
        [
            dbc.Row(
                [
                    dbc.Col([
                        html.Div("Bus Stop", className="card-header"),
                        dcc.Dropdown(
                            id="tab2_bus_stop_no",
                            options=[
                                {'label': 'Ayer Rajah Ave (one-north Stn) - 18051', 'value': '18051'},
                                {'label': 'Ayer Rajah Ave (Opp one-north Stn) - 18059', 'value': '18059'},
                                {'label': 'Portsdown Rd (one-north Stn/Galaxis) - 18159', 'value': '18159'},
                                {'label': 'Portsdown Rd (Opp one-north Stn/Galaxis) - 18151', 'value': '18151'},
                                {'label': 'Buona Vista Flyover (Opp Ayer Rajah Ind Est) - 18121', 'value': '18121'},
                                {'label': 'Buona Vista Flyover (Ayer Rajah Ind Est) - 18129', 'value': '18129'},

                                # Newly Added
                                {'label': 'BUONA VISTA STN EXIT C - 11361', 'value': '11361'},
                                {'label': 'BUONA VISTA STN EXIT D - 11369', 'value': '11369'},
                                {'label': 'OPP GEMPLUS - 18021', 'value': '18021'},
                                {'label': 'TEMPCO MFG - 18029', 'value': '18029'},
                                {'label': 'BLK 71 - 18061', 'value': '18061'},
                                {'label': 'OPP BLK 71 - 18069', 'value': '18069'},
                                {'label': 'BLK 55 - 18081', 'value': '18081'},
                                {'label': 'SINGAPORE POST - 18089', 'value': '18089'},
                                {'label': 'AYER RAJAH BUS PK - 18099', 'value': '18099'},
                                {'label': 'BEF JLN HANG JEBAT (now Infinite Studios) - 18211', 'value': '18211'},
                                {'label': 'MEDIA CAMPUS - 18201', 'value': '18201'},
                                {'label': 'AFT WHITCHURCH RD - 18199', 'value': '18199'},
                                {'label': 'BEF WHITCHURCH RD - 18191', 'value': '18191'},
                                {'label': 'RAEBURN PK SCH (now is Tanglin Trust Sch) - 18189', 'value': '18189'},
                                {'label': 'OPP RAEBURN PK SCH - 18181', 'value': '18181'},
                                {'label': 'OPP WEYHILL CL - 18179', 'value': '18179'},
                                {'label': 'BEF WEYHILL CL - 18171', 'value': '18171'},
                                {'label': 'ESSEC BUSINESS SCH - 18149', 'value': '18149'},
                                {'label': 'AFT ANGLO-CHINESE JC - 18141', 'value': '18141'},
                            ],
                            value="18051"
                        ),

                        html.Div("Visualization Options", className="card-header", style={"margin-top":0}),
                        dcc.Dropdown(
                            id="tab2_viz_option",
                            options=[
                                {"label": "Show All Dates", "value": "all_dates"},
                                {"label": "Show All Hours", "value": "all_hour"},
                                {"label": "Show by Day of Week", "value": "day_week"},
                                {"label": "Filter by Weekday (Inclusive of Customer Threshold)", "value": "weekday"},
                                {"label": "Show Selected Day", "value": "select_day"}
                            ],
                            value="all_dates"
                        ),

                        html.Div(id='tab2_output-container-date-picker-single')
                    ]),
                    dbc.Col([
                        html.Div("Bus Number", className="card-header"),
                        dcc.Dropdown(id="tab2_bus_no"),

                        html.Div("Only Available if you have selected 'Day of Week'", className="card-header"),
                        dcc.Dropdown(
                            id="tab2_weekdays",
                            options=[
                                {"label": "Monday", "value": "Monday"},
                                {"label": "Tuesday", "value": "Tuesday"},
                                {"label": "Wednesday", "value": "Wednesday"},
                                {"label": "Thursday", "value": "Thursday"},
                                {"label": "Friday", "value": "Friday"},
                                {"label": "Saturday", "value": "Saturday"},
                                {"label": "Sunday", "value": "Sunday"}
                            ],
                            value = "Monday"
                        ),

                        html.Div("Only Available if you have selected 'Show Selected Day'", className="card-header"),
                        dcc.DatePickerSingle(
                            id='tab2_date_picker',
                        ),
                        
                    ]),
                ]),

            dbc.Row(
                [
                    dbc.Col([
                        html.Div("Bus Late Count", className="card-header", style={"margin-top":10}),
                        html.Div([
                            # html.P("SEA - Seats Available | SDA - Standing Available | LSD - Limited Standing", className="card-text", style={"textAlign":"center"}),
                            dcc.Graph(id="tab2_bus_graph"),
                        ]),
                    ],
                    # className="card border-primary mb-3"
                    ),
                ]),
        ]
    ),
    className="mt-3",
)
###################################################################################
# TAB 2

# Choose bus stop
@app.callback(
    Output("tab2_bus_no", "options"),
    Output("tab2_bus_no", "value"),
    Input("tab2_bus_stop_no", "value")
)
def select_bus_stop(bus_stop_no):
    df = pd.read_csv(f"./data/bus_data/new_bus_arrival_{bus_stop_no}.csv")
    all_buses = df["bus_number"].unique()
    options = [{"label": bus_no, "value": bus_no} for bus_no in all_buses]
    value = all_buses[0] #default to first option

    return options, value

# Choose bus no
@app.callback(
    Output("tab2_date_picker", "min_date_allowed"),
    Output("tab2_date_picker", "max_date_allowed"),
    Output("tab2_date_picker", "date"),
    Input("tab2_bus_stop_no", "value"),
    Input("tab2_bus_no", "value")
)
def select_bus_no(bus_stop_no, bus_no):
    df = pd.read_csv(f"./data/bus_data/new_bus_arrival_{bus_stop_no}.csv")
    df = df[df["bus_number"]==bus_no]
    min_date_allowed = df["date"].unique()[0]
    max_date_allowed = df["date"].unique()[-1]
    date_arr = min_date_allowed.split("/")
    date_default = date(int(date_arr[2]), int(date_arr[0]), int(date_arr[1])) #default to first allowed date

    return min_date_allowed, max_date_allowed, date_default

# Filters
@app.callback(
    Output('tab2_output-container-date-picker-single', 'children'),
    Output('tab2_bus_graph', 'figure'),
    Output("tab2_date_picker", "disabled"),
    Output('tab2_weekdays', 'disabled'),
    Input('tab2_date_picker', 'date'),
    Input('tab2_bus_stop_no', 'value'),
    Input('tab2_bus_no', 'value'),
    Input("tab2_viz_option", "value"),
    Input("tab2_weekdays", "value")
)

def update_output(date_value, bus_stop_no, bus_no, radioitem, weekday):
    if radioitem == "all_dates":
        df = pd.read_csv(f"./data/bus_data/new_bus_arrival_{bus_stop_no}.csv")
        df = df[df["bus_number"]==bus_no]
        df["date"] = pd.to_datetime(df["date"], format="%m/%d/%Y")
        df = df.groupby(["date", "Late_By"], as_index=False).size()
        fig = px.bar(df, x=df["date"], y=df["size"], color=df["Late_By"], labels={
                    "size": "Frequency | Occurences",
                    "date": "Date",
                    "Late_By": "Late By in Seconds"
                })

        return None, fig, True, True

    if radioitem == "all_hour":
        df = pd.read_csv(f"./data/bus_data/new_bus_arrival_{bus_stop_no}.csv")
        df = df[df["bus_number"]==bus_no]
        #df["date"] = pd.to_datetime(df["date"], format="%m/%d/%Y")
        df = df.groupby(["Hour", "Late_By"], as_index=False).size()
        fig = px.bar(df, x=df["Hour"], y=df["size"], color=df["Late_By"], labels={
                    "size": "Frequency | Occurences",
                    "Hour": "Hour",
                    "Late_By": "Late By in Seconds"
                })

        return None, fig, True, True

    if radioitem == "day_week":
        df = pd.read_csv(f"./data/bus_data/new_bus_arrival_{bus_stop_no}.csv")
        df = df[df["bus_number"]==bus_no]
        cats = [ 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        cat_type = CategoricalDtype(categories=cats, ordered=True)
        df["date"] = pd.to_datetime(df["date"], format="%m/%d/%Y")
        df["Weekday"] = df["date"].dt.day_name()
        df['Weekday']=df['Weekday'].astype(cat_type)
        df = df.groupby(["Weekday", "Late_By"], as_index=False).size()
        fig = px.bar(df, x=df["Weekday"], y=df["size"], color=df["Late_By"], labels={
                    "size": "Frequency | Occurences",
                    "Weekday": "Weekday",
                    "Late_By": "Late By in Seconds"
                })

        return None, fig, True, True

    if radioitem == "weekday":
        df = pd.read_csv(f"./data/bus_data/new_bus_arrival_{bus_stop_no}.csv")
        df = df[df["bus_number"]==bus_no]
        cats = [ 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        cat_type = CategoricalDtype(categories=cats, ordered=True)
        df["date"] = pd.to_datetime(df["date"], format="%m/%d/%Y")
        df["Weekday"] = df["date"].dt.day_name()
        df['Weekday']=df['Weekday'].astype(cat_type)
        df = df.groupby(["Weekday", "Hour"], as_index=False).mean()
        df = df[df["Weekday"] == weekday]
        fig = px.bar(df, x=df["Hour"], y=df["Late_By"], labels={
                    "Late_By": "Averaged Late By (seconds)",
                    "Weekday": "Weekday",
                })
        fig.add_shape(
            go.layout.Shape(
                type="line",
                x0=0,
                y0=300,
                x1=24,
                y1=300,
                line=dict(
                    color="Orange",
                    width=2,
                    dash="solid",
                ),
        ))

        return None, fig, True, False
    
    if radioitem == "select_day":
        string_prefix = 'You have selected: '
        date_object = date.fromisoformat(date_value)
        date_string = date_object.strftime('%B %d, %Y')
        df = pd.read_csv(f"./data/bus_data/new_bus_arrival_{bus_stop_no}.csv")
        df = df[df["bus_number"]==bus_no]
        df["date"] = pd.to_datetime(df["date"], format="%m/%d/%Y")
        df = df.groupby(["date", 'Hour', "Late_By"], as_index=False).size()
        df = df[df["date"]==date_object.strftime("%#m/%#d/%Y")]
        fig = px.bar(df, x=df["Hour"], y=df["Late_By"], barmode="group", labels={
                    "Late_By": "Late By (seconds)",
                    "Hour": "Hour",
                })

        return string_prefix + date_string, fig, False, True
###################################################################################

tab3_content = dbc.Card(
    dbc.CardBody(
        [
            dbc.Row(
                [
                    dbc.Col(html.Div(
                        [
                            html.Div("Taxi Temporal Capture", className="card-header"),
                            html.Video(
                                controls = True,
                                autoPlay=True,
                                src='/static/taxi_time_series.mp4'
                            ),
                        ],
                        className="card border-primary mb-3"
                        )),
                ]),

                dbc.Row(
                [
                    dbc.Col(html.Div(
                        [
                            html.Div("Taxi Heat Map Capture - Phase 1", className="card-header"),
                            html.Video(
                                controls = True,
                                autoPlay=True,
                                src='/static/.mp4'
                            ),
                        ],
                        className="card border-primary mb-3"
                        )),
                ]),

                dbc.Row(
                [
                    dbc.Col(html.Div(
                        [
                            html.Div("Taxi Heat Map Capture - Phase 2", className="card-header"),
                            html.Video(
                                controls = True,
                                autoPlay=True,
                                src='/static/taxi_temporal_phase2.mp4'
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
            html.P("Data Collection Phase: 30 January 2021 - 5 March 2021", className="lead"),
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

# First Batch
                                # {'label': '[1] Ayer Rajah Ave (one-north Stn)', 'value': '18051old'},
                                # {'label': '[1] Ayer Rajah Ave (Opp one-north Stn)', 'value': '18059old'},
                                # {'label': '[1] Portsdown Rd (one-north Stn/Galaxis)', 'value': '18159old'},
                                # {'label': '[1] Portsdown Rd (Opp one-north Stn/Galaxis)', 'value': '18151old'},
                                # {'label': '[1] Buona Vista Flyover (Opp Ayer Rajah Ind Est)', 'value': '18121old'},
                                # {'label': '[1] Buona Vista Flyover (Ayer Rajah Ind Est)', 'value': '18129old'},

                                # dcc.RadioItems(
                        #     id="tab1_radioitems",
                        #     options=[
                        #         {"label": "Show All Dates", "value": "all_dates"},
                        #         {"label": "Show All Hours", "value": "all_hour"},
                        #         {"label": "Show by Day of Week", "value": "day_week"},
                        #         {"label": "Filter by Weekday", "value": "weekday"},
                        #         {"label": "Show Selected Day", "value": "select_day"}
                        #     ],
                        #     value="all_dates",
                        #     labelStyle = {"display": "block"}
                        # ),