from dash import Dash, html, dcc, Output, Input, State
import plotly.graph_objects as go
import plotly.express as px
from pipeline.running import processor


class Act1:
    def annual_revenue_approximated(self):
        fig = go.Figure(go.Indicator(
            mode="number+delta",
            value=processor.total_verified_revenue,
            title={"text": "Approximate Annual Revenue"},
        ))
        return fig

    def monthly_annual_revenue_approximated(self):
        fig = px.line(processor.df_delivered_revenue, x='order_delivered_customer_date', y='cumulative_revenue')
        return fig

    def review_score(self):
        fig = go.Figure(go.Indicator(
            mode="number+delta",
            value=processor.review_score_avg,
            title={"text": "Average Review Score"},
        ))
        return fig

    def distribution_order_status(self):
        fig = px.histogram(
            processor.dfs['olist_orders_dataset'],
            x='order_status',
            title='Distribution of Orders by Status',
            text_auto=True  # adds count labels on top
        )
        return fig

    def createRatio(value, desc):
        value = value * 100  # 75% achieved value=75
        fig = go.Figure(go.Pie(
            values=[value, 100 - value],
            hole=0.95,  # makes it a donut
            marker_colors=['green', 'lightgray'],
            textinfo='none',  # remove labels
            hoverinfo='label+percent'
        ))
        fig.add_annotation(
            text=f"{int(value)}%",  # text to display
            x=0.5, y=0.7,  # center of the figure
            font_size=100,
            showarrow=False
        )
        fig.add_annotation(
            text=f"{desc}",
            x=0.5, y=0.2,  # center of the figure
            font_size=30,
            showarrow=False
        )
        fig.update_layout(
            showlegend=False,
            margin=dict(t=20, b=20, l=20, r=20)
        )

        config = {
            'staticPlot': False
        }

        return fig


class Visualizer:
    def __init__(self): #, theme="light"):
        #self.theme = theme
        self.acts = {"act_1" : Act1()}



    def get_Acts(self):
        return self.acts


visualizer = Visualizer()