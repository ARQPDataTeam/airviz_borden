import pandas as pd
from ast import literal_eval
from dash import html
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sqlalchemy import text
from datetime import datetime as dt
from datetime import timezone as tz
import re
import logging

logger = logging.getLogger(__name__)

def time_series_generator(start_date,end_date,sql_query,sql_engine):
    

    # set the path to the sql folder
    sql_path='assets/sql_queries/'

    # load the plotting properties
    plotting_properties_df=pd.read_csv(sql_path+'plotting_inputs.txt', index_col=0, sep=';', converters={"axis_list": literal_eval})
    plot_title=plotting_properties_df.loc[sql_query,'plot_title']
    y_title_1=plotting_properties_df.loc[sql_query,'y_title_1']
    y_title_2=plotting_properties_df.loc[sql_query,'y_title_2']
    axis_list=list(plotting_properties_df.loc[sql_query,'axis_list'])
    secondary_y_flag=plotting_properties_df.loc[sql_query,'secondary_y_flag']
    
    # load the sql query
    filename=sql_query+'.sql'
    filepath=sql_path+filename
    with open(filepath,'r') as f:
        sql_query=f.read()

    # sql query
    sql_query=(sql_query).format(start_date,end_date)
    # logger.debug(sql_query)
    
    with sql_engine.connect() as conn:
    # create the dataframes from the sql query
        output_df=pd.read_sql_query(sql_query, conn)
    # set a datetime index
    output_df.set_index('datetime', inplace=True)
    output_df.index=pd.to_datetime(output_df.index)

    # plot a scatter chart by specifying the x and y values
    # Use add_trace function to specify secondary_y axes.
    def create_figure (df_index, df,plot_title,y_title_1,y_title_2,df_columns,axis_list,secondary_y_flag):
        plot_color_list=['black','blue','red','green','orange','yellow','brown','violet','turquoise','pink','olive','magenta','lightblue','purple']
        fig = make_subplots(specs=[[{"secondary_y": secondary_y_flag}]])
        # fig = make_subplots()
        for i,column in enumerate(df_columns):
            if secondary_y_flag:
                fig.add_trace(
                    go.Scatter(x=df_index, y=df[column], name=column, line_color=plot_color_list[i]),
                    secondary_y=axis_list[i])
            else:
                fig.add_trace(
                    go.Scatter(x=df_index, y=df[column], name=column, line_color=plot_color_list[i]))
 
        if secondary_y_flag: 
            # set axis titles
            fig.update_layout(
                template='seaborn',
                title=plot_title,
                xaxis_title="Date",
                yaxis_title=y_title_1,
                yaxis2_title=y_title_2,
                legend=dict(
                y=0.99
                )   
            )
        else:
            fig.update_layout(
                template='seaborn',
                title=plot_title,
                xaxis_title="Date",
                yaxis_title=y_title_1,
                legend=dict(
                y=0.99
                )   
            )
        return fig

    fig=create_figure(output_df.index,output_df,plot_title,y_title_1,y_title_2,output_df.columns,axis_list,secondary_y_flag)
    return fig

