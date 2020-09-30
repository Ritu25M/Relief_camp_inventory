import dash
import dash_table
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)

sheet = client.open("survivors_info").worksheet('BKR01-INV')
df = pd.DataFrame(sheet.get_all_records())
dff = df
app = dash.Dash(__name__)

all_options = {
    'Baksa': ['BKR01', 'BKR02'],
    'Udalgiri': [u'ULR01', 'ULR02']
}
app.layout = html.Div([
    html.H1('Stock Register', style={"textAlign": "center"}),
    dcc.Dropdown(
        id='districts-dropdown',
        options=[{'label': k, 'value': k} for k in all_options.keys()],
        value='Baksa'
    ),

    html.Hr(),

    dcc.Dropdown(id='campcodes-dropdown'),

    html.Hr(),

    html.Div([
        dash_table.DataTable(
            id='datatable_id',
            data=dff.to_dict('records'),
            columns=[
                {"name": i, "id": i, "deletable": False, "selectable": False} for i in dff.columns
            ],
            editable=False,
            filter_action="native",
            sort_action="native",
            sort_mode="multi",
            row_selectable="multi",
            row_deletable=False,
            selected_rows=[],
            # page_action="native",
            # page_current=0,
            # page_size=6,
            page_action='none',
            style_cell={
                'whiteSpace': 'normal'
            },
            fixed_rows={'headers': True, 'data': 0},
            virtualization=False,
            style_cell_conditional=[
                {'if': {'column_id': 'Items'},
                 'width': '20%', 'textAlign': 'left'},
                {'if': {'column_id': 'Estimated Items Requirement'},
                 'width': '20%', 'textAlign': 'left'},
                {'if': {'column_id': 'Distributed Items'},
                 'width': '20%', 'textAlign': 'left'},
                {'if': {'column_id': 'Current stock level'},
                 'width': '20%', 'textAlign': 'left'},
                {'if': {'column_id': 'Next supply date'},
                 'width': '20%', 'textAlign': 'left'},
            ],
        ),
    ], className='row'),
])

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
    dash.dependencies.Output('datatable_id', 'children'),
    [dash.dependencies.Input('districts-dropdown', 'value'),
     dash.dependencies.Input('campcodes-dropdown', 'value')])
def set_display_children(selected_district, selected_campcode):
    return u'{} is a city in {}'.format(
        selected_campcode, selected_district,
    )


if __name__ == '__main__':
    app.run_server(debug=True)