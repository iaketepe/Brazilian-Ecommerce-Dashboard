from dash import Dash, html, dcc, Output, Input, State, callback_context, ctx, Patch
from app.visualizer import visualizer
from waitress import serve
from dotenv import dotenv_values
import dash_ag_grid as dag
import dash_mantine_components as dmc
from dash_iconify import DashIconify
from flask_caching import Cache

config = dotenv_values(".env")
MODE = config.get("MODE")

app = Dash(__name__, suppress_callback_exceptions=True)
cache = Cache(app.server, config={'CACHE_TYPE': 'simple'})
#"Source Sans", sans-serif background-color: rgb(14, 17, 23);

# Requires Dash 2.17.0 or later
base = html.Div([
    dcc.Store(id={'type': 'storage', 'index': 'session'}, storage_type='session'),
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
    dmc.ColorSchemeToggle(
        id="color-scheme-toggle",
        lightIcon=DashIconify(icon="radix-icons:sun", width=20),
        darkIcon=DashIconify(icon="radix-icons:moon", width=20),
        color="yellow",
        size="lg",
        bdrs=100,
        style={
            "border" : "1px solid gray",
            "position": "absolute",
            "top": 20,
            "right": 20,
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
                html.Br(),
                dcc.Link("Act 4", href="/act-4"),
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
            "transform": "translateX(-100%)",
            "transition": "transform 0.3s",
            "zIndex": 1000,
            "overflow": "hidden",
            #"display": "none"
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
            dcc.Loading(
                id="loading",
                overlay_style={"visibility":"visible", "filter": "blur(20px)"},
                color="#1f77b4",
                type="default",
                children=html.Div([],
                    id='act-content',
                    style={
                        "border": "1px solid black",
                        "minHeight" : "90vh"
                        ""
                    }
                ),
                style={

                }

            )
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


app.layout = dmc.MantineProvider(theme={}, children=[dmc.pre_render_color_scheme(), base])

@app.callback(
    Output("loading", "overlay_style"),
    Input("color-scheme-toggle", "computedColorScheme")
)
def update_overlay_style(theme):
    if theme == "dark":
        return {
            "backgroundColor": "rgba(0,0,0,0.15)",
            "border" : "none",
        }
    else:
        return {
            "backgroundColor": "rgba(255,255,255,0.15)",
            "border": "none",
        }

@app.callback(
    Output("sidebar","style"),
    Input("sidebar-button", "n_clicks"),
    Input("sidebar-under-button", "n_clicks"),
    Input("color-scheme-toggle", "computedColorScheme"),
    State("sidebar", "style"),
)
def update_sidebar(n_clicks, n_clicks2, theme, s_style):
    sidebar_style = s_style or {}

    button_id = ctx.triggered_id

    if button_id == "color-scheme-toggle":
        return update_sidebar_color(sidebar_style, theme)
    else:
        return toggle_sidebar(sidebar_style)

def update_sidebar_color(s_style, theme):
    sidebar_style = s_style.copy()
    if theme == "dark":
        sidebar_style["backgroundColor"] = "#0e1117"
    else:
        sidebar_style["backgroundColor"] = "#f8f9fa"

    return sidebar_style

def toggle_sidebar(s_style):
    sidebar_style = s_style.copy()

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
        visualizer.setup_act("act_1")
        return act_1()
    elif pathname == "/act-2":
        visualizer.setup_act("act_2")
        return act_2()
    elif pathname == "/act-3":
        visualizer.setup_act("act_3")
        return act_3()
    elif pathname == "/act-4":
        visualizer.setup_act("act_4")
        return act_4()
    else:
        visualizer.setup_act("act_1")
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
                        #figure=visualizer.acts["act_1"].review_score(),
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
            })
    ])

    return layout