def profile_generator(sql_query,sql_engine):

    # set the path to the sql folder
    sql_path='assets/sql_queries/'

    # load the sql query
    filename=sql_query+'.sql'
    filepath=sql_path+filename
    with open(filepath,'r') as f:
        sql_query=f.read()

    sql_time_query = """
    WITH time_bounds AS (
        SELECT 
            to_char(max(datetime)::timestamp - INTERVAL '1 hour', 'YYYY-MM-DD HH24:MI') AS start_time,
            to_char(max(datetime)::timestamp, 'YYYY-MM-DD HH24:MI') AS end_time
        FROM bor__profile_v0
    )
    SELECT * FROM time_bounds;
    """

    with sql_engine.connect() as conn:
    # create the dataframes from the sql query
        output_df=pd.read_sql_query(sql_query, conn)
        result = conn.execute(text(sql_time_query)).fetchone()

    # Access as tuple or named columns
    start_time, end_time = result[0], result[1]

    if start_time is None or end_time is None:
        profile_title = "Average Borden Tower Concentration Profiles (time range unavailable)"
    else:
        profile_title = f"Average Borden Tower Concentration Profiles From {start_time} to {end_time}"
    
    # logger.debug("\noutput:\n%s", output_df)

    output_df.index = [1,5,16,26,33,42]
    output_df.index = output_df.index.astype(float)  # height as float

    temp_cols = [col for col in output_df.columns if 'temp' in col]
    temp_df = output_df[temp_cols].mean(axis=0)

    logger.debug(temp_df)

    # Reindex with int depths
    temp_df.index = [int(re.search(r'(\d+)m', item).group(1)) for item in temp_df.index]
    
    # Transpose: heights become rows, species become columns
    temp_df = temp_df.T

    temp_df.reindex

    logger.debug("\ntemp df:\n%s", temp_df)

    # Separate species into primary and secondary
    o3_species = [ 'o3' ]
    co2_species = ['lic_co2', 'lgr_co2', 'pic_co2']
    ch4_species = ['pic_ch4', 'lgr_co']
    h2o_species = ['lgr_h2o', 'lic_h2o', 'pic_h2o']
    ocs_species = ['lgr_ocs']

    # sub-select the dataframe into smaller sets organized by concentration scale
    o3_df=output_df[o3_species]
    co2_df=output_df[co2_species]
    ch4_df=output_df[ch4_species]
    h2o_df=output_df[h2o_species]
    h2o_df = output_df[h2o_species].copy()
    h2o_df['pic_h2o'] *= 10  # scale
    ocs_df = output_df[ocs_species]

    # set a colour list
    plot_color_list=['black','blue','red','green','orange','yellow','brown','violet','turquoise','pink','olive','magenta','lightblue','purple']

    # create the fig properties
    fig = make_subplots(rows=1, cols=6, column_widths=6*[0.16], shared_yaxes=False)

    # === PANEL 1 CH4 and CO ===
    fig.add_trace(go.Scatter(
        x=o3_df['o3'],
        y=o3_df.index,
        mode='lines+markers',
        line=dict(color=plot_color_list[0]),
        name='O3 (ppbv)',
        legendgroup='panel1',
        showlegend=True
    ), row=1, col=1)

    # === PANEL 2 CO2 group ===
    for i, species in enumerate(co2_species):
        # print (co2_df[species])
        fig.add_trace(go.Scatter(
            x=co2_df[species],
            y=co2_df.index,
            mode='lines+markers',
            line=dict(color=plot_color_list[i+1]),
            name=species,
            # xaxis='x',
            legendgroup='panel2',
            showlegend=True
        ), row=1, col=2)

    # === PANEL 3 CH4 group ===
    for i, species in enumerate(ch4_species):
        # print (ch4_df[species])
        fig.add_trace(go.Scatter(
            x=ch4_df[species],
            y=ch4_df.index,
            mode='lines+markers',
            line=dict(color=plot_color_list[i+3]),
            name=species,
            # xaxis='x2',
            legendgroup='panel3',
            showlegend=True
        ), row=1, col=3)

    # === PANEL 4 H2O group ===
    for i, species in enumerate(h2o_species):
        # print (h2o_df[species])
        fig.add_trace(go.Scatter(
            x=h2o_df[species],
            y=h2o_df.index,
            mode='lines+markers',
            line=dict(color=plot_color_list[i]),
            name=species,
            # xaxis='x3',
            legendgroup='panel4',
            showlegend=True
        ), row=1, col=4)

    # === PANEL 5 OCS ===
    fig.add_trace(go.Scatter(
        x=ocs_df['lgr_ocs'],
        y=ocs_df.index,
        mode='lines+markers',
        line=dict(color=plot_color_list[3]),
        name='OCS_LGR (pptv)',
        # xaxis='x4',
        legendgroup='panel5',
        showlegend=True
    ), row=1, col=5)

    # === PANEL 6 TEMP ===
    fig.add_trace(go.Scatter(
        x=temp_df,
        y=temp_df.index,
        mode='lines+markers',
        line=dict(color=plot_color_list[0]),
        name='Temperature (C)',
        # xaxis='x4',
        legendgroup='panel6',
        showlegend=True
    ), row=1, col=6)


    # === Layout for all x-axes ===
    fig.update_layout(
        height=600,
        title=(profile_title),
        title_x=0.5,  # Center the title horizontally

    # X-Axes
        xaxis=dict(title='O3 (ppbv)', side='bottom'),  # col=1
        xaxis2=dict(title='CO2 (ppmv)', side='bottom'),  # col=2
        xaxis3=dict(title='CH4 / CO (ppmv)', side='bottom'),  # col=3
        xaxis4=dict(title='H2O (ppthv)', side='bottom'),  # col=4
        xaxis5=dict(title='OCS (ppthv)', side='bottom'),  # col=5
        xaxis6=dict(title='Temperature (C)', side='bottom'),  # col=6

        # Position legend to the right of all 3 panels
            legend=dict(
                x=1.05,
                y=1,
                tracegroupgap=20
            ),
            )

    # return the fig
    return fig

