# -*- coding: utf-8 -*-
"""
Created on Thu May  6 12:09:48 2021

@author: jesakke
"""

# Global Path & other utilities
from utils import *

# preprocessing file
from webscrap import LinkedInScrapper
from text_preprocess import *

import dash_core_components as dcc
import dash_html_components as html
import dash
from dash.dependencies import Input, Output

import plotly.graph_objects as go
import plotly.express as px

from plotly.offline import plot


app = dash.Dash(__name__)


app.layout = html.Div([
        html.Div([
            html.H1(children= "Dash Web application - LinkedIn common words used",
            style={"text-align": "center", 'font-weight': 'bold', "font-size":"100%", "color":"black"})
        ]),
        
        html.Div([html.Label(['Enter the URL:'],style={'font-weight': 'bold'})]),
            
            
        html.Div([
           
            dcc.Input(
                id='input1',
                type = 'text',
                value = '', #'https://www.linkedin.com/company/google/',
                style={"width": "50%"}
            ),
        ]),
        
        html.Div([html.Label(['Enter the year:'],style={'font-weight': 'bold'})]),
        
        html.Div([
          dcc.Input(
              id='input2',
              value = 'all', #'2011',
              type = 'text',
              style={"width": "50%"}
          ),
        ]),

        html.Div([html.Label(['Enter number Top N words to display:'],style={'font-weight': 'bold'})]),

        html.Div([
              dcc.Input(
                  id='input3',
                  type = 'number',
                  value = 'initial value',
                  style={"width": "50%"}
              ),
          ]),


    html.Div([
        dcc.Graph(id='the_graph')
    ]),

])



@app.callback(
    Output(component_id='the_graph', component_property='figure'),
    [Input(component_id='input1', component_property='value'),
     Input(component_id='input2', component_property='value'),
     Input(component_id='input3', component_property='value')]
)




def update_output(input1, input2, input3):
    print(input1, input2, input3)
    
    if input1.split('/')[3] == 'company':
        name = input1[33:-1]
    else:
        name  = input1[28:-1]
    
    if input3 > 10:
        call_class                              = LinkedInScrapper(url = input1, period = input2, top_n = input3)
        df_subset, df_words_used, first_n_rows  = call_class.analyze_words()
    
        data = go.Bar(
                x            = first_n_rows.words,
                y            = first_n_rows.counts,
                text         = first_n_rows.counts, 
                textposition = "outside", 
                textfont     = dict(size=12), 
                )
            
    return {'data': [data],'layout' : go.Layout(yaxis_title = 'No of times words used (Counts)',
                                                xaxis_title = f'{name} Words commonly used',
                                                    height=900,                                                 
                                                    )}

      

if __name__ == "__main__":
    app.run_server(debug=True)
                                                    

