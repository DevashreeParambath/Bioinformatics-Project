from dash import Dash, dash_table, dcc, html, Input, Output, callback
import pandas as pd

df = pd.read_csv('https://raw.githubusercontent.com/ThomasCarroll/Bioinformatics-Project/main/DashDataTable.csv', index_col=0)

app = Dash(__name__)

app.layout = html.Div([
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
    html.Div(id='tbl_out', style={'padding': '10px', 'border': '2px solid #d3f3d0', 'border-radius': '5px', 'background-color': '#d3f3d0', 'text-align': 'center'})  # Center align text
])

@app.callback(
    Output('tbl_out', 'children'),
    Input('datatable-interactivity', 'active_cell')
)
def display_second_column_content(active_cell):
    if active_cell:
        row = active_cell['row']
        col = df.columns[1]  # Assuming the second column is 'bigWig'
        value = df.iloc[row][col]
        return html.Div(value, style={'color': 'black', 'font-weight': 'bold', 'padding': '5px', 'display': 'inline-block'})
    else:
        return "Click a cell in the table"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8050", debug=False)