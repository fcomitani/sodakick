from app import app
import numpy as np

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

from dash.dependencies import Input, Output
from app import plt, svd, template, categorical, categories, pal26, rc

""" First Dropdown, per class clinical data. """
    
@app.callback(Output(component_id = 'fig_radar',  component_property = 'figure'),
              [Input(component_id = 'dpdw_play', component_property = 'value'),
               Input(component_id = 'dpdw_season',    component_property = 'value')])

def graph2_update(dpdw_play, dpdw_season):

    values = plt[plt['season']==dpdw_season]
        
    """ Set up grid of plots. """

    fig2 = make_subplots(
                rows=1, cols=1, 
                #column_widths=500,
                #row_width=[.2, .95],
                #vertical_spacing = 0.01,
                #horizontal_spacing = 0.05,
                specs=[[{'type':'polar'}]],
                #subplot_titles=(["",""]))
                )

    """ Scatter plot. """

    if dpdw_play == []:

        fig2.add_trace(go.Scatterpolar(r=[-1]*len(categories),
                        theta=categories,
                        fill='toself',
                        line   = dict(width=0),
                        marker = dict(size=0, opacity=0)),
                        row=1, col=1)

    else:

        for j,p in enumerate(dpdw_play):

        
            ix  = values[values['player']==p].index
            vls = rc.loc[ix[0]]

            fig2.add_trace(go.Scatterpolar(r=[vls[c] for i,c in enumerate(categories)],
                                theta=categories,
                                fill='toself',
                                hoverinfo='text',
                                text = ['Player: '+ values['player'].loc[ix[0]] +\
                                        '<br>Season: '+str(values['season'].loc[ix[0]])+\
                                        '<br>League: '+values['league'].loc[ix[0]]+\
                                        '<br>Team: '+values['squad'].loc[ix[0]]+\
                                        '<br>Position: '+values['position'].loc[ix[0]]+\
                                        '<br>Nationality: '+values['nationality'].loc[ix[0]]+\
                                        '<br>'+ c +': {:.3f}'.format(vls[c])  
                                        for i,c in enumerate(categories)],
                                line   = dict(width=0, color=pal26[j]),
                                marker = dict(size=0, opacity=0)),
                                row=1, col=1)

    """ Update axes properties. """

    fig2.update_polars(radialaxis=dict(title_text="", autorange=False, range=[0, 1], 
        showgrid=False, showline=False), 
        row=1, col=1)
        
    """ Plots configuration. """

    fig2.update_layout(font_family="Helvetica",
                        autosize=True,
                        width=500*4/5,
                        height=425*4/5,
                        margin = dict(t=50, 
                                    b=50, 
                                    l=50, 
                                    r=50),
                        showlegend=False,
                        polar=dict(
                            radialaxis=dict(
                                visible=True
                            ),
                        ),
                        uniformtext_minsize=12, uniformtext_mode='hide',
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)'
                        )

    #add legend

    return fig2