import dash
from dash.dependencies import Input, Output, State, Event
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from plotly.graph_objs import *
import os

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
mapbox_access_token = 'pk.eyJ1IjoiYXl0YWNwYWNhbCIsImEiOiJjam95MnpvcGYyN2syM3FsaGh5azI3YWV6In0.fzNcPtLMMjSIH2qiXTZYVg'


if 'DYNO' in os.environ:
    app.scripts.append_script({
        'external_url': 'https://cdn.rawgit.com/chriddyp/ca0d8f02a1659981a0ea7f013a378bbd/raw/e79f3f789517deec58f41251f7dbb6bee72c44ab/plotly_ga.js'
    })


def initialize():
    df = pd.read_csv('SRFHGMENA_85_1199_TR_YEARMEAN.csv', header=0, na_values='NaN', index_col=4)
    df.index = pd.to_datetime(df.index)
    selected_df = df.loc[(df['bnds'] == 0) & (df['soil_layer'] == 1)]
    return selected_df



colorscale=[[0.0, 'rgb(165,0,38)'], [0.1111111111111111, 'rgb(215,48,39)'],
            [0.2222222222222222, 'rgb(244,109,67)'], [0.3333333333333333, 'rgb(253,174,97)'],
            [0.4444444444444444, 'rgb(254,224,144)'], [0.5555555555555556, 'rgb(224,243,248)'],
            [0.6666666666666666, 'rgb(171,217,233)'], [0.7777777777777778, 'rgb(116,173,209)'],
            [0.8888888888888888, 'rgb(69,117,180)'], [1.0, 'rgb(49,54,149)']]


colorLimits = { 'tas' : [278, 297], 'pr': [0.00000138,0.00029], 'ps': [796, 1017]}


app.layout = html.Div([
    html.Div([
        html.H2("PHYS68L - Atmospheric and Oceanic Fluid Dynamics - Prof.Dr. Murat Turkes - Fall 2018", style={'font-family': 'Dosis'}),
                ], style={'marginBottom': 10, 'marginTop':25}),
    html.Div([
        html.H3("Aytac Pacal", style={'font-family': 'Dosis'}),
                ], style={'marginBottom': 10, 'marginTop':25}),

    dcc.Dropdown(
        id='variable-dropdown',
        options=[
            {'label': 'Near-Surface Air Temperature	', 'value': 'tas'},
            {'label': 'Total Precipitation Flux', 'value': 'pr'},
            {'label': 'Surface Pressure', 'value': 'ps'}
        ],
        value='tas'
    ),

    html.Div([html.P(" ", style={'font-family': 'Dosis'}),
              ], style={'marginBottom': 20, 'marginTop':20}),

    dcc.Slider(
        id='year-slider',
        min=2011,
        max=2099,
        value=2011,
        step=1,
        marks= {
            2011: {'label': '2011'},
            2020: {'label': '2020'},
            2030: {'label': '2030'},
            2040: {'label': '2040'},
            2050: {'label': '2050'},
            2060: {'label': '2060'},
            2070: {'label': '2070'},
            2080: {'label': '2080'},
            2090: {'label': '2090'},
            2099: {'label': '2099'},
        }),

    html.Div([html.P(" ", style={'font-family': 'Dosis'}),
              ], style={'marginBottom': 20, 'marginTop':20}),

    dcc.Graph(id='map'),
    html.Div(id='output')
    ])


@app.callback(Output('map', 'figure'),
              [Input('year-slider', 'value'),
               Input('variable-dropdown', 'value')])
def update_graph(year, variable):

    year_df = selected_df[str(year)]
    long = year_df['xlon'][:]
    lat = year_df['xlat'][:]
    variable_df = year_df[str(variable)][:]
    data = []

    data.append(
        Scattermapbox(
            lon=long.values,
            lat=lat.values,
            mode='markers',
            hoverinfo= 'lat+lon+text',
            text=year_df[str(variable)].values,
            marker=dict(
                showscale=True,
                cmax=colorLimits[str(variable)][1],
                cmin=colorLimits[str(variable)][0],
                color=year_df[str(variable)].values,
                colorscale='RdBu'
            ),

        )
    )


    layout = Layout(
        margin=dict(t=5, b=5, r=5, l=5),
        autosize=True,
        height=750,
        hovermode='closest',
        showlegend=False,
        mapbox=dict(
            accesstoken=mapbox_access_token,
            center=dict(
                lat=39,  # 40.7272
                lon=35  # -73.991251
            ),
            pitch=0,
            zoom=5,
            style='light'
        ),

    )
    
        
    return Figure(data=data, layout=layout)


@app.server.before_first_request
def defineSelectedPandas():
    global selected_df
    selected_df = initialize()

if __name__ == '__main__':
    app.run_server(debug=True)




