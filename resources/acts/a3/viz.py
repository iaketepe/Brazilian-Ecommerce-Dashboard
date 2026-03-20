import plotly.graph_objects as go
import plotly.express as px
import pandas as pd



class Act3:
    def __init__(self, simpledb, category=None):
        self.categories = sorted(pd.DataFrame(simpledb.get_table("TEST_ACT3", "orders_per_category"))['product_category'].unique().tolist())
        self.category = category or self.categories[0]

        self.orders_per_category = simpledb.get_filtered_table("TEST_ACT3", "orders_per_category", "product_category", category)
        self.top_3_sellers = simpledb.get_filtered_table("TEST_ACT3", "top_3_sellers", "product_category", category)
        self.worst_3_sellers = simpledb.get_filtered_table("TEST_ACT3", "worst_3_sellers", "product_category", category)
        self.reviews_per_category = simpledb.get_filtered_table("TEST_ACT3", "reviews_per_category", "product_category", category)
        self.seller_reviews_per_category = simpledb.get_filtered_table("TEST_ACT3", "seller_reviews_per_category", "product_category", category)


