import dash
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, callback
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output
from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.exc import OperationalError
from datetime import datetime as dt
from datetime import timedelta as td
from datetime import timezone as tz
import socket
import logging
import os
# import pandas as pd
from dotenv import load_dotenv
# from packaging import version

# local modules
from plot_generators import time_series_generator
from plot_generators import profile_generator
from plot_generators import status_indicator
from get_server_environment import get_server_environment, create_dash_app

# set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(message)s"
)

logger = logging.getLogger(__name__)

host,path_prefix,parent_dir = get_server_environment(local_computer_name='wontn74902')

# parent_dir = os.getcwd()
# path_prefix = '/' + os.path.basename(os.path.normpath(parent_dir)) + '/'

# # set a local switch to select host environment
# computer = socket.gethostname().lower()
# if computer == 'wontn74902':
#     host = 'local'
# elif 'qpdata' in computer:
#     host = 'qpdata'
# elif 'sandbox' in computer:
#     host = 'sandbox'
# else:
#     host = 'fsdh'

# # display host info
# logging.basicConfig(level=logging.INFO)
# logger.info(f"Host environment detected: {host}")
# logger.info(f"parent path: {parent_dir}")
# print ( 'path_prefix: ' + path_prefix )

# set up the sql connection string
if host == 'fsdh':
    # Load OS environment variables
    DB_HOST = os.getenv('DATAHUB_PSQL_SERVER')
    DB_USER = os.getenv('DATAHUB_PSQL_USER')
    DB_PASS = os.getenv('DATAHUB_PSQL_PASSWORD')

else:
    # Load variables from .env into environment
    load_dotenv( parent_dir + '/.env', override=True)
    DB_HOST = os.getenv('QP_SERVER')
    DB_USER = os.getenv('QP_VIEWER_USER')
    DB_PASS = os.getenv('QP_VIEWER_PASSWORD')

# logger.info('Credentials loaded locally')
logger.debug(f"{'DATABASE_SERVER'}: {DB_HOST}")
#logger.debug(f"{'DATABASE_USER'}: {DB_USER}")

# set up the engine
sql_engine_string=('postgresql://{}:{}@{}/{}?sslmode=require').format(DB_USER,DB_PASS,DB_HOST,'borden')
try:
    sql_engine=create_engine(sql_engine_string,pool_pre_ping=True)
except Exception as e:
    error_occur = True
    print(f"An error occurred trying to create db connection: {e}")    

try:
    with sql_engine.connect() as connection:
        print("Connection successful!")
except OperationalError as e:
    print(f"Connection failed: {e}")

# set datetime parameters
first_date=dt.strftime(dt(dt.today().year, 1, 1),'%Y-%m-%d')

# establish default date range: last 7 days
now=dt.now(tz.utc)
start_dt=(now-td(days=7)).strftime('%Y-%m-%d %H:%M')
end_dt=now.strftime('%Y-%m-%d %H:%M')
start_time=(now-td(hours=1)).strftime('%h:%m')

# set up a generic button style
button_style = {
    "backgroundColor": "#e0f0ff",
    "borderRadius": "12px",
    "padding": "10px 24px",
    "border": "none",
    "color": "#333",
    "fontWeight": "bold",
    "boxShadow": "0 2px 6px rgba(0,0,0,0.07)"
}

# initialize the app based on host, specify the url_prefix if needed
app, server = create_dash_app(host, path_prefix, url_prefix="/app/AQPDBOR/")
# if host == 'fsdh':
#     url_prefix = "/app/AQPDBOR/"
#     app = dash.Dash(__name__,  
#                     requests_pathname_prefix=url_prefix,
#                     routes_pathname_prefix=url_prefix,
#                     external_stylesheets=[dbc.themes.BOOTSTRAP],
#                     suppress_callback_exceptions=True            
#                     )
#     server = app.server
# elif host == 'qpdata':
#     url_prefix = path_prefix
#     app = dash.Dash(__name__, 
#                     requests_pathname_prefix=url_prefix,
#                     external_stylesheets=[dbc.themes.BOOTSTRAP],
#                     suppress_callback_exceptions=True,
#                     eager_loading=True
#                     )
#     server = app.server
    
# else:
#     url_prefix = "/app/AQPDBOR/"
#     app = dash.Dash(__name__, 
#                     url_base_pathname=url_prefix,
#                     external_stylesheets=[dbc.themes.BOOTSTRAP],
#                     suppress_callback_exceptions=True
#                     ) 


