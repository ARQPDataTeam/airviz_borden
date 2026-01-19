
# Dash data extraction and reporting repo.  The app is configured with a home page that is navigated by anchor buttons.  It also has a profile plot comprised of the most recent hour's data.

The app structure uses a common host/credentials module that requires the computer name and URL prefix as keyword arguments stored in the .env file like all the other credential information.  Credential keys are now the same for all environments. All workspaces and .env files will need the following keys:
COMPUTER, SERVER, VIEWER_USER, VIEWER_PASSWORD, EDITOR_USER, EDITOR_PASSWORD, DATABASE, URL_PREFIX

This project uses Dash (https://dash.plotly.com/) 

Documentation for Plotly can be found here:
https://plotly.com/python/plotly-express/

No need to describe the how-to's here, the documentation will do a much better job.

## CSAT
This instrument measures relative component winds and virtual temperature.

## G2401
This instrument (Picarro) measures CO, CO2, CH4 and H2O.

