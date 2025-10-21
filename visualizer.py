from dash import Dash, html, dcc, Output, Input, State
import plotly.graph_objects as go
from pipeline.running import processor


class Act1:
    def review_score(self):
        fig = go.Figure(go.Indicator(
            mode="number+delta",
            value=processor.review_score_avg,
            title={"text": "Average Review Score"},
        ))
        return fig

    def annual_revenue_approximated(self):
        fig = go.Figure(go.Indicator(
            mode="number+delta",
            value=processor.total_verified_revenue,
        ))
        return fig


class Visualizer:
    def __init__(self): #, theme="light"):
        #self.theme = theme
        self.acts = {"act_1" : Act1()}



    def get_Acts(self):
        return self.acts


visualizer = Visualizer()