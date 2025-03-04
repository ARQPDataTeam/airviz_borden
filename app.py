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
from postgres_query import fig_generator
from credentials import sql_engine_string_generator


url_prefix = "/app/AQPDBOR/"
app = dash.Dash(__name__, url_base_pathname=url_prefix, external_stylesheets=[dbc.themes.BOOTSTRAP])
# generate the sql connection string
sql_engine_string=sql_engine_string_generator('QP_SERVER','DATAHUB_PSQL_USER','DATAHUB_PSQL_PASSWORD','borden')
sql_engine=create_engine(sql_engine_string)

# set datetime parameters
now=dt.today()
start_date=(now-td(days=1)).strftime('%Y-%m-%d')
end_date=now.strftime('%Y-%m-%d')

# set datetime parameters
first_date=dt.strftime(dt(dt.today().year, 1, 1),'%Y-%m-%d')

now=dt.today()
start_date=(now-td(days=7)).strftime('%Y-%m-%d')
end_date=now.strftime('%Y-%m-%d')

# set up the app layout
app.layout = html.Div(children=
                    [
                    html.H1('BORDEN DATA DASHBOARD', style={'textAlign': 'center'}),
                    html.H3('Pick the desired date range.  This will apply to all plots on the page.'),
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
                    html.H2('Borden CR3000 Temperatures Display'),
                    html.A(id="plot_1"),
                    dcc.Graph(id='plot_1',figure=fig_generator(start_date,end_date,'plot_1',sql_engine)),
                    html.Br(),
                    html.H2(children=['Borden CSAT Temperatures Display']),
                    html.Br(),
                    html.A(id="plot_2"),
                    dcc.Graph(id='plot_2',figure=fig_generator(start_date,end_date,'plot_2',sql_engine)),
                    html.Br(),
                    html.H2('Borden Gases Display'),
                    html.Br(),
                    html.A(id="plot_3"),
                    dcc.Graph(id='plot_3',figure=fig_generator(start_date,end_date,'plot_3',sql_engine)),
                    html.Br(),
                    html.H2(children=['Borden Water Vapour Display']),
                    html.A(id="plot_4"),
                    dcc.Graph(id='plot_4',figure=fig_generator(start_date,end_date,'plot_4',sql_engine)),
                    ] 
                    )

print ('plot generated')
@app.callback(
    Output('plot_1', 'figure'),
    Output('plot_2', 'figure'),
    Input('date-picker', 'start_date'),
    Input('date-picker', 'end_date'))

def update_output(start_date,end_date):
    if not start_date or not end_date:
        raise PreventUpdate
    else:
        print ('Updating plot')
        plot_1_fig=fig_generator(start_date,end_date,'plot_1',sql_engine_string)
        plot_2_fig=fig_generator(start_date,end_date,'plot_2',sql_engine_string)
    return plot_1_fig,plot_2_fig

sql_engine.dispose()
if __name__ == "__main__":
    app.run(debug=True, port=8080)
