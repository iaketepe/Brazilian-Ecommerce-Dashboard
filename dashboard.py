from dash import Dash, html, dcc, callback, Output, Input, State
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import processor

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv')

app = Dash()

#"Source Sans", sans-serif background-color: rgb(14, 17, 23);

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
    html.Div([
            html.H1("Brazilian Ecommerce Dashboard",
                    style={
                        "text-align": "center",
                    }
            ),
            html.Div(
                [f"Total Orders: {processor.review_score_avg}"],
                style={
                    "border": "1px solid black",
                    "display" : "flex",
                    "flex": "1 1 0%"
                }
            ),
        ],
        id="page-content",
        style={"padding": "50px",
               "margin-top": "25px",
               "display": "flex",
               "flex-direction": "column",
               }
    )
],
style={
    #"fontFamily": '"Source Sans", sans-serif'
})


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


# plotly test
def review_score(review_score_avg):
    fig = go.Figure(go.Indicator(
        mode="number+gauge+delta",
        value=review_score_avg,
        title={"text": "Average Review Score"},
        gauge={
            "axis": {"range": [0, 5]},
            "bar": {"color": "green"},
        }
    ))

    fig.show()



if __name__ == '__main__':
    app.run(debug=True)