@app.callback(
    Output('a1-review_score', 'figure'),
    Output('a1-annual_revenue', 'figure'),
    Output('a1-ratio_pf', 'figure'),
    Output('a1-ratio_sc', 'figure'),
    Output('a1-ratio_cc', 'figure'),
    Output('a1-order_status', 'figure'),
    Output('a1-revenue_csum', 'figure'),
    Input("color-scheme-toggle", "computedColorScheme"),  # fires on color change
)
def update_act1(theme):
    fig_theme = visualizer.get_theme(theme)

    review_score_fig = visualizer.acts["act_1"].review_score()
    review_score_fig.layout.template = fig_theme

    annual_revenue_fig = visualizer.acts["act_1"].annual_revenue_approximated()
    annual_revenue_fig.layout.template = fig_theme

    ratio_pf_fig = visualizer.acts["act_1"].createRatioInstallmentsInFull()
    ratio_pf_fig.layout.template = fig_theme

    ratio_sc_fig = visualizer.acts["act_1"].createRatioSellerCarrier()
    ratio_sc_fig.layout.template = fig_theme

    ratio_cc_fig = visualizer.acts["act_1"].createRatioCarrierCustomer()
    ratio_cc_fig.layout.template = fig_theme

    order_status_fig = visualizer.acts["act_1"].distribution_order_status()
    order_status_fig.layout.template = fig_theme

    revenue_csum_fig = visualizer.acts["act_1"].monthly_annual_revenue_approximated()
    revenue_csum_fig.layout.template = fig_theme

    return (
        review_score_fig,
        annual_revenue_fig,
        ratio_pf_fig,
        ratio_sc_fig,
        ratio_cc_fig,
        order_status_fig,
        revenue_csum_fig
    )




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
    #ctx = callback_context

    #button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    button_id = ctx.triggered_id

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
                    html.Label("-", id="a3-product_category", style={"width": "100%", "fontSize": "24px", "fontWeight": "bold"}),
                    html.Label(
                        "Product Category"
                    )
                ],
                style={
                    "border": "1px solid black",
                    "textAlign": "center",
                    "display": "flex",
                    "flexDirection": "column",
                    "justifyContent": "center",
                    "overflowX" : "auto",
                    "gap" : "20px",
                    "height": "30%",
                }),
                html.Div([  #a3-selection-query-options
                    html.Div([

                    ],
                    style={
                    }),
                    dmc.Select(
                    id="a3-product_categories",
                    data=[],
                    searchable=True,
                    maxDropdownHeight=400,
                    style={
                    })
                ],
                style={
                    "display": "grid",
                    "gridTemplateRows": ".1fr 1fr",
                    # "display" : "flex",
                    # "height" : "30%"
                }),

            ],
            style={
                    "display" : "flex",
                    "flexDirection": "column",
                    "minWidth": "25%",
                    "width": "25%",
                    "padding" : "20px",
                    "gap" : "20px",
            }),
            html.Div([ #a3-analytics
                html.Div([ #a3-analytics-tophalf
                    html.Div([ #a3-analytics-tophalf-left
                        html.Div([
                            dcc.Graph(
                                id='a3-orders_per_category',
                                config={'staticPlot': True},
                                style={"width": "100%", "height": "100%"}
                            ),
                        ],style = {"flex": "1 1 0"}),
                        html.Div([
                            dcc.Graph(
                                id='a3-platform_share_per_category',
                                config={'staticPlot': True},
                                style={"width": "100%", "height": "100%"}
                            ),
                        ], style={"flex": "1 1 0"})
                    ],
                        style={
                            "display": "flex",
                            "overflowX": "auto",
                            "width": "40%",
                            "flex": "1 1 0"
                        }),
                    html.Div([ #a3-analytics-tophalf-right
                        html.Div([  # Top 3 Sellers
                            html.Label("Top 3 Sellers", style={"fontWeight": "bold"}),
                            html.Div([  # AgGrid container
                                dag.AgGrid(
                                    id="a3-top_sellers",
                                    rowData=[],
                                    columnSize="responsiveSizeToFit",
                                    style={"width": "100%", "height": "100%"}
                                )
                            ], style={"flex": "1 1 0"})
                        ], style={"display": "flex", "flexDirection": "column", "flex": "1 1 0"}),
                        html.Div([  # Worst 3 Sellers
                            html.Label("Worst 3 Sellers", style={"fontWeight": "bold"}),
                            html.Div([  # AgGrid container
                                dag.AgGrid(
                                    id="a3-worst_sellers",
                                    rowData=[],
                                    columnSize="responsiveSizeToFit",
                                    style={"width": "100%", "height": "100%"},
                                )
                            ], style={"flex": "1 1 0"})
                        ], style={"display": "flex", "flexDirection": "column", "flex": "1 1 0"}),
                    ],
                    style={
                        "display": "flex",
                        "flexDirection": "column",
                        "width": "60%",
                        "height": "100%",
                        "overflowX": "auto",
                    }),
                ],
                style={ #a3-analytics-tophalf
                    "display": "flex",
                    "width": "100%",
                    "height": "100%",
                    "overflow": "auto",
                }),
                html.Div([ # a3-analytics-bottomhalf
                    html.Div([
                        dcc.Graph(
                            id="a3-reviews_per_category",
                            style={"width": "100%", "height": "100%"},
                            config={'responsive': True}
                        ),
                    ], style={"gridColumn": "1", "gridRow": "1", "height": "100%", "width": "100%", "overflow": "auto"}),
                    html.Div([
                        dcc.Graph(
                            id="a3-seller_reviews_per_category",
                            style={"width": "100%", "height": "100%"},
                            config={'responsive': True}
                        ),
                    ], style={"gridColumn": "2", "gridRow": "1", "height": "100%", "width": "100%", "overflow": "auto"}),
                ],
                    style={
                        "display" : "grid",
                        "gridTemplateColumns": "1fr 1fr",  # independent two-column layout
                        "overflow": "auto",
                    }),
            ],
            style={ # a3-analytics
                "display": "grid",
                "gridTemplateRows": "40% 60%",
                "width": "80%",
                "height": "100%",
            }),
        ],
        style={ #a3-base
            "display": "flex",
            "width" : "100%",
            "height": "90vh",
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
    Output('a3-top_sellers', 'rowData'),
    Output('a3-top_sellers', 'columnDefs'),
    Output('a3-worst_sellers', 'rowData'),
    Output('a3-worst_sellers', 'columnDefs'),
    Input('a3-product_categories','value'),
)
def update_act3(category):
    visualizer.acts["act_3"].update(category)
    top_3_row_data, top_3_columns_def = get_top_3_sellers()
    worst_3_row_data, worst_3_columns_def = get_worst_3_sellers()
    return get_category(), get_orders_per_category(), get_platform_share_per_category(), get_reviews_per_category(), get_seller_reviews_per_category(), top_3_row_data, top_3_columns_def, worst_3_row_data, worst_3_columns_def

