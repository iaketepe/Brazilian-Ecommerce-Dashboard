# ACT 2:
import pandas as pd
from importlib import resources
import geopandas as gp
import json

def calculate(dfs):
    with resources.path("resources", "gadm41_BRA_1.json") as geofile:
        gdf = gp.read_file(geofile)

    with open(geofile) as f:
        geojson_dict = json.load(f)

    states = (
        gdf[['HASC_1','NAME_1']]
        .drop_duplicates()
        .assign(
            state=lambda x: x['HASC_1'].str.split('.').str[1]
        )
    )

    # 1 Sellers Geographic Distribution
    df_sellers = dfs['olist_sellers_dataset']

    df_sellers_dist = (
        pd.merge(
            states[['NAME_1','state']],
            df_sellers.groupby("seller_state").size().reset_index(name="seller_count"),
            left_on='state',
            right_on='seller_state',
            how='left'
        )
        .fillna({'seller_count': 0})
        .drop(columns=['seller_state'])
    )

    df_sellers_dist['seller_count'] = df_sellers_dist['seller_count'].astype('Int64')

    # 2 Customers Geographic Distribution
    df_customers = dfs['olist_customers_dataset']

    df_customers_dist = (
        pd.merge(
            states[['NAME_1','state']],
            df_customers.groupby("customer_state").size().reset_index(name="customer_count"),
            left_on='state',
            right_on='customer_state',
            how='left'
        )
        .fillna({'customer_count': 0})
        .drop(columns=['customer_state'])
    )

    df_customers_dist['customer_count'] = df_customers_dist['customer_count'].astype('Int64')

    # 2 - Reviews Geographic Distribution

    first_half = pd.merge(
        dfs['olist_order_reviews_dataset'][['order_id', 'review_score']],
        dfs['olist_orders_dataset'][['order_id', 'order_status']],
        on='order_id',
        how='left'
    )

    sec_half = pd.merge(
        dfs['olist_order_items_dataset'][['order_id', 'seller_id']],
        dfs['olist_sellers_dataset'][['seller_id', 'seller_state']],
        on='seller_id',
        how='inner'
    )

    sec_half_agg = sec_half.groupby('order_id').agg({
        'seller_id': 'first',
        'seller_state': 'first'
    }).reset_index()

    orders_sellers = pd.merge(first_half, sec_half_agg, on='order_id', how='inner')

    state_reviews = orders_sellers.groupby('seller_state')['review_score'].mean().reset_index(name='review_score')

    state_reviews = (
        pd.merge(
            states[['NAME_1','state']],
            state_reviews,
            left_on='state',
            right_on='seller_state',
            how='left'
        )
        .fillna({'review_score': 0})
        .drop(columns=['seller_state'])
    )

    state_reviews['review_score'] = state_reviews['review_score'].round(2)

    geo_distributions = pd.merge(df_sellers_dist, df_customers_dist, on=['NAME_1','state'], how='inner')
    geo_distributions = geo_distributions.merge(state_reviews, on=['NAME_1','state'], how='inner')

    geo_distributions.rename(columns={'NAME_1': 'name'}, inplace=True)

    return  {
        "geo_distributions" : geo_distributions.to_dict('records')
    }