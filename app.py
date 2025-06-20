from dash import Dash, html, dcc 
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
# import pandas as pd
# import numpy as np
from sqlalchemy import create_engine,text
from credentials import sql_engine_string_generator
from flask import request
from datetime import datetime
# from azure.identity import DefaultAzureCredential
# from azure.keyvault.secrets import SecretClient
import os
from dotenv import load_dotenv 
import logging

# Version number to display
version = "1.3"

# Setup logger
if not os.path.exists('logs'):
    os.mkdir('logs')
    
logging.basicConfig(
    format = '%(message)s',
    filename='logs/log.log', 
    filemode='w+',
    level = 20)

#logging.getLogger("azure").setLevel(logging.ERROR)
logging.getLogger("azure").setLevel(logging.DEBUG)

#initialize the dash app as 'app'
app = Dash(__name__,
            external_stylesheets=[dbc.themes.SLATE],
            requests_pathname_prefix="/app/AQPDBOR/",
            routes_pathname_prefix="/app/AQPDBOR/")
# app = Dash(__name__,
#             external_stylesheets=[dbc.themes.SLATE])

# Global variable to store headers
request_headers = {}

print ( 'python print: DATAHUB_PSQL_SERVER' )

# # Get connection string
# sql_engine_string=sql_engine_string_generator('DATAHUB_PSQL_SERVER','DATAHUB_SWAPIT_DBNAME','DATAHUB_PSQL_EDITUSER','DATAHUB_PSQL_EDITPASSWORD')
# swapit_sql_engine=create_engine(sql_engine_string)

#sql_engine_string=sql_engine_string_generator('DATAHUB_PSQL_SERVER','dcp','DATAHUB_PSQL_USER','DATAHUB_PSQL_PASSWORD')
# dcp_sql_engine=create_engine(sql_engine_string)

MSG = " PYTHON START\n"

try:
    DB_HOST = os.getenv('DATAHUB_PSQL_SERVER')
    DB_USER = os.getenv('DATAHUB_PSQL_USER')
    DB_PASS = os.getenv('DATAHUB_PSQL_PASSWORD')

    # set the key vault path
    # KEY_VAULT_URL = "https://fsdh-proj-aqpd-prd-kv.vault.azure.net/"
    # error_occur = False

    # # Retrieve the secrets containing DB connection details
    # credential = DefaultAzureCredential()
    # secret_client = SecretClient(vault_url=KEY_VAULT_URL, credential=credential)

    # # Retrieve the secrets containing DB connection details
    # DB_HOST = secret_client.get_secret('DATAHUB_PSQL_SERVER').value
    # DB_USER = secret_client.get_secret('DATAHUB_PSQL_USER').value
    # DB_PASS = secret_client.get_secret('DATAHUB_PSQL_PASSWORD').value
    # print ('Credentials loaded from FSDH')
    MSG += "DB_HOST: "
    MSG += DB_HOST
    MSG += " :: \n"
    MSG += "DB_USER: "
    MSG += DB_USER
    MSG += " :: \n"

except Exception as e:
    # declare FSDH keys exception
    error_occur = True
    print(f"An error occurred: {e}")
    MSG += f"An error occurred: {e}\n"

print ( 'python print: after kv try' )

# for secret_properties in secret_client.list_properties_of_secrets():
#     print(secret_properties.name)

## + secret_client.list_properties_of_secrets()
app.layout = [ html.Div(children= MSG ) ]

print ( 'python print: after app layout' )

server = app.server 
# if __name__=='__main__':
#     app.run_server(debug=True,port=8080)

print ( 'python print: after app loaded' )