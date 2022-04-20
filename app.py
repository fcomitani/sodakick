
#what about improvements? how the player improved in the years
#update dropdowns dynamically
#https://community.plotly.com/t/updating-a-dropdown-menus-contents-dynamically/4920/2

import numpy as np
import pandas as pd
import pickle

import dash
from dash import html
from dash import dcc

import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
from matplotlib.colors import LinearSegmentedColormap
from default import make_def_sc, make_def_ra, make_def_pr

template='flatly'
load_figure_template(template)

""" Load data. """

prj = pd.read_hdf('./data/prj_minkowski_separate_teams_220218.h5')
plt = pd.read_hdf('./data/all_players_separate_teams_220218.h5')

svd = pd.read_hdf('./data/svd_separate_teams_220218.h5')
svd = (svd-svd.min())/(svd.max()-svd.min())

rc = pd.read_hdf('./data/rc_features_220413.h5')

plt = plt[sorted(plt.columns)]
plt.season = plt.season.astype(str)

leagues      = ['Bundesliga','La Liga','Ligue 1','Premier League','Serie A']
leagues_abbr = ['BL','LL','LU','PL','SA']

categorical={}
for cl in plt.columns:
    categorical[cl] = True if cl in ['league','squad','position','nationality','season'] else False

feat_labs      = [{'label': i.lower(), 'value': i} for i in plt.columns if not categorical[i]] 
league_labs    = [{'label': i, 'value': a} for i,a in zip(leagues,leagues_abbr)]
squad_labs     = [{'label': i, 'value': i} for i in sorted(plt['squad'].unique())]
pos_labs       = [{'label': i, 'value': i} for i in sorted(plt['position'].apply(lambda x: x.split(',')[0]).unique())]
nat_labs       = [{'label': i, 'value': i} for i in sorted(plt['nationality'].unique())]
season_labs    = [{'label': 'Average', 'value': 'average'}] +\
                    [{'label': '20'+i[:2]+'-20'+i[2:], 'value': i} for i in sorted(plt['season'].astype(str).unique()[:-1])][::-1]
play_labs      = [{'label': i, 'value': i} for i in sorted(plt['player'].unique())]

categories     = ['blocks','aggressivity','experience','goal keeping','action precision','goals','shots','action support','passes']
rc_labs        = [{'label': l, 'value': l} for i,l in enumerate(rc.columns)]

seasons             = ['2017/2018','2018/2019','2019/2020','2020/2021','2021/2022','average']
seasons_abbr        = sorted(plt['season'].unique())

pal26=['#%02x%02x%02x' % x for x in [(240,163,255),(0,117,220),(153,63,0),
                                     (255,255,128),(25,25,25),(0,92,49),(43,206,72),
                                     (255,204,153),(128,128,128),(148,255,181),
                                     (143,124,0),(157,204,0),(194,0,136),(0,51,128),(255,164,5),
                                     (255,168,187),(66,102,0),(255,0,16),(94,241,242),
                                     (0,153,143),(224,255,102),(116,10,255),(153,0,0),(76,0,92),(255,255,0),(255,80,5)]]

midpal=['#F8B195','#F67280','#C06C84','#6C5B7B','#355C7D'][::-1]
midpalmap=LinearSegmentedColormap.from_list('my_list', midpal, N=1000)

""" Set up the dashboard. """

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

config = {'responsive': True}

""" Set up default plots. """

def_scatter, kde = make_def_sc(prj, template, app)
def_radar = make_def_ra(prj, template, app, categories)
def_progress = make_def_pr(prj, template, app, seasons)

""" Define app layout. """

