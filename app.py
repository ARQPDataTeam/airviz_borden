import dash
from dash import Dash, html, dcc, callback 
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from sqlalchemy import create_engine
from sqlalchemy import text
from datetime import datetime as dt
from datetime import timedelta as td


# local modules
from plot_generators import time_series_generator
from plot_generators import profile_generator
from credentials import sql_engine_string_generator


url_prefix = "/app/AQPDBOR/"
app = dash.Dash(__name__, url_base_pathname=url_prefix, external_stylesheets=[dbc.themes.BOOTSTRAP])
# generate the sql connection string
sql_engine_string=sql_engine_string_generator('QP_SERVER','DATAHUB_PSQL_SERVER','DATAHUB_PSQL_USER','DATAHUB_PSQL_PASSWORD','borden')
sql_engine=create_engine(sql_engine_string)

# set datetime parameters
first_date=dt.strftime(dt(dt.today().year, 1, 1),'%Y-%m-%d')

now=dt.today()
start_date=(now-td(days=7)).strftime('%Y-%m-%d')
end_date=now.strftime('%Y-%m-%d')
start_time=(now-td(hours=1)).strftime('%h:%m')


######## temporary html output to screen ######
html_string = "<h2 style='color:green;'>This is rendered HTML</h2><p>{sql_engine_string}</p>"

app.layout = html.Div([
    html.Div(dangerouslySetInnerHTML={'__html': html_string})
])
"""
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
                    dcc.Graph(id='plot_1',figure=time_series_generator(start_date,end_date,'plot_1',sql_engine)),
                    html.Br(),
                    html.H2(children=['Borden CSAT Temperatures Display']),
                    html.Br(),
                    html.A(id="anchor_2"),
                    dcc.Graph(id='plot_2',figure=time_series_generator(start_date,end_date,'plot_2',sql_engine)),
                    html.Br(),
                    html.H2('Borden Gases Display'),
                    html.Br(),
                    html.A(id="anchor_3"),
                    dcc.Graph(id='plot_3',figure=time_series_generator(start_date,end_date,'plot_3',sql_engine)),
                    html.Br(),
                    html.H2(children=['Borden Water Vapour Display']),
                    html.A(id="anchor_4"),
                    dcc.Graph(id='plot_4',figure=time_series_generator(start_date,end_date,'plot_4',sql_engine)),
                    html.Br(),
                    html.H2(children=['Borden Tower Measurements']),
                    html.A(id="anchor_5"),
                    dcc.Graph(id='plot_5',figure=profile_generator('q_profile_last_available_cycle',sql_engine)),
                    # html.H3('Pick the desired date range.  This will apply to all time plots on the page.'),
                    # dcc.DatePickerRange(
                    #     id='profile_date-picker',
                    #     min_date_allowed=first_date,
                    #     max_date_allowed=end_date,
                    #     display_format='YYYY-MM-DD'
                    # ),
                    ] 
                    )

print ('plot generated')
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
        print ('Updating plot')
        plot_1_fig=time_series_generator(start_date,end_date,'plot_1',sql_engine)
        plot_2_fig=time_series_generator(start_date,end_date,'plot_2',sql_engine)
        plot_3_fig=time_series_generator(start_date,end_date,'plot_3',sql_engine)
        plot_4_fig=time_series_generator(start_date,end_date,'plot_4',sql_engine)

    return plot_1_fig,plot_2_fig,plot_3_fig,plot_4_fig
"""
# sql_engine.dispose()
if __name__ == "__main__":
    app.run(debug=True, port=8080)
