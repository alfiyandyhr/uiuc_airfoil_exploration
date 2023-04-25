# -----------------------------------
# Dash app to explore UIUC airfoils
# by alfiyandyhr
# -----------------------------------
from dash import Dash, dcc, html
import dash
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# Importing database
df = pd.read_csv('summary/summary_all.csv')
available_indicators = ['CL', 'CD', 'CDp', 'CM', 'Top_Xtr', 'Bot_Xtr', 'L_by_D']

with open('names_list/airfoil_names.txt', 'r') as f:
    names_list = f.readlines()
with open('names_list/problematic_airfoil.txt', 'r') as f:
    problematic_list = f.readlines()
with open('names_list/not_converged.txt', 'r') as f:
    empty_list = f.readlines()

for i in range(len(names_list)):
    names_list[i] = names_list[i][:-1]

for i in range(len(problematic_list)):
    problematic_list[i] = problematic_list[i][:-1]
    
for i in range(len(empty_list)):
    empty_list[i] = empty_list[i][:-1]

# List of airfoils with successful analysis
done_list = list(set(names_list) - set(problematic_list) - set(empty_list))

# Importing airfoil coordinates
coord_list = {}
for idx, name in enumerate(done_list):
    coord_list[name] = np.genfromtxt(f'processed_coordinates/{name}')

# Instantiating Dash
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets)

# Create server variable with Flask server object for use with gunicorn
server = app.server

