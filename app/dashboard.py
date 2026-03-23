from click import style
from dash import Dash, html, dcc, Output, Input, State, callback_context
from app.visualizer import visualizer
from waitress import serve
from dotenv import dotenv_values

config = dotenv_values(".env")
MODE = config.get("MODE")

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
                html.Br(),
                dcc.Link("Act 3", href="/act-3"),
            ],
            id="sidebar-elements"),
        ],
        id="sidebar",
        style={
            "position": "fixed",
            "top": 0,
            "left": 0,
            "height" : "100vh",
            "width": "320px",
            "padding": "20px",
            "backgroundColor": "#f8f9fa",
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
                    "textAlign": "center",
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
               "marginTop": "25px",
               "display": "flex",
               "flexDirection": "column",
               #"width" : "100%",
               #"height" : "100%"
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
    elif pathname == "/act-3":
        return act_3()
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
                        "gridColumn": "1",
                        "gridRow": "1",
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
                        "gridColumn": "2",
                        "gridRow": "1",
                        "height": "100%",
                    }),
                html.Div([
                    dcc.Graph(
                        id='a1-ratio_pf',
                        style={"width": "100%", "height": "100%", "aspectRatio" : "1 / 1","overflow": "visible"},
                        config={'staticPlot': True}
                    ),
                ], style={"gridColumn": "3", "gridRow": "1", "height": "100%", "width" : "100%"}),
                html.Div([
                    dcc.Graph(
                        id='a1-ratio_sc',
                        style={"width": "100%", "height": "100%", "aspectRatio" : "1 / 1","overflow": "visible"},
                        config={'staticPlot': True}
                    ),
                ], style={"gridColumn": "4", "gridRow": "1", "height": "100%", "width" : "100%"}),
                html.Div([
                    dcc.Graph(
                        id='a1-ratio_cc',
                        style={"width": "100%", "height": "100%", "aspectRatio" : "1 / 1","overflow": "visible"},
                        config={'staticPlot': True}
                    ),
                ], style={"gridColumn": "5", "gridRow": "1", "height": "100%", "width" : "100%"}),
            ],
            style={
                "display": "grid",
                "gridTemplateColumns": "1.25fr 1fr 1fr 1fr 1fr",
                "gridGap": 10,
                "alignItems": "center",
                "gridAutoRows": "300px",
                "overflowX" : "auto"
            }),

            html.Div([
                html.Div([
                    dcc.Graph(
                        id='a1-order_status',
                        style={"width": "100%", "height": "100%", "aspectRatio": "1 / 1", "overflow": "visible"},
                        config={'responsive': True}
                    ),
                ], style={"gridColumn": "1", "gridRow": "1", "height": "100%", "width": "100%"}),
                html.Div([
                    dcc.Graph(
                        id='a1-revenue_csum',
                        style={"width": "100%", "height": "100%", "aspectRatio" : "1 / 1","overflow": "visible"},
                        config={'responsive': True}
                    ),
                ], style={"gridColumn": "2", "gridRow": "1", "height": "100%", "width" : "100%"}),
            ], style={
                "display": "grid",
                "gridTemplateColumns": "1fr 1fr",  # independent two-column layout
                "gridGap": "10px",
            })
    ])

    return layout

@app.callback(
    Output('a1-review_score', 'figure'),
    Input('a1-review_score','id'),
)
def review_score(_):
    return visualizer.acts["act_1"].review_score()

@app.callback(
    Output('a1-annual_revenue', 'figure'),
    Input('a1-annual_revenue','id')
)
def annual_revenue_approximated(_):
  return visualizer.acts["act_1"].annual_revenue_approximated()

@app.callback(
    Output('a1-ratio_pf', 'figure'),
    Input('a1-ratio_pf','id')
)
def createRatioInstallmentsInFull(_):
    return visualizer.acts["act_1"].createRatioInstallmentsInFull()

@app.callback(
    Output('a1-ratio_sc', 'figure'),
    Input('a1-ratio_sc', 'id')
)
def createRatioSellerCarrier(_):
    return visualizer.acts["act_1"].createRatioSellerCarrier()

