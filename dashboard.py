from dash import Dash, html, dcc, Output, Input, State
import plotly.graph_objects as go
from pipeline.running import processor
from visualizer import visualizer

app = Dash(__name__, suppress_callback_exceptions=True)

#"Source Sans", sans-serif background-color: rgb(14, 17, 23);

# Requires Dash 2.17.0 or later
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),

    # Sidebar
    html.Button(">>",
        id="sidebar-under-button",
        style={
            "position": "absolute",
            "top": 20,
            "left": 20,
            "display": "block"
        }
    ),
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
    html.Div(
        [
            html.H1("Brazilian Ecommerce Dashboard",
                style={
                    "text-align": "center",
                }
            ),
            html.Div([],
                id='act-content',
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
    Output('act-content', 'children'),
    Input('url', 'pathname')
)
def display_page(pathname):
    if pathname == "/act-1":
        return act_1()
    elif pathname == "/act-2":
        return act_2()
    else:
        return act_1()

def act_1():
    layout = [
            dcc.Interval(id='a1-annual_revenue_intervals', interval=10000, n_intervals=0),
            dcc.Graph(id='a1-annual_revenue'),

            html.Div([
                dcc.Interval(id='a1-review_intervals', interval=10000, n_intervals=0),
                dcc.Graph(id='a1-review_score', config={'staticPlot': True}),
                html.Div([
                        html.Span("★", style={'color': 'lightgray'}),
                        html.Span("★",
                                  style={'color': 'gold', 'width': '43%', 'overflow': 'hidden'}),
                    ],
                    style={
                        "font-size": 100,
                        "display": "inline-block"
                    }
                ),
            ],
            style={
                "display": "flex",
                "align-items" : "center",
            })
    ]

    return layout

@app.callback(
    Output('a1-review_score', 'figure'),
    Input('a1-review_intervals','n_intervals'),
)
def review_score(_):
    return visualizer.acts["act_1"].review_score()

@app.callback(
    Output('a1-annual_revenue', 'figure'),
    Input('a1-annual_revenue_intervals','n_intervals')
)
def annual_revenue_approximated(_):
  return visualizer.acts["act_1"].annual_revenue_approximated()


def act_2():
    layout = [

    ]
    return layout




if __name__ == '__main__':
    app.run(debug=True)
