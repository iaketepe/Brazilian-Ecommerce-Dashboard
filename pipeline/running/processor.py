from pipeline.running import ingestion, act_processes
from act_processes import a1proc
import pandas as pd

dfs = ingestion.ingest()

acts = {}

acts["ACT1"] = a1proc.calculate(dfs)

from importlib import resources
import geopandas as gp
import json

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
    "geo_distributions" : geo_distributions.to_dict('records')
}


# ACT 3:

### Setting Up

order_items = dfs['olist_order_items_dataset']
order_items = order_items[['order_id','product_id','seller_id','price','freight_value']]

orders = dfs['olist_orders_dataset']
orders = orders[orders['order_status'] == 'delivered']
orders = orders[['order_id','customer_id','order_purchase_timestamp','order_delivered_customer_date','order_estimated_delivery_date']]

order_products = dfs['olist_products_dataset']
order_products = order_products[['product_id','product_category_name','product_photos_qty']]

order_sellers = dfs['olist_sellers_dataset']
order_sellers = order_sellers[['seller_id','seller_state']]

order_customers = dfs['olist_customers_dataset']
order_customers = order_customers[['customer_id','customer_state']]

order_reviews = dfs['olist_order_reviews_dataset']
order_reviews = order_reviews[['order_id','review_score']]

product_category_translation = dfs['product_category_name_translation']

ml_data = order_items.copy()

# join orders
ml_data = ml_data.merge(
    orders,
    on="order_id",
    how="right"
)

# join products
ml_data = ml_data.merge(
    order_products,
    on="product_id",
    how="inner"
)

# join translations
ml_data = ml_data.merge(
    product_category_translation,
    on="product_category_name",
    how="inner"
)

# join sellers
ml_data = ml_data.merge(
    order_sellers,
    on="seller_id",
    how="inner"
)

# join customers
ml_data = ml_data.merge(
    order_customers,
    on="customer_id",
    how="inner"
)

# join reviews (inner join since we need review_score)
ml_data = ml_data.merge(
    order_reviews,
    on="order_id",
    how="inner"
)

ml_data.drop(columns='product_category_name',inplace=True)

ml_data.rename(columns={"product_category_name_english" : "product_category_name"},inplace=True)

ml_data.head()

# 0 - number of orders per product category

orders_per_category = ml_data.groupby('product_category_name')['order_id'].count().reset_index()
orders_per_category.rename(columns={'order_id': 'num_orders'}, inplace=True)

# 1 - number of orders per category relative to total platform orders

total_orders = ml_data['order_id'].nunique()
orders_per_category['platform_share'] = orders_per_category['num_orders'] / total_orders

# 2 & 3 - TOP/WORST 3 sellers per category

seller_category = (
    ml_data.groupby(['product_category_name','seller_id'])
    .agg(v=('review_score','count'), R=('review_score','mean'))
    .reset_index()
)

C = ml_data['review_score'].mean()

category_orders = ml_data.groupby('product_category_name')['order_id'].count().reset_index()
category_products = ml_data.groupby('product_category_name')['product_id'].nunique().reset_index()
category_stats = category_orders.merge(category_products, on='product_category_name')
category_stats['m'] = category_stats['order_id'] / category_stats['product_id']

seller_category = seller_category.merge(category_stats[['product_category_name','m']], on='product_category_name')

seller_category['bayes_score'] = (seller_category['v'] / (seller_category['v'] + seller_category['m'])) * seller_category['R'] \
                                  + (seller_category['m'] / (seller_category['v'] + seller_category['m'])) * C

top_sellers = (
    seller_category
    .sort_values(['product_category_name', 'bayes_score'], ascending=[True, False])
    .groupby('product_category_name', group_keys=False)
    .head(3)
)

worst_sellers = (
    seller_category
    .sort_values(['product_category_name', 'bayes_score'], ascending=[True, True])
    .groupby('product_category_name', group_keys=False)
    .head(3)
)

# 4 - Distribution of review_scores for each product category

categories = ml_data['product_category_name'].unique()
review_bins = {}
for category in categories:
    review_bins[category] = {
        'review_scores': ml_data[ml_data['product_category_name']==category]['review_score']
        .value_counts()
        .reindex([1,2,3,4,5], fill_value=0)
        .to_dict()
    }

# 5 - Histogram of average review_scores per seller in a category

seller_avg = ml_data.groupby(['product_category_name','seller_id'])['review_score'].mean().reset_index()

seller_review_bins = {}
for category in categories:
    seller_review_bins[category] = {
        'review_scores': seller_avg[seller_avg['product_category_name']==category]['review_score']
        .value_counts()
        .reindex([1,2,3,4,5], fill_value=0)
        .to_dict()
    }
