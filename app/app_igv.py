import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import dash_bio as dashbio

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H1("Genomics Data Viewer", className="text-center"), className="mb-5 mt-5")
        ]),
        dbc.Row([
            dbc.Col([
                dcc.Dropdown(
                    id='dropdown-dataset',
                    options=[
                        {'label': 'Dataset 1', 'value': 'dataset1'},
                        {'label': 'Dataset 2', 'value': 'dataset2'}
                    ],
                    value='dataset1',
                    className='mb-3'
                ),
                dashbio.Igv(
                    id='genome-viewer',
                    genome='hg38'
                )
            ])
        ])
    ])
])

@app.callback(
    Output('genome-viewer', 'tracks'),
    [Input('dropdown-dataset', 'value')]
)
def update_tracks(selected_dataset):
    if selected_dataset == 'dataset1':
        tracks = [
            {
                'name': 'BigWigA',
                'url': 'https://www.encodeproject.org/files/ENCFF297ACQ/@@download/ENCFF297ACQ.bigWig',
                'format': 'bigwig',
                'type': 'wig',
                'min': '0',
                'max': '30',
                'color': 'rgb(0, 0, 150)'
            }
        ]
    else:
        tracks = [
            {
                'name': 'BigWigB',
                'url': 'https://www.encodeproject.org/files/ENCFF297ACQ/@@download/ENCFF297ACQ.bigWig',
                'format': 'bigwig',
                'type': 'wig',
                'min': '0',
                'max': '30',
                'color': 'rgb(0, 0, 150)'
            }
        ]
    return tracks

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8050", debug=True)
