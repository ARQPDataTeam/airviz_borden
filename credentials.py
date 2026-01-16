# this function differentiates host environments

import socket
import logging
import os
import dash
import dash_bootstrap_components as dbc
from dotenv import load_dotenv
from pathlib import Path

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
    env_path = Path(parent_dir) / ".env"

    # 1. Try loading .env if it exists
    if env_path.exists():
        load_dotenv(env_path, override=True)
        source = ".env file"
    else:
        source = "OS environment"

    # 2. Read variables from environment (same code path either way)
    COMPUTER   = os.getenv("COMPUTER")
    DB_SERVER = os.getenv("SERVER")
    VIEWER = os.getenv("VIEWER")
    VIEWER_PWD   = os.getenv("VIEWER_PWD")
    EDITOR = os.getenv("EDITOR")
    EDITOR_PWD   = os.getenv("EDITOR_PWD")
    DB_NAME   = os.getenv("DATABASE")
    URL_PREFIX= os.getenv("URL_PREFIX")

    # 3. Validate
    vars_dict = {
        "COMPUTER": COMPUTER,
        "SERVER": DB_SERVER,
        "VIEWER": VIEWER,
        "VIEWER_PWD": VIEWER_PWD,
        "EDITOR": EDITOR,
        "EDITOR_PWD": EDITOR_PWD,
        "DATABASE": DB_NAME,
        "URL_PREFIX": URL_PREFIX,
    }

    missing = [name for name, value in vars_dict.items() if not value]

    if missing:
        raise ValueError(
            f"Missing environment variables ({source}): {', '.join(missing)}"
        )

    logger.info(f"Credentials loaded from {source}")
    logger.debug(f"DATABASE_SERVER: {DB_SERVER}")
    logger.debug(f"DATABASE_USER: {VIEWER}")
    
    logger.debug(f"DATABASE_NAME: {DB_NAME}")


    return COMPUTER, DB_SERVER, VIEWER, VIEWER_PWD, EDITOR, EDITOR_PWD, DB_NAME, URL_PREFIX

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
