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

sheet = client.open("survivors_info").worksheet('BKR01')
df = pd.DataFrame(sheet.get_all_records())

dff = df  # .groupby('District', as_index=False)[['Total people', 'Available vacancies']].sum()
# print(dff[:5])

# ---------------------------------------------------------------
app.layout = html.Div([
    html.H1('Survivors Information ', style={"textAlign": "center"}),
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
                {'if': {'column_id': 'Date of entry'},
                 'width': '20%', 'textAlign': 'left'},
                {'if': {'column_id': 'Aadhar number'},
                 'width': '20%', 'textAlign': 'left'},
                {'if': {'column_id': 'Gender'},
                 'width': '20%', 'textAlign': 'left'},
                {'if': {'column_id': 'Name'},
                 'width': '20%', 'textAlign': 'left'},
                {'if': {'column_id': 'Age category'},
                 'width': '20%', 'textAlign': 'left'},
            ],
        ),
    ], className='row'),

    html.Div([
        html.Label(['Survivor information']),
        dcc.Dropdown(
            id='my_dropdown',
            options=[
                {'label': 'Gender', 'value': 'Gender'},
                {'label': 'Age category', 'value': 'Age category'},
                {'label': 'Medical requirements', 'value': 'Medical requirements'}
            ],
            value='Gender',
            multi=False,
            clearable=False,
            style={"width": "50%"}
        ),
    ]),

    html.Div([
        dcc.Graph(id='the_graph')
    ]),

    html.Div([
        dcc.Graph(id='the_linegraph')
    ]),
])


# ---------------------------------------------------------------
@app.callback(
    Output(component_id='the_graph', component_property='figure'),
    [Input(component_id='my_dropdown', component_property='value')]
)
def update_graph(my_dropdown):
    dff = df

    piechart = px.pie(
        data_frame=dff,
        names=my_dropdown,
        hole=.3,
    )

    return (piechart)


@app.callback(
    Output(component_id='the_linegraph', component_property='figure'),
    [Input(component_id='my_dropdown', component_property='value')]
)
def update_graph(my_dropdown):
    firstcol = np.array(sheet.col_values(1))
    unique_elements, counts_elements = np.unique(firstcol, return_counts=True)
    linechart = px.line( x=unique_elements, y=counts_elements)

    return linechart


if __name__ == '__main__':
    app.run_server(debug=True)
