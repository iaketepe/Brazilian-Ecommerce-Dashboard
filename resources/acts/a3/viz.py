import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from dash import dash_table


class Act3:
    def __init__(self, simpledb, category=None):
        self.simpledb = simpledb
        self.categories = sorted(pd.DataFrame(self.simpledb.get_table("TEST_ACT3", "orders_per_category"))['product_category'].unique().tolist())

        self.update(category)

    def update(self, category):
        self.category = category or self.categories[0]

        self.orders_per_category = self.simpledb.get_filtered_table("TEST_ACT3", "orders_per_category", "product_category", self.category)[0]
        self.top_3_sellers = pd.DataFrame(self.simpledb.get_filtered_table("TEST_ACT3", "top_3_sellers", "product_category", self.category))
        self.worst_3_sellers = self.simpledb.get_filtered_table("TEST_ACT3", "worst_3_sellers", "product_category", self.category)

        self.reviews_per_category = pd.Series(self.simpledb.get_filtered_table("TEST_ACT3", "reviews_per_category", "product_category", self.category)[0])
        self.reviews_per_category.drop('product_category', inplace=True)

        self.seller_reviews_per_category = pd.Series(self.simpledb.get_filtered_table("TEST_ACT3", "seller_reviews_per_category", "product_category", self.category)[0])
        self.seller_reviews_per_category.drop('product_category', inplace=True)

    def get_category(self):
        return self.category

    def get_categories(self):
        return self.categories

    def get_orders_per_category(self):
        fig = go.Figure(go.Indicator(
            mode="number",
            value=self.orders_per_category['num_orders'],
            title={"text": "Number of Orders"},
        ))
        return fig

    def get_platform_share_per_category(self):
        fig = go.Figure(go.Indicator(
            mode="number",
            value=float(self.orders_per_category['platform_share']) * 100,
            number={"suffix": "%"},
            title={"text": "Platform Order Share"}
        ))
        return fig

    def get_reviews_per_category(self):
        fig = px.bar(
            x=self.reviews_per_category.index,
            y=self.reviews_per_category.values,
            labels={'x' : 'Review Score', 'y': 'Count'},
            title=f"Distribution of Review Scores for {self.category} Products",
            text_auto=True,
        )
        fig.update_traces(textposition='outside', textfont_size=14)
        return fig

    def get_seller_reviews_per_category(self):
        fig = px.bar(
            x=self.seller_reviews_per_category.index,
            y=self.seller_reviews_per_category.values,
            labels={'x' : 'Review Score', 'y': 'Count'},
            title=f"Distribution of {self.category} Sellers Average Review Scores",
            text_auto=True,
        )
        fig.update_traces(textposition='outside', textfont_size=14)
        return fig

    def get_top_3_sellers(self):
        df = pd.DataFrame(self.top_3_sellers)
        df = df.drop(columns=['product_category'], errors='ignore')
        self.top_3_sellers = df.to_dict(orient='records')

        return dash_table.DataTable(
            self.top_3_sellers
        )

    def get_worst_3_sellers(self):
        df = pd.DataFrame(self.worst_3_sellers)
        df = df.drop(columns=['product_category'], errors='ignore')
        self.worst_3_sellers = df.to_dict(orient='records')

        return dash_table.DataTable(
            self.worst_3_sellers
        )