app.layout = html.Div(id = 'parent', children = [

    html.H3(id = 'H_clinical', children = 'SodaKick dashboard', style = {'textAlign':'center',
                                                                'marginTop':40,'marginBottom':40, 
                                                                'font-family':'Helvetica'}, 
                                                   className='text-center text-primary, mb-3'), 

    html.Div(className='row', style = {'textAlign':'left', 'width': '60%', 'marginLeft':'20%','marginRight':'20%'},
        children = [


        html.Div(children=[
            html.Label(['Season'], style={'font-family':'Helvetica', 'font-weight': 'bold', "text-align": "center"}),
            dcc.Dropdown( id = 'dpdw_season',
                options = season_labs,
                value = 'average',
                style={'font-family':'Helvetica'},
                clearable=False),
            ], style=dict(width='100%')),

        html.Div(className='two columns', style = {'textAlign':'left', 'width': '50%'},
            children = [

        html.Div(children=[
            html.Label(['Feature'], style={'font-family':'Helvetica', 'font-weight': 'bold', "text-align": "center"}),
            dcc.Dropdown( id = 'dpdw_feat',
                    options = feat_labs,
                    value = 'goals',
                    style={'font-family':'Helvetica'},
                    clearable=False),
            ], style=dict(width='33,333%')),


        html.Div(className='row', 
            children = [

        html.Div(className='two columns', style = {'textAlign':'left', 'width': '50%'},
            children = [

        html.Div(children=[
            html.Label(['League'], style={'font-family':'Helvetica', 'font-weight': 'bold', "text-align": "center"}),
            dcc.Dropdown( id = 'dpdw_league',
                options = league_labs,
                value = [],
                multi= True,
                style={'font-family':'Helvetica'},
                clearable=False),
            ], style=dict(width='100%')),
        
        ]),

        html.Div(className='two columns', style = {'textAlign':'left', 'width': '50%'},
            children = [

        html.Div(children=[
            html.Label(['Team'], style={'font-family':'Helvetica', 'font-weight': 'bold', "text-align": "center"}),
            dcc.Dropdown( id = 'dpdw_squad',
                options = squad_labs,
                value = [],
                multi= True,
                style={'font-family':'Helvetica'},
                searchable=True,
                clearable=False),
            ], style=dict(width='100%')),
        
        ]),

        ]),

        html.Div(className='row', 
            children = [

        html.Div(className='two columns', style = {'textAlign':'left', 'width': '50%'},
            children = [

        html.Div(children=[
            html.Label(['Role'], style={'font-family':'Helvetica', 'font-weight': 'bold', "text-align": "center"}),
            dcc.Dropdown( id = 'dpdw_pos',
                options = pos_labs,
                value = [],
                multi= True,
                style={'font-family':'Helvetica'},
                clearable=False),
            ], style=dict(width='100%')),
            
        ]),

        html.Div(className='two columns', style = {'textAlign':'left', 'width': '50%'},
            children = [

        html.Div(children=[
            html.Label(['Nationality'], style={'font-family':'Helvetica', 'font-weight': 'bold', "text-align": "center"}),
            dcc.Dropdown( id = 'dpdw_nat',
                options = nat_labs,
                value = [],
                multi= True,
                style={'font-family':'Helvetica'},
                searchable=True,
                clearable=False),
            ], style=dict(width='100%')),
        ]),

        ]),

        dcc.Graph(id = 'fig_scatter', figure=def_scatter, style=dict(width='100%')),
    ]),


    html.Div(className='two columns', style = {'textAlign':'left', 'width': '50%'},
        children = [

        html.Div(children=[
            html.Label(['Player'], style={'font-family':'Helvetica', 'font-weight': 'bold', "text-align": "center"}),
            dcc.Dropdown( id = 'dpdw_play',
                    options = play_labs,
                    value = None,
                    style={'font-family':'Helvetica'},
                    multi=True,
                    searchable=True,
                    clearable=False),
            ], style=dict(width='100%')),
    
        dcc.Graph(id = 'fig_radar', figure=def_radar, style=dict(width='100%')),

        html.Div(children=[
            html.Label(['Category'], style={'font-family':'Helvetica', 'font-weight': 'bold', "text-align": "center"}),
            dcc.Dropdown( id = 'dpdw_cat',
                    options = rc_labs,
                    value = 'goals',
                    style={'font-family':'Helvetica'},
                    multi=False,
                    searchable=True,
                    clearable=False),
            ], style=dict(width='100%')),
    
        dcc.Graph(id = 'fig_progress', figure=def_progress, style=dict(width='100%')),

    ]), ]),

    ])


