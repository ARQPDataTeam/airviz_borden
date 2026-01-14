# this function differentiates host environments

import socket
import logging
import os
import dash
import dash_bootstrap_components as dbc
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

def get_host_environment(local_computer_name):

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

def get_credentials(parent_dir):
    try:
        # Load variables from local .env into environment
        load_dotenv(parent_dir + '/.env', override=True)
        COMPUTER = os.getenv('COMPUTER')
        DB_SERVER = os.getenv('SERVER')
        DB_USER = os.getenv('VIEWER_USER')
        DB_PASS = os.getenv('VIEWER_PASSWORD')
        DB_NAME = os.getenv('DATABASE')
        URL_PREFIX = os.getenv('URL_PREFIX')   

    except Exception as e:
        logger.error(f"Error loading .env file: {e}")
        # Load OS environment variables
        DB_SERVER = os.getenv('SERVER')
        DB_USER = os.getenv('VIEWER_USER')
        DB_PASS = os.getenv('VIEWER_PASSWORD')
        DB_NAME = os.getenv('DATABASE')
        URL_PREFIX = os.getenv('URL_PREFIX')

    # logger.info('Credentials loaded locally')
    logger.debug(f"{'DATABASE_SERVER'}: {DB_SERVER}")
    logger.debug(f"{'DATABASE_USER'}: {DB_USER}")
    logger.debug(f"{'DATABASE_NAME'}: {DB_NAME}")

    return COMPUTER, DB_SERVER, DB_USER, DB_PASS, DB_NAME, URL_PREFIX

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