@app.callback(
    Output('a1-ratio_cc', 'figure'),
    Input('a1-ratio_cc', 'id')
)
def createRatioCarrierCustomer(_):
    return visualizer.acts["act_1"].createRatioCarrierCustomer()

@app.callback(
    Output('a1-order_status', 'figure'),
    Input('a1-order_status', 'id')
)
def distribution_order_status(_):
    return visualizer.acts["act_1"].distribution_order_status()

@app.callback(
    Output('a1-revenue_csum', 'figure'),
    Input('a1-revenue_csum', 'id')
)
def monthly_annual_revenue_approximated(_):
    return visualizer.acts["act_1"].monthly_annual_revenue_approximated()




def act_2():
    layout = [
        html.Div([
            html.Div([
                html.Div([
                    html.Button("Sellers", id="btn-sellers", n_clicks=0),
                    html.Button("Customers", id="btn-customers", n_clicks=0),
                    html.Button("Reviews", id="btn-reviews", n_clicks=0),
                ],
                style={
                    "display": "flex",
                    "flexDirection": "row",
                    "gap" : "5px",
                    "borderRadius" : "100%"
                    #"height": "50%",
                    #"maxHeight": "50%",
                })
            ],
            style={
                "display": "flex",
                "justifyContent": "center",
                "width": "100%",
                "paddingTop" : "20px",
                #"maxWidth": "15%",
                #"height": "100%",
            }),
            html.Div([
                dcc.Graph(
                    id="a2-distribution",
                    style={"width": "100%", "height": "100%"}
                )
            ],
            style={
                #"width": "70%",
                #"height": "100%",
                "display" : "flex",
                "flex" : "1",
                #"aspectRatio" : "1.5 / 1",
            }),
        ],
        style={
            "display": "flex",
            "flexDirection": "column",
            "width" : "100%",
            "height": "90vh",
            #"divide" : "divi"
        })
    ]
    return layout

@app.callback(
    Output('a2-distribution', 'figure'),
    [
        Input("btn-sellers", "n_clicks"),
        Input("btn-customers", "n_clicks"),
        Input("btn-reviews", "n_clicks"),
    ],
)
def render_a2_graph(sellers_clicks, customers_clicks, reviews_clicks):
    ctx = callback_context

    button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if button_id == "btn-sellers":
        return visualizer.acts["act_2"].sellers_distribution()

    if button_id == "btn-customers":
        return visualizer.acts["act_2"].customers_distribution()

    if button_id == "btn-reviews":
        return visualizer.acts["act_2"].seller_review_score_by_state()

    # Fallback
    return visualizer.acts["act_2"].sellers_distribution()


