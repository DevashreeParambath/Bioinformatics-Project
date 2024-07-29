from dash import Dash, dash_table, dcc, html, Input, Output, State
import pandas as pd
import dash_bio as dashbio

# Read data for DataTable
df = pd.read_csv('https://raw.githubusercontent.com/ThomasCarroll/Bioinformatics-Project/main/DashDataTable.csv', index_col=0)

# Initialize Dash app
app = Dash(__name__)

# Hosted genome options for IGV dropdown
HOSTED_GENOME_DICT = [
    {'value': 'mm10', 'label': 'Mouse (GRCm38/mm10)'},
    {'value': 'rn6', 'label': 'Rat (RGCS 6.0/rn6)'},
    {'value': 'gorGor4', 'label': 'Gorilla (gorGor4.1/gorGor4)'},
    {'value': 'panTro4', 'label': 'Chimp (SAC 2.1.4/panTro4)'},
    {'value': 'panPan2', 'label': 'Bonobo (MPI-EVA panpan1.1/panPan2)'},
    {'value': 'canFam3', 'label': 'Dog (Broad CanFam3.1/canFam3)'},
    {'value': 'ce11', 'label': 'C. elegans (ce11)'}
]

# Define app layout
app.layout = html.Div([
    # Top half: DataTable
    html.Div([
        dash_table.DataTable(
            id='datatable-interactivity',
            columns=[
                {"name": i, "id": i, "deletable": True, "selectable": True} for i in df.columns
            ],
            data=df.to_dict('records'),
            editable=True,
            filter_action="native",
            sort_action="native",
            sort_mode="multi",
            column_selectable="single",
            row_selectable="multi",
            row_deletable=True,
            selected_columns=[],
            selected_rows=[],
            page_action="native",
            page_current=0,
            page_size=10,
        ),
        html.Div(id='tbl_out', style={'padding': '10px', 'border': '2px solid #d3f3d0', 'border-radius': '5px', 'background-color': '#d3f3d0', 'text-align': 'center'})
    ]),

    # Bottom half: IGV component
    html.Div([
        dcc.Loading(id='igv-loading', children=[
            html.Div(id='igv-output')
        ]),
        html.Hr(),
        html.P('Select the genome to display below.'),
        dcc.Dropdown(
            id='default-igv-genome-select',
            options=HOSTED_GENOME_DICT,
            value='mm10'
        )
    ]),
    dcc.Store(id='track-storage', data=[])
])

# Callback to update display and IGV component
@app.callback(
    [Output('tbl_out', 'children'),
     Output('igv-output', 'children'),
     Output('track-storage', 'data')],
    [Input('datatable-interactivity', 'active_cell'),
     Input('default-igv-genome-select', 'value')],
    [State('track-storage', 'data')]
)
def update_display_and_igv(active_cell, genome, current_tracks):
    tbl_out_content = "Click a cell in the table"
    igv_output_content = []

    if active_cell:
        row = active_cell['row']
        col = df.columns[1]  # Assuming the second column is 'bigWig' URL
        col2 = df.columns[0]
        value = df.iloc[row][col]
        name = df.iloc[row][col2]

        # Ensure URL is correctly formatted and accessible
        track_url = f'{value}'
        track_name = f'Track - {name}'

        # Define the track with the correct URL and other properties
        new_track = {
            'name': track_name,
            'url': track_url,
            'type': 'wig',
            'min': '0',
            'max': '30',
            'color': 'rgb(0, 0, 150)'
        }

        # Append the new track to the current tracks if it doesn't already exist
        if new_track not in current_tracks:
            current_tracks.append(new_track)

        tbl_out_content = html.Div(value, style={'color': 'black', 'font-weight': 'bold', 'padding': '5px', 'display': 'inline-block'})

    igv_output_content = [
        dashbio.Igv(
            id='default-igv',
            genome=genome,
            minimumBases=100,
            tracks=current_tracks
        )
    ]

    return tbl_out_content, igv_output_content, current_tracks

if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=8050, debug=False)
