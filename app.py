import dash
from dash.dependencies import Input, Output, State, Event
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from plotly.graph_objs import *
import plotly.figure_factory as ff
import os

print os.getcwd()

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


colorLimits = { 'tas' : [5.5205, 28.7251],
                'pr': [0.00000138,0.00029],
                'ps': [796, 1017],
                'hfss': [1.30,76.6],
                'sund': [3495,4752],
                }

titleDict = {'tas':'Near-Surface Air Temperature',
             'pr':'Total Precipitation Flux',
             'ps': 'Surface Pressure',
             'hfss' : 'Sensible heat flux',
             'sund': 'Duration of sunshine'}

app.layout = html.Div([
    html.Div([
        html.H2("PHYS68L - Atmospheric and Oceanic Fluid Dynamics Fall 2018 ", style={'font-family': 'Dosis'}),
                ], style={'marginBottom': 10, 'marginTop':25}),
    html.Div([
        html.P("Instructor: Prof.Dr. Murat Turkes | Student: Aytac Pacal ", style={'font-family': 'Dosis'}),
                ], style={'marginBottom': 15, 'marginTop':10}),

    dcc.Dropdown(
        id='variable-dropdown',
        options=[
            {'label': 'Near-Surface Air Temperature	', 'value': 'tas'},
            {'label': 'Total Precipitation Flux', 'value': 'pr'},
            {'label': 'Surface Pressure', 'value': 'ps'},
            {'label': 'Sensible heat flux', 'value': 'hfss'},
            {'label': 'Duration of sunshine', 'value': 'sund'},
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

    html.Div(
        [
            html.Div(
                [
                    dcc.Graph(id='map')
                ],
                className='eight columns',
                style={'margin-top': '20'}
            ),
            html.Div(
                [dcc.Graph(id='graph'),
                 ],
                className='four columns',
                style={'margin-top': '20'}
            ),
        ],
        className='row'
    ),
    html.Div(id='output')
    ])

#  Update map
@app.callback(Output('map', 'figure'),
              [Input('year-slider', 'value'),
               Input('variable-dropdown', 'value')])
def update_graph(year, variable):

    year_df = selected_df[str(year)]
    long = year_df['xlon'][:]
    lat = year_df['xlat'][:]
    if str(variable) ==  'tas' :
        variable_df = [x-273.15 for x in year_df[str(variable)][:]]
    else:
        variable_df = year_df[str(variable)][:]
    data = []

    data.extend([
        Scattermapbox(
            lon=long.values,
            lat=lat.values,
            mode='markers',
            hoverinfo= 'lat+lon+text',
            text=variable_df,
            marker=dict(
                showscale=True,
                cmax=colorLimits[str(variable)][1],
                cmin=colorLimits[str(variable)][0],
                color=variable_df,
                colorscale='RdBu',
                size=25,
                opacity = 0.8
            ),
        ),
        Scattermapbox(
            lat=["41.0082"],
            lon=["28.9784"],
            mode='markers',
            hoverinfo="text",
            text=["Istanbul"],
            # opacity=0.5,
        )
        ])

    layout = Layout(
        title = str(year),
        margin=dict(t=30, b=5, r=20, l=20),
        autosize=True,
        height=600,
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
        updatemenus=[
            dict(
                buttons=([
                    dict(
                        args=[{
                            'mapbox.zoom': 5,
                            'mapbox.center.lon': '35.42',
                            'mapbox.center.lat': '38.79',
                            'mapbox.bearing': 0,
                        }],
                        label='Reset Zoom',
                        method='relayout'
                    )
                ]),
                direction='left',
                pad={'r': 0, 't': 0, 'b': 0, 'l': 0},
                showactive=False,
                type='buttons',
                x=0.45,
                xanchor='left',
                yanchor='bottom',
                bgcolor='#323130',
                borderwidth=1,
                bordercolor="#6d6d6d",
                font=dict(
                    color="#FFFFFF"
                ),
                y=0.02
            ),
            dict(
                buttons=([
                    dict(
                        args=[{
                            'mapbox.zoom': 6,
                            'mapbox.center.lon': '28.9784',
                            'mapbox.center.lat': '41.0082',
                            'mapbox.bearing': 0,
                        }],
                        label='Istanbul',
                        method='relayout'
                    ),
                ]),
                direction="down",
                pad={'r': 0, 't': 0, 'b': 0, 'l': 0},
                showactive=False,
                bgcolor="rgb(50, 49, 48, 0)",
                type='buttons',
                yanchor='bottom',
                xanchor='left',
                font=dict(
                    color="#FFFFFF"
                ),
                x=0,
                y=0.05
            )
        ]

    )

    return Figure(data=data, layout=layout)


# Update graph
@app.callback(
    Output('graph', 'figure'),
    [Input('map', 'clickData'),
     Input('year-slider', 'value'),
     Input('variable-dropdown', 'value')])
def update_figure(clickData,year,variable):

    year_df = selected_df[str(year)]
    initial_hist_df = selected_df['2011']

    initial_hist = Histogram(
        x = [temp-273.15 for temp in initial_hist_df[str(variable)].values],
        opacity=0.75,
        name='2011'
    )
    updated_hist = Histogram(
        x = [temp-273.15 for temp in year_df[str(variable)].values],
        opacity=0.5,
        name=str(year)
    )

    data = [initial_hist, updated_hist]
    layout = Layout(
        title='Histogram',
        barmode='overlay',
        xaxis = dict(
            title=titleDict[str(variable)]
        ),
        yaxis = dict(
            title = 'Number of grid points'
        )
    )

    return Figure(data=data, layout=layout)


@app.server.before_first_request
def defineSelectedPandas():
    global selected_df
    selected_df = initialize()

if __name__ == '__main__':
    app.run_server(debug=True)




