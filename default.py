import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

import numpy as np

def make_def_sc(prj, template, app):

    """ Set up grid of plots. """

    def_scatter = make_subplots(
                rows=3, cols=1, 
                #column_widths=500,
                row_width=[0.05, .2, .95],
                vertical_spacing = 0.01,
                #horizontal_spacing = 0.05,
                specs=[[{}],[{"secondary_y": True}],[{}]],
                subplot_titles=(["",""]))

    """ Scatter plot. """

    #def_scatter.add_trace(go.Scatter(x = prj[0], 
    #                    y = prj[1],
    #                    mode = 'markers',
    #                    name = '',
    #                    hoverinfo = 'skip',
    #                    #text = ['Player : '+  for ix in prj.index],
    #                    marker = dict(size=4, color='#aaaaaa', 
    #                        line = dict(width=0))), 
    #                        #colorscale='Viridis', colorbar=dict(thickness=20, orientation='h'))),
    #                    row=1, col=1)

    kde = go.Histogram2dContour(
            x = prj[0],
            y = prj[1],
            opacity=.5,
            reversescale=True,
            colorscale='gray',
            hoverinfo='skip', 
            showscale = False,
            line = dict(width=0),
        )
        
    def_scatter.add_trace(kde)

    """ Update axes properties. """

    def_scatter.update_xaxes(title_text="", autorange=False, range=[-.05, 1.05], 
        showgrid=False, zeroline=False, visible=False, fixedrange=True, row=1, col=1)
    def_scatter.update_yaxes(title_text="", autorange=False, range=[-.05, 1.05], 
        showgrid=False, zeroline=False, visible=False, fixedrange=True, row=1, col=1)

    """ Age violin plot. """

    def_scatter.add_trace(go.Violin(x= prj[0], line_color='#aaaaaa', 
                            box_visible=True, meanline_visible=True,
                            orientation='h', side='positive', width=1, points=False,
                            name='', legendgroup = '', showlegend=False), 
                            row=2, col=1)
 
    def_scatter.update_xaxes(title_text="", autorange=False, range=[-0.01, 1.01], 
        showgrid=False, zeroline=False, visible=False, fixedrange=True, row=2, col=1)
    def_scatter.update_yaxes(title_text="Players Density", autorange=False, range=[0,.55],
        showgrid=False, zeroline=False, visible=False, fixedrange=True, row=2, col=1)

    """ Add custom color bar. """

    def_scatter.add_trace(go.Scatter(x = np.linspace(0,1,1000), 
                        y = [0]*1000,
                        mode = 'markers',
                        name = '',
                        hoverinfo='skip',
                        marker_symbol='square',
                        marker = dict(size=25, color='#aaaaaa', 
                            line = dict(width=0))), 
                            #colorscale='Viridis', colorbar=dict(thickness=20, orientation='h'))),
                        row=3, col=1)

    """ Update axes properties. """

    def_scatter.update_xaxes(title_text="", autorange=False, range=[-0.01, 1.01], 
        showgrid=False, zeroline=False, visible=False, fixedrange=True, row=3, col=1)
    def_scatter.update_yaxes(title_text="", autorange=False, range=[-0.5, 0], 
        showgrid=False, zeroline=False, visible=False, fixedrange=True, row=3, col=1)

    """ Plots configuration. """

    def_scatter.update_layout(font_family="Helvetica",
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
                        uniformtext_minsize=12, uniformtext_mode='hide',
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)'
                        )

    return def_scatter, kde

def make_def_ra(svd, template, app, categories):

    """ Set up grid of plots. """

    def_radar = make_subplots(
                rows=1, cols=1, 
                #column_widths=500,
                #row_width=[.2, .95],
                #vertical_spacing = 0.01,
                #horizontal_spacing = 0.05,
                specs=[[{'type':'polar'}]],
                #subplot_titles=(["",""]))
                )

    """ Scatter plot. """

    def_radar.add_trace(go.Scatterpolar(r=[-1]*len(categories),
                        theta=categories,
                        fill='toself',
                        line   = dict(width=0),
                        marker = dict(size=0, opacity=0)),
                        row=1, col=1)

    """ Update axes properties. """

    def_radar.update_polars(radialaxis=dict(title_text="", autorange=False, range=[0, 1], 
        showgrid=False, showline=False), 
        row=1, col=1)

    """ Plots configuration. """

    def_radar.update_layout(font_family="Helvetica",
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

    return def_radar


def make_def_pr(svd, template, app, seasons):

    """ Set up grid of plots. """

    def_progress = make_subplots(
                rows=1, cols=1, 
                #column_widths=500,
                #row_width=[.2, .8],
                #vertical_spacing = 0.01,
                #horizontal_spacing = 0.05,
                specs=[[{}]],
                #subplot_titles=(["",""])
                )

    """ Improvement plot. """

    def_progress.add_trace(go.Scatter(x=seasons[:-1]+['improvement'],
                        y=[-1]*(len(seasons)),
                        line   = dict(width=1),
                        marker = dict(size=0, opacity=0)),
                        row=1, col=1)

    """ Update axes properties. """

    def_progress.update_xaxes(title_text="", autorange=False, range=[-0.1, len(seasons[:-1])+0.1], 
        showgrid=False, zeroline=True, visible=True, fixedrange=True, row=1, col=1)
    def_progress.update_yaxes(autorange=False, range=[-0.1, 1+0.1], 
        showgrid=False, zeroline=True, visible=True, fixedrange=True, row=1, col=1,
        title_text="Score",
        title_font=dict(family="Helvetica",
                        size=15), )

    """ Plots configuration. """

    def_progress.update_layout(font_family="Helvetica",
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

    return def_progress