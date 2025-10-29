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
# from packaging import version
import base64
from flask import Flask

# local modules
from plot_generators import time_series_generator
from plot_generators import profile_generator
from plot_generators import status_indicator

# Create the underlying Flask app
server = Flask(__name__)

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
            server=server,  
            requests_pathname_prefix=url_prefix,
            external_stylesheets=[dbc.themes.BOOTSTRAP],
            suppress_callback_exceptions=True
            ) 

# # set up Dash server
# server = app.server

logging.basicConfig(
    level=logging.DEBUG,
    format="%(message)s"
)

logger = logging.getLogger(__name__)

logger.debug('app.y START')

# Load variables from .env into environment
load_dotenv()
DB_HOST = os.getenv('QP_SERVER')
DB_USER = os.getenv('QP_VIEWER_USER')
DB_PASS = os.getenv('QP_VIEWER_PASSWORD')

# logger.info('Credentials loaded locally')
# logger.debug(f"{'DATABASE_SERVER'}: {DB_HOST}")
# logger.debug(f"{'DATABASE_USER'}: {DB_USER}")

# set up the engine
sql_engine_string=('postgresql://{}:{}@{}/{}?sslmode=require').format(DB_USER,DB_PASS,DB_HOST,'borden')
sql_engine=create_engine(sql_engine_string,pool_pre_ping=True)

now=dt.now(tz.utc)
start_dt=(now-td(days=7)).strftime('%Y-%m-%d %H:%M')
end_dt=now.strftime('%Y-%m-%d %H:%M')
start_time=(now-td(hours=1)).strftime('%h:%m')

# sound_filename =  'assets/loop.mp3'
# encoded_sound = base64.b64encode(open(sound_filename, 'rb').read())

# set up a generic button style
# button_style = {
#     "backgroundColor": "#e0f0ff",
#     "borderRadius": "12px",
#     "padding": "10px 24px",
#     "border": "none",
#     "color": "#333",
#     "fontWeight": "bold",
#     "boxShadow": "0 2px 6px rgba(0,0,0,0.07)"
# }

# set up the app layout
app.layout = dbc.Container([
    #     html.Div(
    #     style={
    #         "backgroundImage": f"url('{app.get_asset_url('skyline.jpg')}')",
    #         "backgroundSize": "cover",
    #         "backgroundPosition": "center",
    #         "padding": "40px 0",
    #         "borderRadius": "12px",
    #         "marginBottom": "24px",
    #         "boxShadow": "0 2px 8px rgba(0,0,0,0.15)",
    #     },
    #     children=[
    #         html.H1(
    #             "BORDEN DATA DASHBOARD",
    #             style={
    #                 "textAlign": "center",
    #                 "color": "white",
    #                 "textShadow": "2px 2px 8px #333",
    #                 "margin": 0,
    #             },
    #         )
    #     ],
    # ),

    dbc.Row([
        # dbc.Col(  # LEFT: Status Indicator (2/12 width)
        #     status_indicator('status_indicator', sql_engine),  # your function
        #     width=2,
        #     style={
        #         'backgroundColor': '#f8f9fa',
        #         'padding': '10px',
        #         'borderRight': '1px solid #dee2e6',
        #         'height': '100vh',
        #         'overflowY': 'auto'
        #     }
        # ),
        dbc.Col(  # RIGHT: Main Dashboard (10/12 width)
            html.Div([
                html.Br(),
                html.H3('Borden Tower Profile', style={"textAlign": "center"}),
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
    Output('plot_5', 'figure'),
    Input("start-date", "date"),
    Input("start-time", "value"),
    Input("end-date", "date"),
    Input("end-time", "value")
)

    # html.Audio(id='audio-player', src='data:audio/mpeg;base64,{}'.format(encoded_sound.decode()),
    #                       controls=True,
    #                       autoPlay=False,
    #                       hidden=True
    #                       ),    

# def play( end_date ):
#     if end_date:
#         return html.Audio(src='data:audio/mpeg;base64,{}'.format(encoded_sound.decode()),
#                           controls=False,
#                           autoPlay=True,
#                           )

def update_output(start_date, start_time, end_date, end_time):

    if not start_date or not start_time or not end_date or not end_time:
        logger.info('update_output : PreventUpdate')
        raise PreventUpdate

    logger.info('update_output')

    # Combine into UTC datetime objects
    start_dt = dt.strptime(f"{start_date} {start_time}", "%Y-%m-%d %H:%M").replace(tzinfo=tz.utc)
    end_dt   = dt.strptime(f"{end_date} {end_time}", "%Y-%m-%d %H:%M").replace(tzinfo=tz.utc)

    # Call your plot generator functions with UTC datetimes
    # plot_1_fig = time_series_generator(start_dt, end_dt, "plot_1", sql_engine)
    # plot_2_fig = time_series_generator(start_dt, end_dt, "plot_2", sql_engine)
    # plot_3_fig = time_series_generator(start_dt, end_dt, "plot_3", sql_engine)
    # plot_4_fig = time_series_generator(start_dt, end_dt, "plot_4", sql_engine)

    profile_fig = profile_generator('q_profile_last_available_cycle', sql_engine)

    # return plot_1_fig, plot_2_fig, plot_3_fig, plot_4_fig

if __name__ == "__main__":
    
    if local:
        app.run(debug=False, port=8080)
    # else:
    #     app.run_server(debug=False)
    sql_engine.dispose()

# Expose the Flask server for mod_wsgi
application = app.server

logger.debug('app.y END')