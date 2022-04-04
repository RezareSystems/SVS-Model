# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.4.2
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

import dash
from dash import dash_table
from dash import html
from dash import dcc
import plotly.graph_objects as go
import plotly.express as px
import datetime as dt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from bisect import bisect_left, bisect_right
from jupyter_dash import JupyterDash
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import cufflinks as cf
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import copy
import CropNBalFunctions as cnbf

# ## General components

CropCoefficients, EndUseCatagoriesDropdown, metFiles, MetDropDown, MonthIndexs = cnbf.Generalcomponents()

# ## Core crop model components

# +
Scallers = cnbf.Scallers 
StagePropns = cnbf.StagePropns

# Graphs scallers over thermal time series
Graph = plt.figure()
plt.plot(Scallers.loc[:,'scaller'])
plt.plot(Scallers.loc[:,'cover'])
plt.plot(Scallers.loc[:,'rootDepth'])
T_mat = 100
for p in StagePropns.index:
    plt.plot(StagePropns.loc[p,'PrpnTt']*T_mat,StagePropns.loc[p,'PrpnMaxDM'],'o',color='k')
    plt.text(StagePropns.loc[p,'PrpnTt']*T_mat+3,StagePropns.loc[p,'PrpnMaxDM'],p,verticalalignment='top')
    plt.plot([StagePropns.loc[p,'PrpnTt']*T_mat]*2,[0,Scallers.loc[round(StagePropns.loc[p,'PrpnTt'] * T_mat),'max']],'--',color='k',lw=1)
plt.ylabel('Relative DM accumulation')
plt.xlabel('Temperature accumulation')

# -

# ## Declair Global properties

# +
PreviousConfig = cnbf.setCropConfig(["Lincoln","","","","",0,1,0,0,0,
                                dt.datetime.strptime('03-09-2021','%d-%m-%Y'),"Seed",
                                dt.datetime.strptime('06-03-2022','%d-%m-%Y'),"EarlyReproductive",[]])
PreviousConfig.to_pickle("Previous_Config.pkl")

CurrentConfig = cnbf.setCropConfig(["Lincoln","","","","",0,1,0,0,0,
                                dt.datetime.strptime('05-05-2022','%d-%m-%Y'),"Seed",
                                dt.datetime.strptime('08-02-2023','%d-%m-%Y'),"EarlyReproductive",[]])
CurrentConfig.to_pickle("Current_Config.pkl")

FollowingConfig = cnbf.setCropConfig(["Lincoln","","","","",0,1,0,0,0,
                                dt.datetime.strptime('02-04-2022','%d-%m-%Y'),"Seed",
                                dt.datetime.strptime('04-10-2022','%d-%m-%Y'),"EarlyReproductive",[]])
FollowingConfig.to_pickle("Following_Config.pkl")
# Tt = pd.DataFrame()
# -

# ## Graph constructors

# +
def CropNGraph(cropN,NComponentColors):
    NData = cropN.reset_index()
    fig = px.line(data_frame=NData,x='Date',y='Values',color='Component',color_discrete_sequence=NComponentColors,
                 )#range_x = [c['EstablishDate']-dt.timedelta(days=7),c['HarvestDate']+dt.timedelta(days=7)])
    fig.update_layout(title_text="Crop N", title_font_size = 30, title_x = 0.5, title_xanchor = 'center')
    fig.update_yaxes(title_text="Nitrogen (kg/ha)", title_font_size = 20)
    fig.update_xaxes(title_text=None)
    return fig

def CropWaterGraph(cropWater):
    NData = cropWater.reset_index()
    fig = px.line(data_frame=NData,x='Date',y='Values',color='Component',color_discrete_sequence=['brown','orange','red','green'],
                 )#range_x = [c['EstablishDate']-dt.timedelta(days=7),c['HarvestDate']+dt.timedelta(days=7)])
    fig.update_layout(title_text="Cover and Root Depth", title_font_size = 30, title_x = 0.5, title_xanchor = 'center')
    fig.update_yaxes(title_text="Cover (m2/m2) and depth (m)", title_font_size = 20)
    fig.update_xaxes(title_text=None)
    return fig


# -

# ## App layout and callbacks

# +
app = JupyterDash(external_stylesheets=[dbc.themes.SLATE])

@app.callback(Output("Location",'value'),Input("Location",'value'))
def StateCrop(Location):
    for pos in ['Previous_','Current_','Following_']:
        cnbf.updateConfig(["Location"],[Location],pos+"Config.pkl")
    return Location

def splitprops(prop_ID,propExt):
    prop_ID = prop_ID.replace(propExt,'')
    return prop_ID.split('_')[0]+'_', prop_ID.split('_')[1]

