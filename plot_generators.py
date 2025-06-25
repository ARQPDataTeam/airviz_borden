import pandas as pd
from ast import literal_eval
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sqlalchemy import text
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

def time_series_generator(start_date,end_date,sql_query,sql_engine,logger):

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
    logger.debug(sql_query)
    
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

def profile_generator(sql_query,sql_engine,logger):

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

    # print (output_df)
    output_df.columns=['species',1,5,16,26,33,42]
    output_df.set_index('species', drop=True, inplace=True)
    # print (output_df)
    # Transpose: heights become rows, species become columns
    output_df = output_df.T
    output_df.index = output_df.index.astype(float)  # height as float

    # Separate species into primary and secondary
    o3_species = [ 'O3' ]
    co2_species = ['CO2_LIC', 'CO2d_LGR', 'CO2d_PIC']
    ch4_species = ['CH4d_PIC', 'COd_LGR']
    h2o_species = ['H2O_LGR', 'H2O_LIC', 'H2O_PIC']
    ocs_species = ['OCS_LGR']

    # sub-select the dataframe into smaller sets organized by concentration scale
    o3_df=output_df[o3_species]
    co2_df=output_df[co2_species]
    ch4_df=output_df[ch4_species]
    h2o_df=output_df[h2o_species]
    h2o_df = output_df[h2o_species].copy()
    h2o_df['H2O_PIC'] *= 10  # scale
    ocs_df = output_df[ocs_species]

    # set a colour list
    plot_color_list=['black','blue','red','green','orange','yellow','brown','violet','turquoise','pink','olive','magenta','lightblue','purple']

    # create the fig properties
    fig = make_subplots(rows=1, cols=5, column_widths=[0.18, 0.18, 0.18, 0.18, 0.18], shared_yaxes=True)

    # === PANEL 1 CH4 and CO ===
    fig.add_trace(go.Scatter(
        x=o3_df['O3'],
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
        x=ocs_df['OCS_LGR'],
        y=ocs_df.index,
        mode='lines+markers',
        line=dict(color=plot_color_list[3]),
        name='OCS_LGR (pptv)',
        # xaxis='x4',
        legendgroup='panel5',
        showlegend=True
    ), row=1, col=5)

    # === Layout for all x-axes ===
    fig.update_layout(
        height=600,
        title=('Average Borden Tower Concentration Profiles From '+start_time+' to '+end_time),
        title_x=0.5,  # Center the title horizontally

    # X-Axes
        xaxis=dict(title='O3 (ppbv)', side='bottom'),         # col=1
        xaxis2=dict(title='CO2 (ppmv)', side='bottom'),   # col=2
        xaxis3=dict(title='CH4 / CO (ppmv)', side='bottom'),   # col=3
        xaxis4=dict(title='H2O (ppthv)', side='bottom'),  # col=4
        xaxis5=dict(title='OCS (ppthv)', side='bottom'),  # col=5

        # Position legend to the right of all 3 panels
            legend=dict(
                x=1.05,
                y=1,
                tracegroupgap=20
            ),
            )

    # return the fig
    return fig