@app.callback(
    Output('a3-product_categories', 'data'), #Output('a3-product_categories', 'options'),
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
    row_data, column_defs = visualizer.acts["act_3"].get_top_3_sellers()
    return row_data, column_defs

def get_worst_3_sellers():
    return visualizer.acts["act_3"].get_worst_3_sellers()


def act_4():
    layout = [
        html.Div([ #a4-base
            html.Div([ #a4-selection
                html.Div([ #a4-selection-model_card
                    html.Label("-", id="a4-model_name", style={"width": "100%", "fontSize": "24px", "fontWeight": "bold"}),
                    html.Label(
                        "Model Name"
                    )
                ],
                style={
                    "border": "1px solid black",
                    "textAlign": "center",
                    "display": "flex",
                    "flexDirection": "column",
                    "justifyContent": "center",
                    "overflowX" : "auto",
                    "gap" : "20px",
                    "height": "30%",
                }),
                html.Div([  #a4-selection-options
                    dmc.Select(
                    id="a4-model_selection",
                    data=[],
                    searchable=True,
                    maxDropdownHeight=400,
                    style={
                    })
                ],
                style={
                }),

            ],
            style={
                    "display" : "flex",
                    "flexDirection": "column",
                    "minWidth": "25%",
                    "width": "25%",
                    "padding" : "20px",
                    "gap" : "20px",
            }),
            html.Div([#a4-model_metrics
                html.Div([#a4-model_core_metrics
                    html.Div([
                        dcc.Graph(
                            id="a4-actual_predicted",
                            style={"width": "100%", "height": "100%"},
                            config={'responsive': True}
                        ),
                    ], style={"gridColumn": "1", "gridRow": "1", "height": "100%", "width": "100%", "overflow": "auto"}),
                    html.Div([
                        dcc.Graph(
                            id="a4-important_features",
                            style={"width": "100%", "height": "100%"},
                            config={'responsive': True}
                        ),
                    ], style={"gridColumn": "2", "gridRow": "1", "height": "100%", "width": "100%", "overflow": "auto"}),
                ],
                style={
                    "border": "1px solid black",
                    "display": "grid",
                    "gridTemplateColumns": "50% 50%",
                }),
                html.Div([ #a4-model_evals
                    html.Label("Evaluation Metrics", style={"fontWeight": "bold"}),
                    html.Div([  # AgGrid container
                        dag.AgGrid(
                            id="a4-model_evals",
                            rowData=[],
                            columnSize="responsiveSizeToFit",
                            style={"width": "100%", "height": "100%"},
                        )
                    ], style={"flex": "1 1 0"})
                ],
                style={
                    "border": "1px solid black",
                    "display": "flex", "flexDirection": "column", "flex": "1 1 0"
                }),
            ],
            style={
                "border" : "1px solid black",
                "display": "grid",
                "gridTemplateRows": "85% 15%",
                "width": "80%",
                "height": "100%",
            }),

        ],
        style={
            "display": "flex",
            "width": "100%",
            "height": "90vh",
        })
    ]
    return layout

@app.callback(
Output('a4-model_name', 'children'),
Output('a4-actual_predicted', 'figure'),
Output('a4-important_features', 'figure'),
    Output('a4-model_evals', 'rowData'),
    Output('a4-model_evals', 'columnDefs'),
    Input('a4-model_selection', 'value'),
)

def update_act4(model_name):
    visualizer.acts["act_4"].update(model_name)
    row_data, column_defs = get_model_evals()
    return get_model(), get_actual_predicted(), get_10_important_features(), row_data, column_defs

@app.callback(
    Output('a4-model_selection', 'data'),
    Input('a4-model_selection','id'),
)

def get_models(_):
    return visualizer.acts["act_4"].get_models()

def get_model():
    return visualizer.acts["act_4"].get_model()

def get_model_evals():
    return visualizer.acts["act_4"].get_model_evals()

def get_10_important_features():
    return visualizer.acts["act_4"].get_10_important_features()

def get_actual_predicted():
    return visualizer.acts["act_4"].get_actual_predicted()


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
