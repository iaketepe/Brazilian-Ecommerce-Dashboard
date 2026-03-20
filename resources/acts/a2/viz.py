
from importlib import resources
import plotly.graph_objects as go
import plotly.express as px
import geopandas as gp
import pandas as pd
import json

with resources.path("resources", "gadm41_BRA_1.json") as geofile:
    gdf = gp.read_file(geofile)

with open(geofile, "r", encoding="utf-8") as f:
    geojson_dict = json.load(f)

class Act2:
    def __init__(self, simpledb):
        gd = pd.DataFrame(simpledb.get_table("BED_ACT2","geo_distributions"))
        gd['review_score'] = gd['review_score'].astype(float)

        self.geo_distributions = gd

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