from dash import Dash, html, dcc, Output, Input, State
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from app.simpleDB import SimpleDB

class TableWrapper:
    def __init__(self, tableData):
        self.tableData = tableData
        self._lookup = {rec['name']: rec['value'] for rec in tableData}

    def __getattr__(self, name):
        return self._lookup.get(name)

    def __getitem__(self, name):
        return self._lookup.get(name)


class Act1:
    def __init__(self, actData):
        # Promote each table to an attribute
        for table_name, table in actData.items():
            setattr(self, table_name, table)

    def __getitem__(self, table_name):
        return getattr(self, table_name)

    def annual_revenue_approximated(self):
        fig = go.Figure(go.Indicator(
            mode="number+delta",
            value=float(self.metrics.total_verified_revenue),
            title={"text": "Approximate Total Revenue"},
        ))
        return fig

    def monthly_annual_revenue_approximated(self):
        fig = px.line(
            self.cumulative_revenue,
            x='order_delivered_customer_date',
            y='cumulative_revenue',
            labels={
                'order_delivered_customer_date': 'Timeline',
                'cumulative_revenue': 'Revenue ($)'
            },
            title='Revenue Growth over Time',
        )
        return fig

    def review_score(self):
        fig = go.Figure(go.Indicator(
            mode="number+delta",
            value=float(self.metrics.review_score_avg),
            title={"text": "Average Review Score"},
        ))
        return fig

    def distribution_order_status(self):
        fig = px.bar(
            x=self.order_status.index,
            y=self.order_status.values,
            labels={'x': 'Order Status', 'y': 'Count'},
            title='Distribution of Orders by Status',
            text_auto=True
        )
        return fig

    def createRatio(self, value, desc):
        value = float(value) * 100  # 75% achieved value=75
        fig = go.Figure(go.Pie(
            values=[value, (100 - value)],
            hole=0.95,  # makes it a donut
            marker_colors=['green', 'lightgray'],
            textinfo='none',  # remove labels
        ))
        fig.update_traces(domain=dict(x=[0, 1], y=[0, 1]))
        fig.add_annotation(
            text=f"{int(value)}%",  # text to display
            x=0.5, y=0.5,  # center of the figure
            font=dict(size=40),
            showarrow=False
        )
        fig.update_layout(
            margin=dict(t=100, b=30, l=50, r=50),  # same for all
            title=dict(text=desc, font=dict(size=16),x=0.5, xanchor="center", y=0.95,yanchor="top"),
            showlegend=False,
        )

        return fig

    def createRatioInstallmentsInFull(self):
        return self.createRatio(self.metrics.ratio_delivered_orders_paid_in_full,"<br>Orders Paid<br><b>in full</b><br>with installments")

    def createRatioSellerCarrier(self):
        return self.createRatio(self.metrics.ratio_orders_delivered_shipped,"<br>Orders shipped<br><b>Seller → Carrier</b><br>before deadline")

    def createRatioCarrierCustomer(self):
        return self.createRatio(self.metrics.ratio_orders_estimated_delivered,"<br>Orders Delivered<br><b>Carrier → Customer</b><br>before deadline")

from importlib import resources
import geopandas as gp
import json

with resources.path("resources", "gadm41_BRA_1.json") as geofile:
    gdf = gp.read_file(geofile)

with open(geofile, "r", encoding="utf-8") as f:
    geojson_dict = json.load(f)

class Act2:
    def __init__(self, actData):
        # Promote each table to an attribute
        for table_name, table in actData.items():
            setattr(self, table_name, table)

    def __getitem__(self, table_name):
        return getattr(self, table_name)

    def sellers_distribution(self):
        fig = px.choropleth_mapbox(
            data_frame=self.geo_distributions,
            geojson=geojson_dict,
            locations='name',
            featureidkey='properties.NAME_1',
            hover_name='name',
            hover_data={'seller_count': True},
            title='Geographic Distribution of Olist Sellers Across Brazil',
            color='seller_count',
            color_continuous_scale="blues",
            mapbox_style='carto-positron',
            zoom=4,
            center={"lat": -15.78, "lon": -47.93},
            opacity=0.8
        )
        return fig

    def customers_distribution(self):
        fig = px.choropleth_mapbox(
            data_frame=self.geo_distributions,
            geojson=geojson_dict,
            locations='name',
            featureidkey='properties.NAME_1',
            hover_name='name',
            hover_data={"customer_count": True},
            title='Geographic Distribution of Olist Customers Across Brazil',
            color='customer_count',
            color_continuous_scale="greens",
            mapbox_style='carto-positron',
            zoom=4,
            center={"lat": -15.78, "lon": -47.93},
            opacity=0.8
        )
        return fig

    def seller_review_score_by_state(self):
        fig = px.choropleth_mapbox(
            data_frame=self.geo_distributions,
            geojson=geojson_dict,
            locations='name',
            featureidkey='properties.NAME_1',
            hover_name='name',
            hover_data={"review_score": True},
            title='Geographic Average Olist Seller Reviews By State',
            color='review_score',
            color_continuous_scale=[
                [0, 'white'],
                [0.2, '#d73027'],
                [0.5, 'yellow'],
                [1.0, 'darkgreen']
            ],
            color_continuous_midpoint=2.5,
            mapbox_style='carto-positron',
            zoom=4,
            center={"lat": -15.78, "lon": -47.93},
            opacity=0.8
        )
        return fig


class Visualizer:
    def __init__(self): #, theme="light"):
        #self.theme = theme
        self.simpledb = SimpleDB()

        order_status_data = self.simpledb.get_table("TEST_ACT1","order_status")
        gd = pd.DataFrame(self.simpledb.get_table("TEST_ACT2","geo_distributions"))
        gd['review_score'] = gd['review_score'].astype(float)


        self.acts = {"act_1" : Act1({
            "metrics" : TableWrapper(self.simpledb.get_table("TEST_ACT1","metrics")),
            "order_status" : pd.Series(order_status_data[0])[1:],
            "cumulative_revenue" : self.simpledb.get_table("TEST_ACT1","cumulative_revenue"),
        }),
        #"act_2" : Act2({"geo_distributions" : self.simpledb.get_table("TEST_ACT2","geo_distributions")})}
        "act_2": Act2({"geo_distributions": gd})}

    def get_Acts(self):
        return self.acts


visualizer = Visualizer()