# Main Layout
app.layout = html.Div([
    html.H4(children='UIUC Airfoil Database Exploration',
            style={'text-align': 'center'}),
    
    html.H5(children='Re: 3.5E6, Mach = 0.117',
            style={'text-align': 'center'}),
    
    html.H6(children='''by @alfiyandyhr at teTra-aviation corp.''',
             style={'text-align': 'center'}),
    
    html.Div(children='''Set the x-axis on the left column, and y-axis on the right column.
                         Move the slider for a specific angle of attack (from -2 to 10).
                      ''',
             style={'text-align': 'center'}),

    html.Div(children='''Hover around and click the point to select the candidate! Happy exploring 1300+ airfoils!''',
             style={'text-align': 'center'}),

    html.Div([

        html.Div([
            dcc.Dropdown(
                id='crossfilter-xaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='CL'
            ),
            dcc.RadioItems(
                id='crossfilter-xaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ],
        style={'width': '49%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='crossfilter-yaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='L_by_D'
            ),
            dcc.RadioItems(
                id='crossfilter-yaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ], style={'width': '49%', 'float': 'right', 'display': 'inline-block'})
    ], style={
        'borderBottom': 'thin lightgrey solid',
        'backgroundColor': 'rgb(250, 250, 250)',
        'padding': '10px 5px'
    }),

    html.Div(children='''Angle of Attack Slider''',
             style={'text-align': 'center','padding-top':'20px'}),    
    
    html.Div(dcc.Slider(
        id='crossfilter-alpha--slider',
        min=df['Alpha'].min(),
        max=df['Alpha'].max(),
        value=0.0,
        marks={str(alpha): str(alpha) for alpha in df['Alpha'].unique()},
        step=None
    ), style={'width': '80%', 'margin': 'auto'}),    
    
    html.Div([
        dcc.Graph(
            id='crossfilter-indicator-scatter',
            clickData={'points': [{'customdata': 'e1233.dat'}]}
        )
    ], style={'width': '60%', 'display': 'block', 'margin': 'auto'}),

    html.Div([
            html.Div([
                dcc.Graph(id='x-time-series'),
                dcc.Graph(id='y-time-series'),
            ], style={'display': 'inline-block', 'width': '48%'}),

            html.Div([
                html.H6(children='''You can also pinpoint the airfoil candidate from the list below.''',
                        style={'text-align': 'center', 'margin-top': '20px'}),
                dcc.Dropdown(
                    id='crossfilter-airfoil-candidates',
                    options=[{'label': i, 'value': i} for i in done_list],
                    value='e1233.dat'
                ),
                dcc.Graph(id='airfoil-plot',
                          style={'margin-top': '120px'}),
            ], style={'display': 'inline-block', 'width': '48%', 'float':'right'})
    ], style={'width': '98%'}),
    
])

@app.callback(
    dash.dependencies.Output('crossfilter-indicator-scatter', 'figure'),
    [dash.dependencies.Input('crossfilter-airfoil-candidates', 'value'),
     dash.dependencies.Input('crossfilter-xaxis-column', 'value'),
     dash.dependencies.Input('crossfilter-yaxis-column', 'value'),
     dash.dependencies.Input('crossfilter-xaxis-type', 'value'),
     dash.dependencies.Input('crossfilter-yaxis-type', 'value'),
     dash.dependencies.Input('crossfilter-alpha--slider', 'value')])

def update_graph(airfoil_candidate_name,
                 xaxis_column_name, yaxis_column_name,
                 xaxis_type, yaxis_type,
                 alpha_value):
    
    dff = df[df['Alpha'] == alpha_value]

    fig = go.Figure()
    
    fig.add_trace(
        go.Scatter(
            x=dff[dff['Indicator Name'] == xaxis_column_name]['Value'],
            y=dff[dff['Indicator Name'] == yaxis_column_name]['Value'],
            text=dff[dff['Indicator Name'] == yaxis_column_name]['Airfoil Name'],
            customdata=dff[dff['Indicator Name'] == yaxis_column_name]['Airfoil Name'],
            mode='markers',
            marker={
                'size': 25,
                'opacity': 0.7,
                'color': 'orange',
                'line': {'width': 2, 'color': 'purple'}
            },
            name='All Airfoils'
        )
    )
    
    fig.add_trace(
        go.Scatter(
            x=dff[dff['Indicator Name'] == xaxis_column_name][dff['Airfoil Name'] == airfoil_candidate_name]['Value'],
            y=dff[dff['Indicator Name'] == yaxis_column_name][dff['Airfoil Name'] == airfoil_candidate_name]['Value'],
            text=airfoil_candidate_name,
            customdata=[airfoil_candidate_name],
            mode='markers',
            marker={
                'size': 25,
                'opacity': 1.0,
                'color': 'black',
                'symbol': 'x'
            },
            name='Selected Candidate'
        )
    )
    
    fig.update_layout(
        xaxis={
            'title': xaxis_column_name,
            'type': 'linear' if xaxis_type == 'Linear' else 'log'
        },
        yaxis={
            'title': yaxis_column_name,
            'type': 'linear' if yaxis_type == 'Linear' else 'log'
        },
        margin={'l': 40, 'b': 30, 't': 10, 'r': 0},
        height=450,
        hovermode='closest'
    )
    
    return fig

def create_time_series(dff, axis_type, title):
    return {
        'data': [dict(
            x=dff['Alpha'],
            y=dff['Value'],
            mode='markers'
        )],
        'layout': {
            'height': 225,
            'margin': {'l': 20, 'b': 30, 'r': 10, 't': 10},
            'annotations': [{
                'x': 0, 'y': 0.85, 'xanchor': 'left', 'yanchor': 'bottom',
                'xref': 'paper', 'yref': 'paper', 'showarrow': False,
                'align': 'left', 'bgcolor': 'rgba(255, 255, 255, 0.5)',
                'text': title
            }],
            'yaxis': {'type': 'linear' if axis_type == 'Linear' else 'log'},
            'xaxis': {'showgrid': False},
        }
    }

@app.callback(
    dash.dependencies.Output('x-time-series', 'figure'),
    [dash.dependencies.Input('crossfilter-indicator-scatter', 'clickData'),
     dash.dependencies.Input('crossfilter-xaxis-column', 'value'),
     dash.dependencies.Input('crossfilter-xaxis-type', 'value')])
def update_x_timeseries(clickData, xaxis_column_name, axis_type):
    airfoil_name = clickData['points'][0]['customdata']
    dff = df[df['Airfoil Name'] == airfoil_name]
    dff = dff[dff['Indicator Name'] == xaxis_column_name]
    title = '<b>{}</b><br>{}'.format(airfoil_name, xaxis_column_name)
    return create_time_series(dff, axis_type, title)

@app.callback(
    dash.dependencies.Output('y-time-series', 'figure'),
    [dash.dependencies.Input('crossfilter-indicator-scatter', 'clickData'),
     dash.dependencies.Input('crossfilter-yaxis-column', 'value'),
     dash.dependencies.Input('crossfilter-yaxis-type', 'value')])
def update_y_timeseries(clickData, yaxis_column_name, axis_type):
    dff = df[df['Airfoil Name'] == clickData['points'][0]['customdata']]
    dff = dff[dff['Indicator Name'] == yaxis_column_name]
    return create_time_series(dff, axis_type, yaxis_column_name)

def airfoil_plot(coord_np, title):
    return {
        'data': [dict(
            x=pd.Series(coord_np[:,0]),
            y=pd.Series(coord_np[:,1]),
            mode='lines'
        )],
        'layout': {
            'height': 225,
            'margin': {'l': 20, 'b': 30, 'r': 10, 't': 10},
            'annotations': [{
                'x': 0, 'y': 0.85, 'xanchor': 'left', 'yanchor': 'bottom',
                'xref': 'paper', 'yref': 'paper', 'showarrow': False,
                'align': 'left', 'bgcolor': 'rgba(255, 255, 255, 0.5)',
                'text': title
            }],
            'yaxis': {'type': 'linear'},
            'xaxis': {'showgrid': False},
        }
    }

@app.callback(
    dash.dependencies.Output('airfoil-plot', 'figure'),
    [dash.dependencies.Input('crossfilter-indicator-scatter', 'clickData')])
def update_airfoil_plot(clickData):
    airfoil_name = clickData['points'][0]['customdata']
    coord_np = coord_list[airfoil_name]
    return airfoil_plot(coord_np, airfoil_name)

if __name__ == '__main__':
	app.run_server(debug=True)