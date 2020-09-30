import pandas as pd
import plotly
import plotly.express as px

import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import gspread
from oauth2client.service_account import ServiceAccountCredentials
# Connect to main app.py file
from app import app
from app import server

# Connect to your app pages
from apps import campslist, stockregister, survivorinfo

body = html.Div([
    dcc.Location(id='url',refresh=False),
    html.Div(id='page_content')
],id='body')

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div([
        dcc.Link('Camps List |   ', href='/apps/campslist'),
        dcc.Link('Stock Register  |  ', href='/apps/stockregister'),
        dcc.Link('Survivor information', href='/apps/survivorinfo'),
    ], className="row"),
    html.Div(id='page-content', children=[])
])


@app.callback(
    Output('piechart', 'figure'),
    [Input('datatable_id', 'selected_rows'),
     Input('piedropdown', 'value')]
)
def update_data(chosen_rows, piedropval):
    if len(chosen_rows) == 0:
        df_filterd = dff[dff['District'].isin(['Baksa', 'Udalgiri', 'Nalbari', 'Chirang', 'Hojali'])]
    else:
        print(chosen_rows)
        df_filterd = dff[dff.index.isin(chosen_rows)]

    pie_chart = px.pie(
        data_frame=df_filterd,
        names='Camp code',
        values=piedropval,
        hole=.3,
        # labels={'District': 'Countries'}
    )

    return pie_chart


@app.callback(
    dash.dependencies.Output('campcodes-dropdown', 'options'),
    [dash.dependencies.Input('districts-dropdown', 'value')])
def set_cities_options(selected_district):
    return [{'label': i, 'value': i} for i in all_options[selected_district]]

@app.callback(
    dash.dependencies.Output('campcodes-dropdown', 'value'),
    [dash.dependencies.Input('campcodes-dropdown', 'options')])
def set_cities_value(available_options):
    return available_options[0]['value']

@app.callback(
    dash.dependencies.Output('display-selected-values', 'children'),
    [dash.dependencies.Input('districts-dropdown', 'value'),
     dash.dependencies.Input('campcodes-dropdown', 'value')])
def set_display_children(selected_district, selected_campcode):
    return u'{} is a city in {}'.format(
        selected_campcode, selected_district,
    )

@app.callback(
    Output('piechart', 'figure'),
    [Input('datatable_id', 'selected_rows'),
     Input('piedropdown', 'value')]
)
def update_data(chosen_rows, piedropval):
    if len(chosen_rows) == 0:
        df_filterd = dff
    else:
        print(chosen_rows)
        df_filterd = dff[dff.index.isin(chosen_rows)]

    pie_chart = px.pie(
        data_frame=df_filterd,
        names='Gender',
        values=piedropval,
        hole=.3,
        # labels={'District': 'Countries'}
    )

    return pie_chart


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return 'Welcome to the portal! Please choose a link'
    if pathname == '/apps/campslist':
        return campslist.app.layout
    if pathname == '/apps/stockregister':
        return stockregister.app.layout
    if pathname == '/apps/survivorinfo':
        return survivorinfo.app.layout
    else:
        return "404 Page Error! Please choose a link"


if __name__ == '__main__':
    app.run_server(debug=False)