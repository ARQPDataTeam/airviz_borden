# this function differentiates server environments

import socket
import logging
import os
import dash
import dash_bootstrap_components as dbc

logger = logging.getLogger(__name__)

def get_server_environment(local_computer_name):
    parent_dir = os.getcwd()
    path_prefix = '/' + os.path.basename(os.path.normpath(parent_dir)) + '/'

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
    logger.info(f"parent path: {parent_dir}")
    print ( 'path_prefix: ' + path_prefix ) 
    return host,path_prefix,parent_dir 

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

    else:
        app = dash.Dash(
            __name__,
            url_base_pathname=url_prefix,
            external_stylesheets=[dbc.themes.BOOTSTRAP],
            suppress_callback_exceptions=True
        )

    logger.info(f"url_prefix: {url_prefix}")
    return app, app.server
