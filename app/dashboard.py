from click import style
from dash import Dash, html, dcc, Output, Input, State
import plotly.graph_objects as go
from app.visualizer import visualizer
from waitress import serve

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
    layout = html.Div([
            html.Div([
                html.Div([
                    dcc.Interval(id='a1-annual_revenue_intervals', interval=10000, n_intervals=0),
                    dcc.Graph(
                        id='a1-annual_revenue',
                        style={"width": "100%", "height": "100%"},
                        config={'staticPlot': True}
                    ),
                ],
                    style={
                        "grid-column": "1",
                        "grid-row": "1",
                        "height": "100%",
                    }),

                html.Div([
                    dcc.Interval(id='a1-review_intervals', interval=10000, n_intervals=0),
                    dcc.Graph(
                        id='a1-review_score',
                        style={"width": "100%", "height": "100%"},
                        config={'staticPlot': True}
                    ),
                ],
                    style={
                        "grid-column": "2",
                        "grid-row": "1",
                        "height": "100%",
                    }),
                html.Div([
                    dcc.Interval(id='a1-ratio_pf', interval=10000, n_intervals=0),
                    dcc.Graph(
                        id='a1-ratio_pf',
                        style={"width": "100%", "height": "100%", "aspect-ratio" : "1 / 1","overflow": "visible"},
                        config={'staticPlot': True}
                    ),
                ], style={"grid-column": "3", "grid-row": "1", "height": "100%", "width" : "100%"}),
                html.Div([
                    dcc.Interval(id='a1-ratio_sc', interval=10000, n_intervals=0),
                    dcc.Graph(
                        id='a1-ratio_sc',
                        style={"width": "100%", "height": "100%", "aspect-ratio" : "1 / 1","overflow": "visible"},
                        config={'staticPlot': True}
                    ),
                ], style={"grid-column": "4", "grid-row": "1", "height": "100%", "width" : "100%"}),
                html.Div([
                    dcc.Interval(id='a1-ratio_cc', interval=10000, n_intervals=0),
                    dcc.Graph(
                        id='a1-ratio_cc',
                        style={"width": "100%", "height": "100%", "aspect-ratio" : "1 / 1","overflow": "visible"},
                        config={'staticPlot': True}
                    ),
                ], style={"grid-column": "5", "grid-row": "1", "height": "100%", "width" : "100%"}),
            ],
            style={
                "display": "grid",
                "grid-template-columns": "1.25fr 1fr 1fr 1fr 1fr",
                "grid-gap": 10,
                "align-items": "center",
                "grid-auto-rows": "300px",
                "overflow-x" : "auto"
            }),

            html.Div([
                html.Div([
                    dcc.Interval(id='a1-order_status', interval=10000, n_intervals=0),
                    dcc.Graph(
                        id='a1-order_status',
                        style={"width": "100%", "height": "100%", "aspect-ratio": "1 / 1", "overflow": "visible"},
                        config={'responsive': True}
                    ),
                ], style={"grid-column": "1", "grid-row": "1", "height": "100%", "width": "100%"}),
                html.Div([
                    dcc.Interval(id='a1-revenue_csum', interval=10000, n_intervals=0),
                    dcc.Graph(
                        id='a1-revenue_csum',
                        style={"width": "100%", "height": "100%", "aspect-ratio" : "1 / 1","overflow": "visible"},
                        config={'responsive': True}
                    ),
                ], style={"grid-column": "2", "grid-row": "1", "height": "100%", "width" : "100%"}),
            ], style={
                "display": "grid",
                "grid-template-columns": "1fr 1fr",  # independent two-column layout
                "grid-gap": "10px",
            })
    ])

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

@app.callback(
    Output('a1-ratio_pf', 'figure'),
    Input('a1-ratio_pf','n_intervals')
)
def createRatioInstallmentsInFull(_):
    return visualizer.acts["act_1"].createRatioInstallmentsInFull()

@app.callback(
    Output('a1-ratio_sc', 'figure'),
    Input('a1-ratio_sc', 'n_intervals')
)
def createRatioSellerCarrier(_):
    return visualizer.acts["act_1"].createRatioSellerCarrier()

@app.callback(
    Output('a1-ratio_cc', 'figure'),
    Input('a1-ratio_cc', 'n_intervals')
)
def createRatioCarrierCustomer(_):
    return visualizer.acts["act_1"].createRatioCarrierCustomer()

@app.callback(
    Output('a1-order_status', 'figure'),
    Input('a1-order_status', 'n_intervals')
)
def distribution_order_status(_):
    return visualizer.acts["act_1"].distribution_order_status()

@app.callback(
    Output('a1-revenue_csum', 'figure'),
    Input('a1-revenue_csum', 'n_intervals')
)
def monthly_annual_revenue_approximated(_):
    return visualizer.acts["act_1"].monthly_annual_revenue_approximated()




def act_2():
    layout = [

    ]
    return layout




if __name__ == '__main__':
    serve(
        app,
        host='0.0.0.0',
        port=8050,
        threads=8
    )
    _= """app.run(
        debug=False,
        host='0.0.0.0',
        port=8050
    )"""