def act_3():
    layout = [
        html.Div([ #a3-base
            html.Div([ #a3-selection
                html.Div([ #a3-selection-product_category_card
                    html.H2("Name", id="a3-product_category"),
                    html.Label(
                        "Product Category"
                    ),
                ],
                style={
                    "border": "1px solid black",
                    "display" : "flex",
                    "flexDirection": "column",
                    "justifyContent": "center",
                    "alignItems": "center",
                    #"height" : "30%"
                }),
                html.Div([  #a3-selection-query-options
                    html.Div([

                    ],
                    style={
                        "border": "1px solid black",
                    }),
                    dcc.Dropdown([ #a3-selection-product_categories

                    ],
                    id="a3-product_categories",
                    style={

                    })
                ],
                style={
                    "border": "1px solid black",
                    "display": "grid",
                    "gridTemplateRows": ".1fr 1fr",
                    # "display" : "flex",
                    # "height" : "30%"
                }),

            ],
            style={
                    "border" : "1px solid black",
                    "display" : "grid",
                    "gridTemplateRows" : ".3fr 1fr",
                    "width" : "20%",
                    "padding" : "20px",
                    "gap" : "20px",
            }),
            html.Div([ #a3-analytics
                html.Div([ #a3-analytics-tophalf
                    html.Div([ #a3-analytics-tophalf-left
                        html.Div([
                            dcc.Graph(
                                id='a3-orders_per_category',
                                config={'staticPlot': True}
                            ),
                        ],
                        style={
                        }),
                        html.Div([
                            dcc.Graph(
                                id='a3-platform_share_per_category',
                                config={'staticPlot': True}
                            ),
                        ],
                        style={
                        })
                    ],
                        style={
                            "border": "1px solid black",
                            "display": "grid",
                            "gridTemplateColumns": "1fr 1fr",
                        }),
                    html.Div([ #a3-analytics-tophalf-right
                        html.Div([
                            html.Label("Top 3 Sellers",style={"display":"flex"}),
                            html.Div([

                            ],
                            id='a3-top_sellers',
                            )
                        ],
                        style={

                        }),
                        html.Div([
                            html.Label("Worst 3 Sellers"),
                            html.Div([

                            ],
                            id='a3-worst_sellers',
                            )
                        ],
                        style={
                            "border": "1px solid black",
                        })
                    ],
                        style={
                            "display": "grid",
                            "gridTemplateRows": "1fr 1fr",  # independent two-column layout
                        }),
                ],
                style={ #
                    "display": "grid",
                    "gridTemplateColumns": ".8fr 1.2fr",  # independent two-column layout
                    "border": "1px solid black",
                    "height" : "40%",
                }),
                html.Div([ # a3-analytics-bottomhalf
                    html.Div([
                        dcc.Graph(
                            id="a3-reviews_per_category",
                            config={'staticPlot': True}
                        ),
                    ],
                    style={
                        "border": "1px solid black",
                    }),
                    html.Div([
                        dcc.Graph(
                            id="a3-seller_reviews_per_category",
                            style={"overflow": "visible"},
                            config={'staticPlot': True}
                        ),
                    ],
                    style={
                        "border": "1px solid black",
                    }),
                ],
                    style={
                        "display" : "grid",
                        "gridTemplateColumns": "1fr 1fr",  # independent two-column layout
                        "height" : "60%",
                    }),
            ],
            style={ # a3-analytics
                    "display" : "flex",
                    "flexDirection": "column",
                    "width" : "80%",
            }),
        ],
        style={ #a3-base
            "display": "flex",
            "width" : "100%",
            "height": "90vh",
            "flexBasis" : "1/3 2/3",
            #"divide" : "divi"
        })
    ]
    return layout

@app.callback(
    Output('a3-product_category', 'children'),
    Output('a3-orders_per_category', 'figure'),
    Output('a3-platform_share_per_category', 'figure'),
    Output('a3-reviews_per_category', 'figure'),
    Output('a3-seller_reviews_per_category', 'figure'),
    Output('a3-top_sellers', 'children'),
    Output('a3-worst_sellers', 'children'),
    Input('a3-product_categories','value'),
)
def update_act3(category):
    visualizer.acts["act_3"].update(category)
    return get_category(), get_orders_per_category(), get_platform_share_per_category(), get_reviews_per_category(), get_seller_reviews_per_category(), get_top_3_sellers(), get_worst_3_sellers()

@app.callback(
    Output('a3-product_categories', 'options'),
    Input('a3-product_categories','id'),
)
def get_categories(_):
    return visualizer.acts["act_3"].get_categories()

def get_category():
    return visualizer.acts["act_3"].get_category()

def get_orders_per_category():
    return visualizer.acts["act_3"].get_orders_per_category()

def get_platform_share_per_category():
    return visualizer.acts["act_3"].get_platform_share_per_category()

def get_reviews_per_category():
    return visualizer.acts["act_3"].get_reviews_per_category()

def get_seller_reviews_per_category():
    return visualizer.acts["act_3"].get_seller_reviews_per_category()

def get_top_3_sellers():
    return visualizer.acts["act_3"].get_top_3_sellers()

def get_worst_3_sellers():
    return visualizer.acts["act_3"].get_worst_3_sellers()

if __name__ == '__main__':
    if MODE == "main":
       serve(
            app,
            host='0.0.0.0',
            port=8050,
            threads=8
        )
    else:
        app.run(
            debug=True,
            host='0.0.0.0',
            port=8050
        )
