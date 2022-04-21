from app import app
import numpy as np

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

from dash.dependencies import Input, Output
from app import plt, prj, template, categorical, kde, midpalmap, midpal

""" First Dropdown, per class clinical data. """
    
@app.callback(Output(component_id = 'fig_scatter',  component_property = 'figure'),
              [Input(component_id = 'dpdw_feat', component_property = 'value'),
               Input(component_id = 'dpdw_season',    component_property = 'value'),
               Input(component_id = 'dpdw_league',    component_property = 'value'),
               Input(component_id = 'dpdw_squad',    component_property = 'value'),
               Input(component_id = 'dpdw_pos',    component_property = 'value'),
               Input(component_id = 'dpdw_nat',    component_property = 'value'),
               Input(component_id = 'fig_scatter', component_property = 'clickData')
])

def graph1_update(dpdw_feat, dpdw_season, dpdw_league, dpdw_squad, dpdw_pos, dpdw_nat, clickData):

    values = plt

    axmin = min(values[dpdw_feat]) if dpdw_feat is not None else 0
    axmax = max(values[dpdw_feat]) if dpdw_feat is not None else 1

    norm = mpl.colors.Normalize(vmin=axmin, vmax=axmax)
    cmap = midpalmap

    values = values[values['season']==dpdw_season]

    if len(dpdw_league) > 0:
        values = values[values['league'].isin(dpdw_league)]
    if len(dpdw_squad)  > 0:
        values = values[values['squad'].isin(dpdw_squad)]
    if len(dpdw_pos)    > 0:
        values = values[values['position'].apply(lambda x: len(set(x.split(',')).intersection(dpdw_pos)))>0]
    if len(dpdw_nat)    > 0:
        values = values[values['nationality'].isin(dpdw_nat)]

    #values.set_index('player',drop=True,inplace=True)
    #values.drop_duplicates(inplace=True)
    #indices = set(prj.index).intersection(values.index)
    
    """ Set up grid of plots. """

    fig1 = make_subplots(
                rows=3, cols=1, 
                #column_widths=500,
                row_width=[0.05, .2, .95],
                vertical_spacing = 0.01,
                #horizontal_spacing = 0.05,
                specs=[[{}],[{"secondary_y": True}],[{}]],
                subplot_titles=(["",""]))

    """ Scatter plot. """

    """fig1.add_trace(go.Scatter(x = prj[0], 
                    y = prj[1],
                    mode = 'markers',
                    name = '',
                    hoverinfo='text',
                    text = ['Player : '+ plt['player'].loc[ix] for ix in prj.index],
                    marker = dict(size=4, color='#aaaaaa', 
                        line = dict(width=0))), 
                        #colorscale='Viridis', colorbar=dict(thickness=20, orientation='h'))),
                    row=1, col=1)"""
    
    fig1.add_trace(kde,
                    row=1, col=1)

    fig1.add_trace(go.Scatter(x = prj[0].loc[values.index], 
                        y = prj[1].loc[values.index],
                        mode = 'markers',
                        name = '',
                        hoverinfo='text',
                        text = ['Player: '+values['player'].loc[ix]+\
                                '<br>Season: '+str(values['season'].loc[ix])+\
                                '<br>League: '+values['league'].loc[ix]+\
                                '<br>Team: '+values['squad'].loc[ix]+\
                                '<br>Position: '+values['position'].loc[ix]+\
                                '<br>Nationality: '+values['nationality'].loc[ix]+\
                                '<br>'+dpdw_feat+': {:.3f}'.format(values[dpdw_feat].loc[ix])
                                for ix in values.index],
                        marker = dict(size=4, line=dict(width=0),
                                    color=values[dpdw_feat], cmin=axmin, cmax=axmax, colorscale=midpal)),
                                    # colorbar=dict(thickness=20, orientation='h'))),
                        row=1, col=1)

    """ Update axes properties. """

    fig1.update_xaxes(title_text="", autorange=False, range=[-.05, 1.05], 
        showgrid=False, zeroline=False, visible=False, fixedrange=True, row=1, col=1)
    fig1.update_yaxes(title_text="", autorange=False, range=[-.05, 1.05], 
        showgrid=False, zeroline=False, visible=False, fixedrange=True, row=1, col=1)


    """ Violin plot. """

    vls = values[dpdw_feat]
    vcolor = 'rgb' + str(cmap(norm(vls.median()))[0:3]) 

    fig1.add_trace(go.Violin(x=vls, line_color=vcolor, 
                            box_visible=True, meanline_visible=True,
                            orientation='h', side='positive', width=1, points=False,
                            name='', legendgroup = '', showlegend=False), 
                            row=2, col=1)

    fig1.add_trace(go.Scatter(x =vls, 
                y = [0]*len(vls),
                mode = 'markers',
                name = '',
                hoverinfo='text',
                text = ['Player: '+ values['player'].loc[ix] +\
                        '<br>'+ dpdw_feat +': {:.3f}'.format(values[dpdw_feat].loc[ix])
                        for ix in vls.index],
                marker_symbol='circle',
                marker = dict(size=10, 
                    color=['rgb' + str(cmap(norm(v))[0:3]) for v in vls], 
                    line = dict(width=0))),
                secondary_y=True,
                row=2, col=1) 

    """ Update axes properties. """

    fig1.update_xaxes(title_text="", autorange=False, range=[axmin, axmax], 
        showgrid=False, zeroline=False, visible=False, fixedrange=True, row=2, col=1)
    fig1.update_yaxes(title_text="Players Density", autorange=False, range=[0,.55],
        title_font=dict(family="Helvetica",
                        size=15), 
        showticklabels=False, secondary_y=False,
        showgrid=False, zeroline=False, visible=True, fixedrange=True, row=2, col=1)
    fig1.update_yaxes(title_text="y", autorange=False, range=[0,.55],
        showticklabels=False, secondary_y=True,
        rangemode='tozero', constraintoward='bottom',
        showgrid=False, zeroline=False, visible=False, fixedrange=True, row=2, col=1)
        

    """ Add custom color bar. """

    fig1.add_trace(go.Scatter(x = np.linspace(axmin,axmax,1000), 
                        y = [0]*1000,
                        mode = 'markers',
                        name = '',
                        hoverinfo='skip',
                        marker_symbol='square',
                        marker = dict(size=25, color=np.linspace(axmin,axmax,1000), 
                            line = dict(width=0), 
                            colorscale=midpal)),
                        row=3, col=1)

    """ Update axes properties. """

    axxrange = np.linspace(axmin, axmax, 6)

    if dpdw_feat == 'birth_year':
        ticktext = ['{:d}'.format(int(x)) for x in axxrange]
    else:
        ticktext = ['{:.2f}'.format(x) for x in axxrange]

    ###### FIX THIS #######
    fig1.update_xaxes(title_text=dpdw_feat, autorange=False, range=[axmin-.01, axmax+.01], 
        showgrid=True, zeroline=False, visible=True, fixedrange=True, 
        ticktext=ticktext, row=3, col=1)
    fig1.update_yaxes(title_text="", autorange=False, range=[-0.5, 0], 
    showgrid=False, zeroline=False, visible=False, fixedrange=True, row=3, col=1)
    
        
    """ Plots configuration. """

    fig1.update_layout(font_family="Helvetica",
                        autosize=True,
                        width=500*4/5,
                        height=500/.95*1.2*4/5,
                        margin = dict(t=50, 
                                    b=50, 
                                    l=50, 
                                    r=50),
                        showlegend=False,
                        legend_tracegroupgap = 145,
                        template=template, 
                        barmode='stack',
                        uniformtext_minsize=12, uniformtext_mode='hide',
                        clickmode='event+select',
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)'
                        )

    return fig1