import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from dash import dash_table
import dash_ag_grid as dag


class Act3:
    def __init__(self, simpledb, category=None):
        self.simpledb = simpledb
        self.categories = sorted(pd.DataFrame(self.simpledb.get_table("TEST_ACT3", "orders_per_category"))['product_category'].unique().tolist())

        self.update(category)

    def update(self, category):
        self.category = category or self.categories[0]

        self.orders_per_category = self.simpledb.get_filtered_table("TEST_ACT3", "orders_per_category", "product_category", self.category)[0]
        self.sellers_ranked = pd.DataFrame(self.simpledb.get_filtered_table("TEST_ACT3", "sellers_ranked", "product_category", self.category))
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
            title=f"Distribution of Product Review Scores",
            text_auto=True,
        )
        fig.update_traces(textposition='outside', textfont_size=14)
        return fig

    def get_seller_reviews_per_category(self):
        df = self.sellers_ranked
        df['R'] = pd.to_numeric(df['R'], errors='coerce')
        df['R_rounded'] = df['R'].round(2)

        fig = px.histogram(
            df,
            x=df['R_rounded'],
            labels={'R_rounded' : 'Review Score', 'count': 'Count'},
            nbins=10,
            title=f"Distribution of Seller Average Product Review Scores",
        )

        fig.update_traces(
            xbins=dict(
                start=1.0,  # minimum value
                end=5.01,  # slightly past 5 to include exact 5
                size=0.4  # adjust for number of bins
            ),
        )
        fig.update_xaxes(range=[1, 6])
        return fig

    def get_top_3_sellers(self):
        df = pd.DataFrame(self.top_3_sellers)
        df = df.drop(columns=['product_category', 'm'], errors='ignore')

        df['R'] = pd.to_numeric(df['R'], errors='coerce')
        df['R'] = df['R'].round(2)

        df['bayes_score'] = pd.to_numeric(df['bayes_score'], errors='coerce')
        df['bayes_score'] = df['bayes_score'].round(2)

        df = df.rename(columns={"v" : "Number of Orders", "R" : "Review Score (Avg)", "bayes_score" : "Weighted Score (Avg)"})

        row_data = df.to_dict(orient='records')

        column_defs = [
            {"field": col, "headerName": col.replace("_", " ").title()}
            for col in df.columns
        ]

        return row_data, column_defs

    def get_worst_3_sellers(self):
        df = pd.DataFrame(self.worst_3_sellers)
        df = df.drop(columns=['product_category', 'm'], errors='ignore')

        df['R'] = pd.to_numeric(df['R'], errors='coerce')
        df['R'] = df['R'].round(2)

        df['bayes_score'] = pd.to_numeric(df['bayes_score'], errors='coerce')
        df['bayes_score'] = df['bayes_score'].round(2)

        df = df.rename(columns={"v" : "Number of Orders", "R" : "Review Score (Avg)", "bayes_score" : "Weighted Score (Avg)"})

        row_data = df.to_dict(orient='records')

        column_defs = [
            {"field": col, "headerName": col.replace("_", " ").title()}
            for col in df.columns
        ]

        return row_data, column_defs