# set up the app layout
app.layout = dbc.Container([
        html.Div(
        style={
            "backgroundImage": f"url('{app.get_asset_url('skyline.jpg')}')",
            "backgroundSize": "cover",
            "backgroundPosition": "center",
            "padding": "40px 0",
            "borderRadius": "12px",
            "marginBottom": "24px",
            "boxShadow": "0 2px 8px rgba(0,0,0,0.15)",
        },
        children=[
            html.H1(
                "BORDEN DATA DASHBOARD",
                style={
                    "textAlign": "center",
                    "color": "white",
                    "textShadow": "2px 2px 8px #333",
                    "margin": 0,
                },
            )
        ],
    ),

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
                html.Div([
                    html.H4('Pick the desired date range (UTC). This will apply to all time plots on the page.'),
                    dbc.Container([
                        dbc.Row([

                            # Start datetime
                            dbc.Col([
                                html.Label("Start Date-time", style={"fontWeight": "bold"}),

                                dbc.Row([
                                    dbc.Col(
                                        dcc.DatePickerSingle(
                                            id="start-date",
                                            display_format="YYYY-MM-DD",
                                            placeholder="Select date",
                                            style={"width": "100%"}
                                        ), width=3
                                    ),
                                    dbc.Col(
                                        dbc.Input(
                                            id="start-time",
                                            type="time",
                                            value="00:00",
                                            style={"width": "140px"}
                                        ), width=5
                                    )
                                ], className="g-2")  # spacing between date + time
                            ], width=6),

                            # End datetime
                            dbc.Col([
                                html.Label("End Date-time", style={"fontWeight": "bold"}),

                                dbc.Row([
                                    dbc.Col(
                                        dcc.DatePickerSingle(
                                            id="end-date",
                                            display_format="YYYY-MM-DD",
                                            placeholder="Select date",
                                            style={"width": "100%"}
                                        ), width=3
                                    ),
                                    dbc.Col(
                                        dbc.Input(
                                            id="end-time",
                                            type="time",
                                            value=dt.utcnow().strftime("%H:%M"),
                                            style={"width": "140px"}
                                        ), width=5
                                    )
                                ], className="g-2")
                            ], width=6),

                        ], justify="start", className="g-3")  # spacing between start/end blocks
                    ], fluid=True),
                    ],
                    style={
                        "border": "2px solid #b3d8ff",
                        "borderRadius": "12px",
                        "backgroundColor": "#f5fbff",
                        "padding": "24px",
                        "marginBottom": "24px",
                        "boxShadow": "0 2px 8px rgba(0,0,0,0.06)"
                    }
                ),
                html.Br(),
                html.Div(
                    html.A(
                        html.Button('Borden CR3000 Temperatures Display', id='page1-btn', n_clicks=0, style=button_style), href='#plot_1'
                    ),
                    style={"marginBottom": "18px"}  # vertical space after this button
                ),
                
                html.Div(
                    html.A(
                        html.Button('Borden CSAT Temperatures Display', id='page2-btn', n_clicks=0, style=button_style), href='#plot_2'
                    ),
                    style={"marginBottom": "18px"}  # vertical space after this button
                ),
                html.Div(
                    html.A(
                        html.Button('Borden Gases Display', id='page3-btn', n_clicks=0, style=button_style), href='#plot_3'
                    ),
                    style={"marginBottom": "18px"}  # vertical space after this button
                ),
                html.Div(
                    html.A(
                        html.Button('Borden Water Vapour Display', id='page4-btn', n_clicks=0, style=button_style), href='#plot_4'
                    ),
                    style={"marginBottom": "18px"}  # vertical space after this button
                ),
                html.Div(
                    html.A(
                        html.Button('Borden Tower Profiles', id='page5-btn', n_clicks=0, style=button_style), href='#plot_5'
                    ),
                    style={"marginBottom": "18px"}  # vertical space after this button
                ),
                html.Br(),
                html.H3('Borden Time Series Plots', style={"textAlign": "center"}),
                dcc.Graph(id='plot_1', figure=time_series_generator(start_dt, end_dt, 'plot_1', sql_engine)),
                html.Br(),
                # html.H2('Borden CSAT Temperatures Display'),
                dcc.Graph(id='plot_2', figure=time_series_generator(start_dt, end_dt, 'plot_2', sql_engine)),
                html.Br(),
                # html.H2('Borden Gases Display'),
                dcc.Graph(id='plot_3', figure=time_series_generator(start_dt, end_dt, 'plot_3', sql_engine)),
                html.Br(),
                # html.H2('Borden Water Vapour Display'),
                dcc.Graph(id='plot_4', figure=time_series_generator(start_dt, end_dt, 'plot_4', sql_engine)),
                html.Br(),
                html.H3('Borden Tower Measurements', style={"textAlign": "center"}),
                dcc.Graph(id='plot_5')
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
## end of app.layout

logger.info('plot generated')

# Callbacks for interactivity
@app.callback(
    Output('plot_1', 'figure'),
    Output('plot_2', 'figure'),
    Output('plot_3', 'figure'),
    Output('plot_4', 'figure'),
    Input("start-date", "date"),
    Input("start-time", "value"),
    Input("end-date", "date"),
    Input("end-time", "value")
)

# update time series plots based on date range inputs
def update_output(start_date, start_time, end_date, end_time):
    if not start_date or not start_time or not end_date or not end_time:
        raise PreventUpdate

    # Combine into UTC datetime objects
    start_dt = dt.strptime(f"{start_date} {start_time}", "%Y-%m-%d %H:%M").replace(tzinfo=tz.utc)
    end_dt   = dt.strptime(f"{end_date} {end_time}", "%Y-%m-%d %H:%M").replace(tzinfo=tz.utc)

    # Call your plot generator functions with UTC datetimes
    plot_1_fig = time_series_generator(start_dt, end_dt, "plot_1", sql_engine)
    plot_2_fig = time_series_generator(start_dt, end_dt, "plot_2", sql_engine)
    plot_3_fig = time_series_generator(start_dt, end_dt, "plot_3", sql_engine)
    plot_4_fig = time_series_generator(start_dt, end_dt, "plot_4", sql_engine)

    return plot_1_fig, plot_2_fig, plot_3_fig, plot_4_fig

# Callback to update plot_5 every minute
@app.callback(
    Output('plot_5', 'figure'),
    Input('interval-component', 'n_intervals')
)
# update plot_5 periodically
def update_plot_5(n_intervals):
    # You could add more live controls/inputs if you wish here
    # Re-generate plot_5 using latest data from SQL
    fig = profile_generator('q_profile_last_available_cycle', sql_engine)
    return fig

# Run the app
if __name__ == "__main__":
    app.run(debug=False,port=8080)
    sql_engine.dispose()
