# this function differentiates server environments

import socket
import logging
import os
import dash
import dash_bootstrap_components as dbc
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

def get_server_environment(local_computer_name):

    # set a local switch to select host environment
    computer = socket.gethostname().lower()
    if computer == local_computer_name:
        host = 'local'
    elif 'qpdata' in computer:
        host = 'qpdata'
    elif 'sandbox' in computer:
        host = 'sandbox'
    else:
        host = 'fsdh'

    # display host info
    logging.basicConfig(level=logging.INFO)
    logger.info(f"Host environment detected: {host}")

    return host

def credentials(host,parent_dir):
    if host == 'fsdh':
        # Load OS environment variables
        DB_HOST = os.getenv('DATAHUB_PSQL_SERVER')
        DB_USER = os.getenv('DATAHUB_PSQL_USER')
        DB_PASS = os.getenv('DATAHUB_PSQL_PASSWORD')
        DB_NAME = os.getenv('DATAHUB_PSQL_DBNAME')

    else:
        # Load variables from .env into environment
        load_dotenv( parent_dir + '/.env', override=True)
        DB_HOST = os.getenv('QP_SERVER')
        DB_USER = os.getenv('QP_VIEWER_USER')
        DB_PASS = os.getenv('QP_VIEWER_PASSWORD')
        DB_NAME = os.getenv('QP_DATABASE')
    
    # logger.info('Credentials loaded locally')
    logger.debug(f"{'DATABASE_SERVER'}: {DB_HOST}")
    logger.debug(f"{'DATABASE_USER'}: {DB_USER}")
    logger.debug(f"{'DATABASE_NAME'}: {DB_NAME}")

    return DB_HOST, DB_USER, DB_PASS, DB_NAME

def create_dash_app(host, path_prefix, url_prefix):
    if host == "fsdh":
        app = dash.Dash(
            __name__,
            requests_pathname_prefix=url_prefix,
            routes_pathname_prefix=url_prefix,
            external_stylesheets=[dbc.themes.BOOTSTRAP],
            suppress_callback_exceptions=True
        )

    elif host == "qpdata":
        url_prefix = path_prefix
        app = dash.Dash(
            __name__,
            requests_pathname_prefix=url_prefix,
            external_stylesheets=[dbc.themes.BOOTSTRAP],
            suppress_callback_exceptions=True,
            eager_loading=True
        )

    elif host == "sandbox":
        url_prefix = path_prefix
        app = dash.Dash(
            __name__,
            requests_pathname_prefix=url_prefix,
            external_stylesheets=[dbc.themes.BOOTSTRAP],
            suppress_callback_exceptions=True,
            eager_loading=True
        )

    else:
        app = dash.Dash(
            __name__,
            url_base_pathname=url_prefix,
            external_stylesheets=[dbc.themes.BOOTSTRAP],
            suppress_callback_exceptions=True
        )

    logger.info(f"url_prefix: {url_prefix}")
    return app, app.server
