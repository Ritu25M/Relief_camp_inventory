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
from pprint import pprint

app = dash.Dash(__name__)

scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)

sheet = client.open("Relief_Camp_List").sheet1
df = pd.DataFrame(sheet.get_all_records())

dff = df  # .groupby('District', as_index=False)[['Total people', 'Available vacancies']].sum()
# print(dff[:5])

# ---------------------------------------------------------------
app.layout = html.Div([
    html.H1('Relief Camps Information ', style={"textAlign": "center"}),
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
                {'if': {'column_id': 'District'},
                 'width': '10%', 'textAlign': 'left'},
                {'if': {'column_id': 'Camp code'},
                 'width': '10%', 'textAlign': 'left'},
                {'if': {'column_id': 'Map'},
                 'width': '20%', 'textAlign': 'left'},
                {'if': {'column_id': 'Address'},
                 'width': '15%', 'textAlign': 'left'},
                {'if': {'column_id': 'Contact Numbers'},
                 'width': '15%', 'textAlign': 'left'},
                {'if': {'column_id': 'Total people'},
                 'width': '15%', 'textAlign': 'left'},
                {'if': {'column_id': 'Available Vacancies'},
                 'width': '15%', 'textAlign': 'left'},
            ],
        ),
    ], className='row'),

    html.Div([
        html.Div([
            dcc.Dropdown(id='piedropdown',
                         options=[
                             {'label': 'Total people', 'value': 'Total people'},
                             {'label': 'Available vacancies', 'value': 'Available vacancies'}
                         ],
                         placeholder="Select a column for pie chart",
                         value='Available vacancies',
                         multi=False,
                         clearable=False
                         ),
        ], className='six columns'),

    ], className='row'),

    html.Div([
        html.Div([
            dcc.Graph(id='piechart'),
        ], className='six columns'),

    ], className='row'),

])


# ------------------------------------------------------------------
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


# ------------------------------------------------------------------

if __name__ == '__main__':
    app.run_server(debug=True)