""" Callbacks dropdown """

@app.callback(
    dash.dependencies.Output('dpdw_squad', 'options'),
    [dash.dependencies.Input('dpdw_league', 'value')])

def set_team_from_league(dpdw_league):

    indices = []

    for league in dpdw_league:
        indices += list(plt[plt['league']==league]['squad'].unique())

    if len(indices)>0:
        squad_labs = [{'label': i, 'value': i, 'disabled': False} 
                        if i in indices else {'label': i, 'value': i, 'disabled': True}
                        for i in sorted(plt['squad'].unique())]
    else:
        squad_labs = [{'label': i, 'value': i, 'disabled': False}
                        for i in sorted(plt['squad'].unique())]
                        
    return squad_labs 

@app.callback(
    dash.dependencies.Output('dpdw_play', 'options'),
    [dash.dependencies.Input('dpdw_season', 'value')])

def set_player_from_season(dpdw_season):
    
    indices = plt[plt['season']==dpdw_season]['player'].unique()

    return    [{'label': i, 'value': i, 'disabled': False} 
                        if i in indices else {'label': i, 'value': i, 'disabled': True}
                        for i in sorted(plt['player'].unique())]

@app.callback(
    dash.dependencies.Output('dpdw_nat', 'options'),
    [dash.dependencies.Input('dpdw_season', 'value'),
    dash.dependencies.Input('dpdw_league', 'value'),
    dash.dependencies.Input('dpdw_squad', 'value'),
    dash.dependencies.Input('dpdw_pos', 'value')])

def set_nationality_from_many(dpdw_season, dpdw_league, dpdw_squad, dpdw_pos):

    indices = plt[plt['season']==dpdw_season]['nationality'].unique()

    indices_new = []
    for league in dpdw_league:
        indices_new += list(plt[plt['league']==league]['nationality'].unique())
    if len(indices_new)>0:
        indices = [ix for ix in indices_new
            if ix in indices]

    indices_new = []
    for team in dpdw_squad:
        indices_new += list(plt[plt['squad']==team]['nationality'].unique())
    if len(indices_new)>0:
        indices = [ix for ix in indices_new
            if ix in indices]

    indices_new = []
    for role in dpdw_pos:
        indices_new += list(plt[plt['pos']==role]['nationality'].unique())
    if len(indices_new)>0:
        indices = [ix for ix in indices_new
            if ix in indices]

    return    [{'label': i, 'value': i, 'disabled': False} 
                        if i in indices else {'label': i, 'value': i, 'disabled': True}
                        for i in sorted(plt['nationality'].unique())]

@app.callback([dash.dependencies.Output(component_id = 'dpdw_play',  component_property = 'value'),
               dash.dependencies.Output(component_id = 'fig_scatter', component_property = 'clickData')],
               [dash.dependencies.Input(component_id = 'fig_scatter', component_property = 'clickData'),
               dash.dependencies.Input(component_id = 'dpdw_play', component_property = 'value')])

def set_player_from_click(clickData,dpdw_play):

    if dpdw_play is None:
        dpdw_play = []

    return list(set(dpdw_play+[clickData['points'][0]['text'].split('<br>')[0][8:]])), None

#maybe do prediction
#clustering, maybe classify player by type -> similar players
#do logo
#do resize plots with window

""" Callbacks """

from callback_sc import *
from callback_ra import *
from callback_pr import *

if __name__ == '__main__': 
    app.run_server(debug=False)
