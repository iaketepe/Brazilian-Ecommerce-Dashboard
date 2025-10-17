from dash import Dash, html, dcc, Output, Input, State
import plotly.graph_objects as go
from pipeline.running import processor

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
                dcc.Link("Act 1", href="/act-1"),
                html.Br(),
                dcc.Link("Act 2", href="/act-2"),
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
            html.Div([
                dcc.Interval(id='a1-review_intervals', interval=5000, n_intervals=0),
                dcc.Graph(id='a1-review_score'),
                html.Div([
                    html.Span("★", style={'color': 'lightgray'}),
                    html.Span("★", style={'color': 'gold', 'width': '43%', 'overflow': 'hidden', 'display': 'inline-block', "font-size" : 200}),
                ])

            ],
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


@app.callback(
    Output('a1-review_score', 'figure'),
    Input('a1-review_intervals','n_intervals')
)
def review_score(_):
    fig = go.Figure(go.Indicator(
        mode="number+gauge+delta",
        value=processor.review_score_avg,
        title={"text": "Average Review Score"},
        gauge={
            "axis": {"range": [0, 5]},
            "bar": {"color": "green"},
        }
    ))

    return fig



if __name__ == '__main__':
    app.run(debug=True)
