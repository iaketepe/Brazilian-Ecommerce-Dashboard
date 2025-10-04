import kagglehub
import os

# Download latest version
_ = '''
path = kagglehub.dataset_download("olistbr/brazilian-ecommerce")

print("Path to dataset files:", path)

print("Files:", os.listdir(path))

import pandas as pd

# Dictionary to store DataFrames
dfs = {}

# Load each CSV into a DataFrame
for filename in os.listdir(path):
    file = os.path.join(path, filename)
    df_name = filename.replace('.csv', '')  # e.g., olist_customers_dataset
    dfs[df_name] = pd.read_csv(file)
'''




from dash import Dash, html, dcc, callback, Output, Input, State
import plotly.express as px
import pandas as pd

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv')

app = Dash()

# Requires Dash 2.17.0 or later
app.layout = html.Div([
    # Sidebar
    html.Button(">>",
                id="sidebar-under-button",
                style={
                    "position": "absolute",
                    "top": 20,
                    "left": 20,
                    "display": "block"
                }),
    html.Div(
        [
            html.Button("<<",
                        id="sidebar-button",
                        style={
                            "position": "absolute",
                            "right": 20,
                        }),
            html.Div([
                html.H2("Side Bar"),
                html.Hr(),
                html.H3("Acts"),
                dcc.Link("Act 1", href="/page-1"),
                html.Br(),
                dcc.Link("Act 2", href="/page-2"),
            ],
            id="sidebar-elements"),
        ],
        id="sidebar",
        style={
            "position": "absolute",
            "top": 0,
            "left": 0,
            "bottom": 0,
            "width": "320px",
            "padding": "20px",
            "background-color": "#f8f9fa",
            "transition": "transform 0.3s",
            "zIndex": 1000,
            "overflow": "hidden",
            "display": "none"
        }, # #000000
    ),

    # Page content
    html.Div(
        id="page-content",
        #style={"margin-left": "220px", "padding": "20px"}
    )
])

@app.callback(
    Output("sidebar","style"),
    Input("sidebar-button", "n_clicks"),
    Input("sidebar-under-button", "n_clicks"),
    State("sidebar", "style"),
)
def toggle_sidebar(n_clicks, n_clicks2, sidebar_style):
    if not sidebar_style:
        sidebar_style = {}
    sidebar_style = sidebar_style.copy()

    sidebar_style["display"] = "block"

    # toggle left between hidden and visible
    if sidebar_style.get("transform") == "translateX(-100%)":
        sidebar_style["transform"] = "translateX(0)"
    else:
        sidebar_style["transform"] = "translateX(-100%)"

    return sidebar_style



if __name__ == '__main__':
    app.run(debug=True)
