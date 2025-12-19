from pipeline.running import ingestion
import pandas as pd

dfs = ingestion.ingest()

acts = {}

# ACT 1:

# 0: BIG NUMBER - Approximate Annual Revenue
delivered_orders = dfs['olist_orders_dataset'][dfs['olist_orders_dataset']['order_status'] == 'delivered']

delivered_orders = delivered_orders[delivered_orders['order_delivered_customer_date'].notna()]

# take just the columns you need
df_payments = dfs['olist_order_payments_dataset'][['order_id', 'payment_value']]

# group by order_id and sum the payments
df_revenue = df_payments.groupby('order_id', as_index=False).sum()


df_delivered_revenue = df_revenue.merge(
    delivered_orders[['order_id','order_delivered_customer_date']],
    on='order_id',
    how='inner'
)

total_verified_revenue = df_delivered_revenue['payment_value'].sum()

# 1: Cumulative Approximate Annual Revenue

df_month_delivered_revenue = df_delivered_revenue.copy()
df_month_delivered_revenue['order_delivered_customer_date'] = pd.to_datetime(df_month_delivered_revenue['order_delivered_customer_date'])
df_month_delivered_revenue = df_month_delivered_revenue.groupby(
    df_month_delivered_revenue['order_delivered_customer_date'].dt.to_period('M')
)['payment_value'].sum().reset_index(name='monthly_revenue')

df_month_delivered_revenue['order_delivered_customer_date'] = df_month_delivered_revenue['order_delivered_customer_date'].astype(str)

df_month_delivered_revenue['cumulative_revenue'] = df_month_delivered_revenue['monthly_revenue'].cumsum()

month_delivered_revenue = df_month_delivered_revenue.to_dict(orient='records')

_ = """df_delivered_revenue = df_delivered_revenue.sort_values('order_delivered_customer_date')

df_delivered_revenue['cumulative_revenue'] = df_delivered_revenue['payment_value'].cumsum()"""

# 2: review scores overall average
review_score_avg = dfs['olist_order_reviews_dataset']['review_score'].mean()
review_score_max = dfs['olist_order_reviews_dataset']['review_score'].max()

# 3 Ratio of Orders shipped from seller to carrier before deadline:

delivered_orders_carrier_dates = delivered_orders[['order_id','order_delivered_carrier_date']]

seller_shipping_limits = dfs['olist_order_items_dataset'][['order_id','shipping_limit_date']].copy()
seller_shipping_limits = seller_shipping_limits.drop_duplicates(subset='order_id', keep='last')

orders_seller_carrier = delivered_orders_carrier_dates.copy()
orders_seller_carrier = delivered_orders_carrier_dates.merge(
    seller_shipping_limits,
    on='order_id',
    how='inner'  # only keep orders that exist in both
)

orders_delivered_shipped_sum = (orders_seller_carrier['order_delivered_carrier_date'] <= orders_seller_carrier['shipping_limit_date']).sum()
ratio_orders_delivered_shipped = orders_delivered_shipped_sum / orders_seller_carrier.shape[0]


# 4 Ratio of Orders paid in full with installments

df_payment_installments = df_delivered_revenue.copy()

df_payment_installments = df_payment_installments.merge(
    dfs['olist_order_items_dataset'][['order_id','price']],
    on='order_id',
    how='inner'
)

delivered_orders_paid_in_full_sum = (df_payment_installments['payment_value'] >= df_payment_installments['price']).sum()
ratio_delivered_orders_paid_in_full = delivered_orders_paid_in_full_sum / df_payment_installments.shape[0]

# 5 Ratio of Orders delivered to customer before or on deadline:

orders_estimated_delivered_sum = (delivered_orders['order_delivered_customer_date'] <= delivered_orders['order_estimated_delivery_date']).sum()
ratio_orders_estimated_delivered = orders_estimated_delivered_sum / delivered_orders.shape[0]

# 6 Distribution of Orders by Status

acts["ACT1"] = {
        "metrics": [
            {
                "name": "total_verified_revenue",
                "description": "Total approximate annual revenue from delivered orders",
                "value": float(total_verified_revenue)
            },
            {
                "name": "review_score_avg",
                "description": "Average review score of all orders",
                "value": float(review_score_avg)
            },
            {
                "name": "review_score_max",
                "description": "Maximum review score of all orders",
                "value": float(review_score_max)
            },
            {
                "name": "ratio_orders_delivered_shipped",
                "description": "Ratio of orders shipped before shipping limit date",
                "value": float(ratio_orders_delivered_shipped)
            },
            {
                "name": "ratio_delivered_orders_paid_in_full",
                "description": "Ratio of delivered orders paid in full",
                "value": float(ratio_delivered_orders_paid_in_full)
            },
            {
                "name": "ratio_orders_estimated_delivered",
                "description": "Ratio of orders delivered on or before estimated delivery date",
                "value": float(ratio_orders_estimated_delivered)
            },
        ],

        "cumulative_revenue": month_delivered_revenue, #df_delivered_revenue[['order_id', 'order_delivered_customer_date', 'cumulative_revenue']].to_dict(orient='records'),


        "order_status": [
            dfs['olist_orders_dataset']['order_status']
            .value_counts()
            .to_dict()
        ]
    }

import geopandas as gp
import json

geofile = "../../gadm41_BRA_1.json"
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

acts["ACT2"] = {
    "geo_distributions" : geo_distributions
}