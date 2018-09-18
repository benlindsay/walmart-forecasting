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
from src.load import load_train_df
from src.transform import get_week_by_dept_df

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

# csv_path = os.path.join(
#     ROOT_PATH, 'data/raw/train.csv'
# )

# if os.path.isfile(csv_path):
#     FULL_DF = pd.read_csv(csv_path)
# else:
#     FULL_DF = pd.DataFrame({2: np.arange(5), 1: np.arange(1, 6)})

train_df = load_train_df()
ALL_STORES, ALL_DEPTS = train_df['Store'].unique(), train_df['Dept'].unique()
FULL_DF = get_week_by_dept_df(train_df)

def get_updated_df(stores=[1], depts=[1]):
    store_dept_str_list = ['{}_{}'.format(s, d) for d in depts for s in stores]
    df = get_week_by_dept_df()
    store_dept_str_list = [s for s in store_dept_str_list if s in df.columns]
    df = df[store_dept_str_list].copy()
    return df


app.layout = Container([
    Row(
        [
            Col(
                [
                    html.Label('Stores'),
                    dcc.Dropdown(
                        id='stores',
                        options=[
                            {'label': str(s), 'value': str(s)}
                            for s in ALL_STORES
                        ],
                        value=['1'],
                        multi=True,
                    )
                ], bp=BOOTSTRAP_SCREEN_SIZE, size=12,
            ),
            Col(
                [
                    html.Label('Departments'),
                    dcc.Dropdown(
                        id='depts',
                        options=[
                            {'label': str(d), 'value': str(d)}
                            for d in ALL_DEPTS
                        ],
                        value=['1'],
                        multi=True,
                    )
                ], bp=BOOTSTRAP_SCREEN_SIZE, size=12,
            ),
        ]
    ),
    Row(
        Col(
            [
                dcc.Graph(
                    id='graph_1',
                    config={
                        'editable': True,
                        'edits': {'shapePosition': True}
                    },
                )
            ], id='graph_div', bp=BOOTSTRAP_SCREEN_SIZE, size=12,
        )
    ),
    html.Div(id='hidden-data', style={'display': 'none'}),
])


@app.callback(
    Output('hidden-data', 'children'),
    [
        Input('stores', 'value'),
        Input('depts', 'value'),
    ],
)
def hidden_data_callback(stores_value, depts_value):
    df = get_updated_df(stores=stores_value, depts=depts_value)
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
                'mode': 'lines',
                # 'marker': {'size': 10},
                # 'marker': {'size': 10, 'color': POSITION_COLORS[position]},
            } for col in df.columns
        ],
        'layout': {
            'title': 'Walmart Sales over Time',
            'height': '400',
            'font': {'size': 14},
            'hovermode': 'compare',
            'xaxis': {'title': 'Date'},
            'yaxis': {'title': 'Weekly Sales'},
            'shapes': [{
                'type': 'line',
                'x0': df.index[len(df)//2],
                'x1': df.index[len(df)//2],
                'xref': 'x',
                'y0': 0,
                'y1': df.max().max(),
                'yref': 'y',
                'line': {
                    'width': 2,
                    'color': 'rgb(30, 30, 30)',
                }
            }]
        },
    }

# @app.callback(
#     Output('count', 'children'),
#     [],
#     [],
#     [Event('graph_div', 'release')],
# )
# def increment():
#     global COUNT
#     COUNT += 1
#     return str(COUNT)


if __name__ == '__main__':
    # To make this app publicly available, supply the parameter host='0.0.0.0'.
    # You should also disable debug mode in production.
    app.run_server(debug=True, port=8051)
