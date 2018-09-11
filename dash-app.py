#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# dash-app.py

"""Interactive visualization for take home project
"""

from dash.dependencies import Input, State, Output, Event
from dotenv import load_dotenv
from plotly.colors import DEFAULT_PLOTLY_COLORS
from subprocess import check_output
import numpy as np
import os

from dashboard.components import Col
from dashboard.components import Container
from dashboard.components import Row

import warnings
with warnings.catch_warnings():
    # ignore warnings that are safe to ignore according to
    # https://github.com/ContinuumIO/anaconda-issues/issues/6678
    # #issuecomment-337276215
    warnings.simplefilter("ignore")
    import dash
    import dash_core_components as dcc
    import dash_html_components as html
    import pandas as pd


load_dotenv()

app = dash.Dash(__name__)
app.title = 'Dash Skeleton'
server = app.server
my_css_url = "https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css"
app.css.append_css({"external_url": my_css_url})
BOOTSTRAP_SCREEN_SIZE = 'lg'
ROOT_PATH = './'

# If you need to run your app locally
# app.scripts.config.serve_locally = True

csv_path = os.path.join(
    ROOT_PATH, 'data/processed/data.csv'
)

if os.path.isfile(csv_path):
    FULL_DF = pd.read_csv(csv_path)
else:
    FULL_DF = pd.DataFrame({2: np.arange(5), 1: np.arange(1, 6)})


def get_updated_df():
    df = FULL_DF.copy()
    # Process df
    return df


app.layout = Container([
    Row(
        Col(
            [
                html.Label('Options'),
                dcc.Checklist(
                    id='checklist',
                    options=[
                        {'label': 'A', 'value': 'A'},
                        {'label': 'B', 'value': 'B'},
                    ],
                    values=['A', 'B'],
                    labelStyle={'margin': '5px'},
                )
            ], bp=BOOTSTRAP_SCREEN_SIZE, size=12,
        )
    ),
    Row(
        Col(
            [
                dcc.Graph(id='graph_1')
            ], bp=BOOTSTRAP_SCREEN_SIZE, size=12,
        )
    ),
    html.Div(id='hidden-data', style={'display': 'none'}),
])


@app.callback(
    Output('hidden-data', 'children'),
    [
        Input('checklist', 'values'),
    ],
)
def hidden_data_callback(checklist_values):
    df = get_updated_df()
    return df.to_json(orient='split')


@app.callback(
    Output('graph_1', 'figure'),
    [Input('hidden-data', 'children')],
)
def graph_1_callback(jsonified_cleaned_data):
    df = pd.read_json(jsonified_cleaned_data, orient='split')
    return {
        'data': [
            {
                'x': df.index,
                'y': df[col],
                'type': 'scatter',
                'name': col,
                'mode': 'markers',
                'marker': {'size': 10},
                # 'marker': {'size': 10, 'color': POSITION_COLORS[position]},
            } for col in df.columns
        ],
        'layout': {
            'title': 'Sample Graph',
            'height': '400',
            'font': {'size': 14},
            'hovermode': 'closest',
            'xaxis': {'title': 'x'},
            'yaxis': {'title': 'y'},
        },
    }


if __name__ == '__main__':
    # To make this app publicly available, supply the parameter host='0.0.0.0'.
    # You should also disable debug mode in production.
    app.run_server(debug=True, port=8051)