# a function that returns a boolean set from an sql query
def status_indicator(sql_query,sql_engine,component_id='instrument-status-table'):

    # set the path to the sql folder
    sql_path='assets/sql_queries/'

    # load the sql query
    filename=sql_query+'.sql'
    filepath=sql_path+filename
    with open(filepath,'r') as f:
        sql_query=f.read()

    with sql_engine.connect() as conn:
    # create the dataframes from the sql query
        status_df = pd.read_sql_query(sql_query, conn)

    status_df.set_index('source', drop=True, inplace=True)
    # Ensure 'last_datetime' is a datetime dtype
    status_df['last_datetime'] = pd.to_datetime(status_df['last_datetime'])

    # Get current time in GMT (UTC)
    now = dt.now(tz.utc)

    # Function to classify status
    def get_status(last_time):
        delta_hours = (now - last_time).total_seconds() / 3600
        if delta_hours < 1.5:
            return 'green'
        elif 1.5 <= delta_hours <= 24:
            return 'yellow'
        else:
            return 'red'

    # Apply function to dataframe
    status_df['status'] = status_df['last_datetime'].apply(get_status)

    # Create a Dash HTML table with color boxes
    table_rows = []
    for source, row in status_df.iterrows():
        color = row['status']
        table_rows.append(
            html.Tr([
                html.Td(source, style={"padding": "4px 8px"}),
                html.Td(
                    html.Div(style={
                        "backgroundColor": color,
                        "width": "32px",
                        "height": "16px",
                        "borderRadius": "4px",
                        "display": "inline-block"
                    }),
                    style={
                        "padding": "0",
                        "textAlign": "center",
                        "width": "24px",     # lock the indicator col width
                        "minWidth": "24px",
                        "maxWidth": "24px",
                    }
                )
            ])
        )

    legend_rows = []

    # spacer row
    legend_rows.append(html.Tr([
        html.Td(" ", style={"padding": "6px 8px"}),
        html.Td(" ", style={"padding": "2px"})
    ]))

    # green row
    legend_rows.append(html.Tr([
        html.Td("Timestamp < 1.5 hr ago", style={"padding": "2px 8px"}),
        html.Td(
            html.Div(style={
                "backgroundColor": "green",
                "width": "32px",
                "height": "16px",
                "borderRadius": "4px",
                "display": "inline-block"
            }),
            style={"padding": "0", "textAlign": "center", "width": "24px"}
        )
    ]))

    # yellow row
    legend_rows.append(html.Tr([
        html.Td("Timestamp 1.5 < 24 hr ago", style={"padding": "2px 8px"}),
        html.Td(
            html.Div(style={
                "backgroundColor": "yellow",
                "width": "32px",
                "height": "16px",
                "borderRadius": "4px",
                "display": "inline-block"
            }),
            style={"padding": "0", "textAlign": "center", "width": "24px"}
        )
    ]))

    # red row
    legend_rows.append(html.Tr([
        html.Td("Timestamp > 24 hr ago", style={"padding": "2px 8px"}),
        html.Td(
            html.Div(style={
                "backgroundColor": "red",
                "width": "32px",
                "height": "16px",
                "borderRadius": "4px",
                "display": "inline-block"
            }),
            style={"padding": "0", "textAlign": "center", "width": "24px"}
        )
    ]))

    # now return full table
    return html.Div([
        html.H4("Instrument Status", style={"textAlign": "center"}),
        html.Table(
            [
                html.Tbody(table_rows),  # your instrument rows
                html.Tbody(legend_rows, style={
                    "borderTop": "1px solid #ccc",
                    "backgroundColor": "#f9f9f9"
                })
            ],
            style={
                "width": "100%",
                "marginTop": "10px",
                "borderCollapse": "separate",
                "borderSpacing": "0 6px",
                "tableLayout": "fixed"
            }
        )
    ], id=component_id)
