import dash
from dash import Dash, html, dcc, callback, dash_table 
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.exc import OperationalError
from datetime import datetime as dt
from datetime import timedelta as td
from datetime import timezone as tz
import socket
import logging
import os
import pandas as pd
from dotenv import load_dotenv
from packaging import version

# local modules
from plot_generators import time_series_generator
from plot_generators import profile_generator
from plot_generators import status_indicator


# set a local switch to set dash server
computer = socket.gethostname()
if computer == 'WONTN74902':
    local = True
else:
    local = False



if local:     
    url_prefix = "/app/AQPDBOR/"
    app = dash.Dash(__name__, 
        url_base_pathname=url_prefix,
        external_stylesheets=[dbc.themes.BOOTSTRAP],
        suppress_callback_exceptions=True
        ) 

else:
    url_prefix = "/dash/"
    app = dash.Dash(__name__, 
            requests_pathname_prefix=url_prefix,
            external_stylesheets=[dbc.themes.BOOTSTRAP],
            suppress_callback_exceptions=True
            ) 

# set up Dash server
server = app.server

logging.basicConfig(
    level=logging.DEBUG,
    format="%(message)s"
)

logger = logging.getLogger(__name__)

# Load variables from .env into environment
load_dotenv()
DB_HOST = os.getenv('QP_SERVER')
DB_USER = os.getenv('QP_VIEWER_USER')
DB_PASS = os.getenv('QP_VIEWER_PASSWORD')

# logger.info('Credentials loaded locally')
logger.debug(f"{'DATABASE_SERVER'}: {DB_HOST}")
logger.debug(f"{'DATABASE_USER'}: {DB_USER}")

# set up the engine
sql_engine_string=('postgresql://{}:{}@{}/{}?sslmode=require').format(DB_USER,DB_PASS,DB_HOST,'borden')
sql_engine=create_engine(sql_engine_string,pool_pre_ping=True)

# set datetime parameters
first_date=dt.strftime(dt(dt.today().year, 1, 1),'%Y-%m-%d')

now=dt.now(tz.utc)
start_date=(now-td(days=7)).strftime('%Y-%m-%d %H:%M')
end_date=now.strftime('%Y-%m-%d %H:%M')
start_time=(now-td(hours=1)).strftime('%h:%m')

# set up the app layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(  # LEFT: Status Indicator (2/12 width)
            status_indicator('status_indicator', sql_engine),  # your function
            width=2,
            style={
                'backgroundColor': '#f8f9fa',
                'padding': '10px',
                'borderRight': '1px solid #dee2e6',
                'height': '100vh',
                'overflowY': 'auto'
            }
        ),
        dbc.Col(  # RIGHT: Main Dashboard (10/12 width)
            html.Div([
                html.H1('BORDEN DATA DASHBOARD', style={'textAlign': 'center'}),
                html.H3('Pick the desired date range (UTC). This will apply to all time plots on the page.'),
                dcc.DatePickerRange(
                    id='date-picker',
                    min_date_allowed=first_date,
                    max_date_allowed=end_date,
                    display_format='YYYY-MM-DD'
                ),
                html.Br(),
                html.A(html.Button('Borden CR3000 Temperatures Display', id='page1-btn', n_clicks=0), href='#plot_1'),
                html.Br(),
                html.A(html.Button('Borden CSAT Temperatures Display', id='page2-btn', n_clicks=0), href='#plot_2'),
                html.Br(),
                html.A(html.Button('Borden Gases Display', id='page3-btn', n_clicks=0), href='#plot_3'),
                html.Br(),
                html.A(html.Button('Borden Water Vapour Display', id='page4-btn', n_clicks=0), href='#plot_4'),
                html.Br(),
                html.A(html.Button('Borden Profile', id='page5-btn', n_clicks=0), href='#plot_5'),
                html.Br(),
                html.H2('Borden CR3000 Temperatures Display'),
                dcc.Graph(id='plot_1', figure=time_series_generator(start_date, end_date, 'plot_1', sql_engine)),
                html.Br(),
                html.H2('Borden CSAT Temperatures Display'),
                dcc.Graph(id='plot_2', figure=time_series_generator(start_date, end_date, 'plot_2', sql_engine)),
                html.Br(),
                html.H2('Borden Gases Display'),
                dcc.Graph(id='plot_3', figure=time_series_generator(start_date, end_date, 'plot_3', sql_engine)),
                html.Br(),
                html.H2('Borden Water Vapour Display'),
                dcc.Graph(id='plot_4', figure=time_series_generator(start_date, end_date, 'plot_4', sql_engine)),
                html.Br(),
                html.H2('Borden Tower Measurements'),
                dcc.Graph(id='plot_5', figure=profile_generator('q_profile_last_available_cycle', sql_engine))
            ]),
            width=10,
            style={'padding': '20px'}
        )
    ]),
    dcc.Interval(
    id="interval-component",
    interval=60*1000,  # refresh every 60 seconds
    n_intervals=0      # starts at 0
    ),
], fluid=True)


logger.info('plot generated')
@app.callback(
    Output('plot_1', 'figure'),
    Output('plot_2', 'figure'),
    Output('plot_3', 'figure'),
    Output('plot_4', 'figure'),
    Input('date-picker', 'start_date'),
    Input('date-picker', 'end_date'))

def update_output(start_date,end_date):
    if not start_date or not end_date:
        raise PreventUpdate
    else:
        logger.info('Updating plot')
        plot_1_fig=time_series_generator(start_date,end_date,'plot_1',sql_engine)
        plot_2_fig=time_series_generator(start_date,end_date,'plot_2',sql_engine)
        plot_3_fig=time_series_generator(start_date,end_date,'plot_3',sql_engine)
        plot_4_fig=time_series_generator(start_date,end_date,'plot_4',sql_engine)

    return plot_1_fig,plot_2_fig,plot_3_fig,plot_4_fig


if __name__ == "__main__":
    app.run(port=8080)
    sql_engine.dispose()
