from app import app
import numpy as np
import pandas as pd

import matplotlib as mpl 
import matplotlib.pyplot as pypl

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

from dash.dependencies import Input, Output
from app import plt, svd, template, categorical, categories, seasons, seasons_abbr, pal26, rc


""" First Dropdown, per class clinical data. """
    
@app.callback(Output(component_id = 'fig_progress',  component_property = 'figure'),
              [Input(component_id = 'dpdw_play', component_property = 'value'),
               Input(component_id = 'dpdw_cat',    component_property = 'value')])

def graph3_update(dpdw_play, dpdw_cat):

    """ Set up grid of plots. """

    fig3 = make_subplots(
                rows=1, cols=1, 
                #column_widths=500,
                #row_width=[.2, .8],
                #vertical_spacing = 0.01,
                #horizontal_spacing = 0.05,
                specs=[[{}]],
                #subplot_titles=(["",""]))
                )

    """ Scatter plot. """

    if dpdw_play == []:

        fig3.add_trace(go.Scatter(x = np.arange(len(seasons)), 
                    y = [-1]*len(seasons),
                    line   = dict(width=0),
                    marker = dict(size=0, opacity=0)),
                    row=1, col=1)

    else:

        for j,p in enumerate(dpdw_play):

            """ Improvement plot. """

            ix  = plt[plt['player']==p]
            vls = rc[dpdw_cat].loc[ix.index]
            vls.index = ix['season']
            new_vls = pd.Series(np.nan,index=seasons_abbr)
            new_vls[ix['season']]= vls 
            vls = new_vls.values

            fig3.add_trace(go.Scatter(x=seasons[:-1]+['improvement'], 
                                y=[vls[-1]]*(len(seasons)-1)+[np.nan],
                                text = ['Player: '+ plt['player'].loc[ix.index[0]] +\
                                        '<br>Season: '+str(plt['season'].loc[ix.index[0]])+\
                                        '<br>League: '+plt['league'].loc[ix.index[0]]+\
                                        '<br>Team: '+plt['squad'].loc[ix.index[0]]+\
                                        '<br>Position: '+plt['position'].loc[ix.index[0]]+\
                                        '<br>Nationality: '+plt['nationality'].loc[ix.index[0]]+\
                                        '<br> Average '+ dpdw_cat +': {:.3f}'.format(vls[-1]) for _ in vls[:-1]],
                                line   = dict(width=1, color=pal26[j]),
                                marker = dict(size=0, opacity=0)),
                                row=1, col=1)

            fig3.add_trace(go.Scatter(x=seasons[:-1]+['improvement'], 
                                y=list(vls[:-1])+[np.nan],
                                text = ['Player: '+ plt['player'].loc[ix.index[0]] +\
                                        '<br>Season: '+str(plt['season'].loc[ix.index[0]])+\
                                        '<br>League: '+plt['league'].loc[ix.index[0]]+\
                                        '<br>Team: '+plt['squad'].loc[ix.index[0]]+\
                                        '<br>Position: '+plt['position'].loc[ix.index[0]]+\
                                        '<br>Nationality: '+plt['nationality'].loc[ix.index[0]]+\
                                        '<br>'+ dpdw_cat +': {:.3f}'.format(v) for v in vls[:-1]],
                                line   = dict(width=0),
                                marker = dict(size=10, opacity=1, symbol='circle',
                                            color = 'white', line = dict(color=pal26[j], width = 1))),
                                row=1, col=1)
            if len(vls)<3:
                sym = 'square'
                diff = 0
            else:
                diff = vls[-2]-vls[-3]
                cutoff = np.abs(vls[-2])*.05
                if diff > cutoff:
                    sym = 'triangle-up'
                elif diff < -cutoff:
                    sym = 'triangle-down'
                else:
                    sym = 'square'

            fig3.add_trace(go.Scatter(x=seasons[:-1]+['improvement'], 
                                y=[np.nan]*len(seasons[:-1])+[vls[-1]],
                                text = ['Player: '+ plt['player'].loc[ix.index[0]] +\
                                        '<br>Season: '+str(plt['season'].loc[ix.index[0]])+\
                                        '<br>League: '+plt['league'].loc[ix.index[0]]+\
                                        '<br>Team: '+plt['squad'].loc[ix.index[0]]+\
                                        '<br>Position: '+plt['position'].loc[ix.index[0]]+\
                                        '<br>Nationality: '+plt['nationality'].loc[ix.index[0]]+\
                                        '<br> improvement: {:.3f}'.format(diff) for v in vls[:-1]],
                                line   = dict(width=0),
                                marker = dict(size=10, opacity=1, symbol=sym,
                                            color = pal26[j], line = dict(width = 0))),
                                row=1, col=1)


    """ Update axes properties. """

    fig3.update_xaxes(title_text="", autorange=False, range=[-0.1, len(seasons[:-1])+0.1], 
        showgrid=False, zeroline=True, visible=True, fixedrange=True, row=1, col=1,
        )
    fig3.update_yaxes(autorange=False, range=[-0.1, 1.1], 
        showgrid=False, zeroline=True, visible=True, fixedrange=True, row=1, col=1,
        title_text="Score", 
        title_font=dict(family="Helvetica",
                        size=15))

    """ Plots configuration. """

    fig3.update_layout(font_family="Helvetica",
                        autosize=True,
                        width=500*4/5,
                        height=250*4/5,
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

    return fig3