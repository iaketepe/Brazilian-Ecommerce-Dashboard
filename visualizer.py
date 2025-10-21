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

    def createRatio(self, value, desc):
        value = value * 100  # 75% achieved value=75
        fig = go.Figure(go.Pie(
            values=[value, 100 - value],
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
        return self.createRatio(processor.ratio_delivered_orders_paid_in_full,"<br>Orders Paid<br><b>in full</b><br>with installments")

    def createRatioSellerCarrier(self):
        return self.createRatio(processor.ratio_orders_delivered_shipped,"<br>Orders shipped<br><b>Seller → Carrier</b><br>before deadline")

    def createRatioCarrierCustomer(self):
        return self.createRatio(processor.ratio_orders_estimated_delivered,"<br>Orders Delivered<br><b>Carrier → Customer</b><br>before deadline")



class Visualizer:
    def __init__(self): #, theme="light"):
        #self.theme = theme
        self.acts = {"act_1" : Act1()}



    def get_Acts(self):
        return self.acts


visualizer = Visualizer()