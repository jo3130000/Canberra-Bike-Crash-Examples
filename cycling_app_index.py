import json
import sys

import plotly as plt
import plotly.express as px
import pandas as pd
import csv
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State
from flask import request

from cycling_dashboard_app import app, server

from apps import cycling_visual_one
from apps import cycling_visual_two
from apps import cycling_visual_three
from apps import cycling_visual_four



list_colors = [
    '#003f5c'
    '#2f4b7c'
    '#665191'
    '#a05195'
    '#d45087'
    '#f95d6a'
    '#ff7c43'
    '#ffa600'
]

app.layout = html.Div(
    id='main',
    children=[
        #pathname being used to select first visual
        dcc.Location(id='url', refresh=False, pathname='/apps/visual_one'),
        html.Div(
            id='side_menu',
            children=[
                dcc.Link('Cyclist Crashes by Suburb and District', href='/apps/visual_one'),
                dcc.Link('Cyclist Crashed and Weather', href='/apps/visual_two'),
                dcc.Link('Cyclist Crashes by Lighting', href='/apps/visual_three'),
                dcc.Link('Cyclist Crashed by Time and Day', href='/apps/visual_four'),
                dcc.Link('Close', href='/close')
            ]
        ),
        html.Div(
            id='output',
            children=[]
        )
    ]
)


@app.callback(
    Output(component_id='output', component_property='children'),
    [Input(component_id='url', component_property='pathname')]
)
def display_dashboard(pathname):
    if pathname == '/apps/visual_one':
        return cycling_visual_one.var_dashboard
    elif pathname == '/apps/visual_two':
        return cycling_visual_two.var_dashboard
    elif pathname == '/apps/visual_three':
        return cycling_visual_three.var_dashboard
    elif pathname == '/apps/visual_four':
        return cycling_visual_four.var_dashboard
    elif pathname == '/close':
        func = request.environ.get('werkzeug.server.shutdown')
        func()
        return html.P('Sever Closed Successfully')
    else:
        return html.P('Error 404: Page not found...')


if __name__ == '__main__':
    app.run_server(debug=True)
    #, dev_tools_ui=False
