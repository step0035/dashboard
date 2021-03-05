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

#load data
df = pd.read_csv('./data/clean_csv_data/new_bus_arrival_18121.csv')
df["date"] = pd.to_datetime(df["date"], format="%d/%m/%Y")


""" print(type(df["date"][0]))
for i in range(len(df["date"])):
    newDate = datetime.strptime(df.iloc[i]["date"], "%d/%m/%Y").strftime("%Y/%m/%d")
    df.iloc[i]["date"] = newDate
    #print(row) """
print(df['date'][0])


#preprocess data
#df = df.groupby("date").sum()[["late", "late_by"]]
#graph1_df = df.groupby(pd.Grouper(freq='D')).sum()[["late", "late_by"]]

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])

#function to create a column graph box

#create graphs
load_df = df.groupby(["date", "first_next_bus_load"], as_index=False).size()
fig1 = px.bar(load_df, x=load_df["date"], y=load_df["size"], color=load_df["first_next_bus_load"], barmode="group")

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
                            html.Div("Number of late buses per date", className="card-header"),
                            html.Div(
                                [
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
                            html.Div("Header", className="card-header"),
                            html.Div(
                                [
                                    html.H4("Graph 4", className="card-title"),
                                    html.P("Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.", className="card-text")
                                ],
                                className="card-body"
                            ),
                            
                        ],
                        className="card border-primary mb-3"
                    )),
                    dbc.Col(html.Div(
                        [
                            html.Div("Header", className="card-header"),
                            html.Div(
                                [
                                    html.H4("Graph 5", className="card-title"),
                                    html.P("Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.", className="card-text")
                                ],
                                className="card-body"
                            ),
                            
                        ],
                        className="card border-primary mb-3"
                    )),
                    dbc.Col(html.Div(
                        [
                            html.Div("Header", className="card-header"),
                            html.Div(
                                [
                                    html.H4("Graph 6", className="card-title"),
                                    html.P("Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.", className="card-text")
                                ],
                                className="card-body"
                            ),
                            
                        ],
                        className="card border-primary mb-3"
                    ))
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
            html.H1("Hello", className="display-3"),
            html.P("Welcome to my Dashboard, my name is hululuhuhu", className="lead"),
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

if __name__ == '__main__':
    app.run_server(debug=True)