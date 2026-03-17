import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

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