for pos in ['Previous_','Current_','Following_']:
    @app.callback(Output(pos+"Group","children"),Output(pos+"Crop","children"),Output(pos+"Type","children"),Output(pos+"SaleableYield",'children'),
              Output(pos+"Units",'children'),Output(pos+"Product Type","children"), Output(pos+"FieldLoss","children"),Output(pos+"DressingLoss","children"),
              Output(pos+"MoistureContent","children"),Output(pos+"EstablishDate","children"), Output(pos+"EstablishStage",'children'),
              Output(pos+"HarvestDate", "children"),Output(pos+"HarvestStage",'children'),
              Input(pos+"End use DD","value"),Input(pos+"Group DD","value"),Input(pos+"Crop DD","value"), Input(pos+"Type DD","value"))
    def ChangeCrop(EndUseValue, GroupValue, CropValue, TypeValue):
        pos = list(dash.callback_context.inputs.keys())[0].split('_')[0]+'_'
        return cnbf.UpdateCropOptions(EndUseValue, GroupValue, CropValue, TypeValue, CropCoefficients, pos)
    
    @app.callback(Output(pos+"Defoliation Dates","children"), Input(pos+"EstablishDate DP",'date'), Input(pos+"HarvestDate DP",'date'), prevent_initial_call=True)
    def DefoliationOptions(Edate, Hdate):
        pos = list(dash.callback_context.inputs.keys())[0].split('_')[0]+'_'
        defDates = dcc.Checklist(id=pos+"Def Dates",options=[])
        if (Edate != None) and (Hdate!= None):
            cropMonths = pd.date_range(dt.datetime.strptime(str(Edate).split('T')[0],'%Y-%m-%d'),
                                       dt.datetime.strptime(str(Hdate).split('T')[0],'%Y-%m-%d'),freq='MS')
            DefCheckMonths = [{'label':MonthIndexs.loc[i.month,'Name'],'value':i} for i in cropMonths]    
            defDates = dcc.Checklist(id=pos+"Def Dates", options = DefCheckMonths, value=[])
        return defDates
    
    for act in ["EstablishDate", "HarvestDate"]:
        @app.callback(Output(pos+act+' DP','date'),Input(pos+act+' DP','date'), prevent_initial_call=True)
        def StateCrop(actdate):
            prop_ID = list(dash.callback_context.inputs.keys())[0]
            pos,act = splitprops(prop_ID,'.date')
            cnbf.updateConfig([act[:-3]],[dt.datetime.strptime(str(actdate).split('T')[0],'%Y-%m-%d')],pos+"Config.pkl")
            return actdate
    
    for outp in cnbf.UIConfigMap.index:
        @app.callback(Output(pos+outp,'value'),Input(pos+outp,'value'))
        def setInputValue(value):
            prop_ID = list(dash.callback_context.inputs.keys())[0]
            pos,outp = splitprops(prop_ID,'.value')
            cnbf.updateConfig([cnbf.UIConfigMap.loc[outp,"ConfigID"]],[value],pos+"Config.pkl")
            return value
#https://stackoverflow.com/questions/60383266/python-reuse-functions-in-dash-callbacks

@app.callback(
    Output('CropUptakeGraph','figure'),
    Output('MineralNGraph','figure'),
    Output('NInputsGraph','figure'),
    Input('RefreshButton','n_clicks'), prevent_initial_call=True)
def RefreshGraphs(n_clicks):
    Config = pd.read_pickle(pos+"Config.pkl")
    Tt = cnbf.CalculateMedianTt(Config["EstablishDate"],Config["HarvestDate"],metFiles[Config["Location"]])
    CropN, CropWater, NComponentColors = cnbf.CalculateCropOutputs(Tt,Config,CropCoefficients)
    return CropNGraph(CropN, NComponentColors), CropWaterGraph(CropWater)

app.layout = html.Div([
                dbc.Row([
                    dbc.Col([dbc.Row(dbc.Card(cnbf.CropInputs('Previous_',EndUseCatagoriesDropdown))),
                             dbc.Row(dbc.Card(cnbf.CropInputs('Current_',EndUseCatagoriesDropdown))),
                             dbc.Row(dbc.Card(cnbf.CropInputs('Following_',EndUseCatagoriesDropdown)))
                            ]),
                    dbc.Col([dbc.Row(html.H1("Field Location")),
                             dbc.Row(dcc.Dropdown(id="Location",options = MetDropDown,value='Lincoln')),
                             dbc.Row(html.Button("Refresh",id="RefreshButton"))
                            ],width = 2),
                    dbc.Col([dbc.Row(dbc.Card(dcc.Graph(id='CropUptakeGraph'))),
                             dbc.Row(dbc.Card(dcc.Graph(id='MineralNGraph'))),
                             dbc.Row(dbc.Card(dcc.Graph(id='NInputsGraph')))
                            ])
                        ])
                     ])
# Run app and display result inline in the notebook
app.run_server(mode='external')
# -

pd.read_pickle("Previous_Config.pkl")

pd.read_pickle("Current_Config.pkl")

pd.read_pickle("Following_Config.pkl")
