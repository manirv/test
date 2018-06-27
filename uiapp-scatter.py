# -*- coding: utf-8 -*-
"""
Created on Tue Jun 19 13:35:41 2018

@author: Mani
"""
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
from scipy import stats


# Here is the Dash App Layout and interaction behaviour defined.
app = dash.Dash()
#stylesheets = {'stylesheet.css': 'https://codepen.io/chriddyp/pen/bWLwgP.css'}

#df = pd.read_csv(
#    'https://gist.githubusercontent.com/chriddyp/' +
#    '5d1ea79569ed194d432e56108a04d188/raw/' +
#    'a9f9e8076b837d541398e999dcbac2b2826a81f8/'+
#    'gdp-life-exp-2007.csv')

df2 = pd.read_csv('https://raw.githubusercontent.com/colaberry/DSin100days/master/data/Advertising.csv')

# Generated linear fit
slope, intercept, r_value, p_value, std_err = stats.linregress(df2['TV'],df2['Sales'])
line = slope*df2['TV'] + intercept

app.layout = html.Div(children=[
    html.Link(
        rel='stylesheet',
        href='/static/bWLwgP.css'
    ),
    html.H1(children='Predicting Sales using Regression'),

    html.Div(children=[html.Label('TV Advertising Spend in $million '),
    dcc.Input(id='tv-id', value='10.5', type='text')]),

    html.Div(children=[html.Label('Radio Advertising Spend in $million '),
    dcc.Input(id='radio-id', value='12.5', type='text')]),



    html.Div(id='predicted-div'),
        dcc.Graph(
        id='advert-graph',
        figure={
            'data': [
                go.Scatter(
                    x=df2['TV'],
                    y=df2['Sales'],
                    #text='' + df2['TV'],
                    mode='markers',
                    opacity=0.7,
                    marker={
                        'size': 15,
                        'line': {'width': 0.5, 'color': 'white'}
                    }
                )

            ],
            'layout': go.Layout(
                xaxis={'type': 'log', 'title': 'TV Ad Spend'},
                yaxis={'title': 'Sales Turnover'},
                margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                legend={'x': 0, 'y': 1},
                hovermode='closest'
            )
        }    
    )

])

            
@app.callback(
    Output(component_id='predicted-div', component_property='children'),
    [Input(component_id='tv-id', component_property='value'), 
     Input(component_id='radio-id', component_property='value')]
)
def update_output_div(tv_value,radio_value):
    prediction = [200.8]
    tempdf = pd.DataFrame({'TV':[tv_value],'Radio':[radio_value]})
    df2.append(tempdf, ignore_index=True)
    
    #df2['TV']
    #predict(tv_value, radio_value)
    return 'You\'ve entered TV Spend as "{}" and Radio spend as "{}". And the predicted sales is "{}"'.format(tv_value, radio_value, prediction[0]) 


@app.callback(
    dash.dependencies.Output('advert-graph', 'figure'),
        [Input(component_id='tv-id', component_property='value'), 
     Input(component_id='radio-id', component_property='value')])
def update_figure(tv_value,radio_value):
    prediction = [20.8]
    tempdf = pd.DataFrame({'TV':[tv_value],'Radio':[radio_value]})
    tempdf['Sales'] = prediction
    traces = []
    traces.append(go.Scatter(
                    x=df2['TV'],
                    y=df2['Sales'],
                    text=df2['Radio'],
                    mode='markers',
                    opacity=0.7,
                    marker={
                        'size': 15,
                        'line': {'width': 0.5, 'color': 'white'}
                    }, name='Trained'
                ))
    
    traces.append(go.Scatter(
                    x=tempdf['TV'],
                    y=tempdf['Sales'],
                    text=tempdf['Radio'],
                    mode='markers',
                    opacity=0.7,
                    marker={
                        'size': 15,
                        'line': {'width': 0.5, 'color': 'white'}
                    }, name='Predicted'
                ))

    return {
        'data': traces,
        'layout': go.Layout(
                xaxis={'type': 'log', 'title': 'TV Ad Spend'},
                yaxis={'title': 'Sales Turnover'},
                margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                legend={'x': 0, 'y': 1},
                hovermode='closest'
            )
    }


if __name__ == '__main__':
    app.run_server(debug=True)