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
import socket
import logging
import os
import pandas as pd


# local modules
from plot_generators import time_series_generator
from plot_generators import profile_generator
from credentials import sql_engine_string_generator

# set a local switch to speed the credentials try/except up
computer = socket.gethostname()
if computer == 'WONTN74902':
    fsdh = False
else:
    fsdh = True


url_prefix = "/app/AQPDBOR/"
# url_prefix = "/app/ARQPDEV/"

if fsdh:
    app = dash.Dash(__name__, 
                    # url_base_pathname=url_prefix, 
                    external_stylesheets=[dbc.themes.BOOTSTRAP],
                    suppress_callback_exceptions=True,            
                    requests_pathname_prefix=url_prefix,
                    routes_pathname_prefix=url_prefix
                    )
else:
    app = dash.Dash(__name__, 
                    url_base_pathname=url_prefix,
                    suppress_callback_exceptions=True
                    ) 


# configure a logger
logger = logging.getLogger("azure")
logger.setLevel(logging.DEBUG)

# Create a console handler
console_handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s | %(name)s | %(levelname)s | %(message)s')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# set up the sql connection string
DB_HOST = os.getenv('DATAHUB_PSQL_SERVER')
DB_USER = os.getenv('DATAHUB_PSQL_USER')
DB_PASS = os.getenv('DATAHUB_PSQL_PASSWORD')

logger.info('Credentials loaded locally')
logger.debug(f"{'DATAHUB_PSQL_SERVER'}: {DB_HOST}")
logger.debug(f"{'DATAHUB_PSQL_USER'}: {DB_USER}")

sql_engine_string=('postgresql://{}:{}@{}/{}?sslmode=require').format(DB_USER,DB_PASS,DB_HOST,'borden')

# set up the engine
sql_engine_string=sql_engine_string_generator('QP_SERVER','DATAHUB_PSQL_SERVER','DATAHUB_PSQL_USER','DATAHUB_PSQL_PASSWORD','borden',fsdh,logger)
sql_engine=create_engine(sql_engine_string,pool_pre_ping=True)

# MSG = " PYTHON START :: "

# sql_query="""SELECT column_name
# FROM information_schema.columns
# WHERE table_name = '{}'
# ORDER BY ordinal_position;""".format('bor__csat_v1__2024')
# try:
#     with sql_engine.connect() as connection:
#         message = "Connection successful!"
#         output=pd.read_sql_query(sql_query, connection)
# except OperationalError as e:
#     print(f"Connection failed: {e}")
#     message = f" :: An error occurred: {e}"


# set datetime parameters
first_date=dt.strftime(dt(dt.today().year, 1, 1),'%Y-%m-%d')

now=dt.today()
start_date=(now-td(days=7)).strftime('%Y-%m-%d')
end_date=now.strftime('%Y-%m-%d')
start_time=(now-td(hours=1)).strftime('%h:%m')


# ######## temporary html output to screen ######
# html_string = message

# app.layout = html.Div([
#     html.H1("Borden Table Columns"),
#     dash_table.DataTable(
#         data=output.to_dict('records'),
#         columns=[{"name": i, "id": i} for i in output.columns],
#         style_table={'overflowX': 'auto'},
#         style_cell={'textAlign': 'left'}
#     )
# ])



# set up the app layout
app.layout = html.Div(children=
                    [
                    html.H1('BORDEN DATA DASHBOARD', style={'textAlign': 'center'}),
                    html.H3('Pick the desired date range.  This will apply to all time plots on the page.'),
                    dcc.DatePickerRange(
                        id='date-picker',
                        min_date_allowed=first_date,
                        max_date_allowed=end_date,
                        display_format='YYYY-MM-DD'
                    ),
                    html.Br(),
                    html.A(html.Button('Borden CR3000 Temperatures Display', id='page1-btn', n_clicks=0),href='#plot_1'),
                    html.Br(),
                    html.A(html.Button('Borden CSAT Temperatures Display', id='page2-btn', n_clicks=0),href='#plot_2'),
                    html.Br(),
                    html.A(html.Button('Borden Gases Display', id='page3-btn', n_clicks=0),href='#plot_3'),
                    html.Br(),
                    html.A(html.Button('Borden Water Vapour Display', id='page4-btn', n_clicks=0),href='#plot_4'),
                    html.Br(),
                    html.A(html.Button('Borden Profile', id='page5-btn', n_clicks=0),href='#plot_5'),
                    html.Br(),
                    html.H2('Borden CR3000 Temperatures Display'),
                    html.A(id="anchor_1"),
                    dcc.Graph(id='plot_1',figure=time_series_generator(start_date,end_date,'plot_1',sql_engine,logger)),
                    html.Br(),
                    html.H2(children=['Borden CSAT Temperatures Display']),
                    html.Br(),
                    html.A(id="anchor_2"),
                    dcc.Graph(id='plot_2',figure=time_series_generator(start_date,end_date,'plot_2',sql_engine,logger)),
                    html.Br(),
                    html.H2('Borden Gases Display'),
                    html.Br(),
                    html.A(id="anchor_3"),
                    dcc.Graph(id='plot_3',figure=time_series_generator(start_date,end_date,'plot_3',sql_engine,logger)),
                    html.Br(),
                    html.H2(children=['Borden Water Vapour Display']),
                    html.A(id="anchor_4"),
                    dcc.Graph(id='plot_4',figure=time_series_generator(start_date,end_date,'plot_4',sql_engine,logger)),
                    html.Br(),
                    html.H2(children=['Borden Tower Measurements']),
                    ]
                    )
                    # html.A(id="anchor_5"),
                    # dcc.Graph(id='plot_5',figure=profile_generator('q_profile_last_available_cycle',sql_engine,logger)),
                    # ] 
                    # )

logger.info('plot generated')
# @app.callback(
#     Output('plot_1', 'figure'),
#     Output('plot_2', 'figure'),
#     Output('plot_3', 'figure'),
#     Output('plot_4', 'figure'),
#     Input('date-picker', 'start_date'),
#     Input('date-picker', 'end_date'))

# def update_output(start_date,end_date):
#     if not start_date or not end_date:
#         raise PreventUpdate
#     else:
#         logger.info('Updating plot')
#         plot_1_fig=time_series_generator(start_date,end_date,'plot_1',sql_engine)
#         plot_2_fig=time_series_generator(start_date,end_date,'plot_2',sql_engine)
#         plot_3_fig=time_series_generator(start_date,end_date,'plot_3',sql_engine)
#         plot_4_fig=time_series_generator(start_date,end_date,'plot_4',sql_engine)

#     return plot_1_fig,plot_2_fig,plot_3_fig,plot_4_fig

# sql_engine.dispose()


if fsdh:
    server = app.server
else: 
    if __name__ == "__main__":
        app.run(debug=True, port=8080)
