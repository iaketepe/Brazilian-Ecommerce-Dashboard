# ACT 3:
import pandas as pd

def setting_up_calculations(dfs):
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

    ml_data.rename(columns={"product_category_name_english" : "product_category"},inplace=True)

    return ml_data

def calculate(dfs):
    ml_data = setting_up_calculations(dfs)

    # 0 - number of orders per product category

    orders_per_category = ml_data.groupby('product_category')['order_id'].count().reset_index()
    orders_per_category.rename(columns={'order_id': 'num_orders'}, inplace=True)

    # 1 - number of orders per category relative to total platform orders

    total_orders = ml_data['order_id'].nunique()
    orders_per_category['platform_share'] = orders_per_category['num_orders'] / total_orders
    orders_per_category = orders_per_category.to_dict(orient='records')

    # 2 & 3 - TOP/WORST 3 sellers per category

    seller_category = (
        ml_data.groupby(['product_category','seller_id'])
        .agg(v=('review_score','count'), R=('review_score','mean'))
        .reset_index()
    )

    C = ml_data['review_score'].mean()

    category_orders = ml_data.groupby('product_category')['order_id'].count().reset_index()
    category_products = ml_data.groupby('product_category')['product_id'].nunique().reset_index()
    category_stats = category_orders.merge(category_products, on='product_category')
    category_stats['m'] = category_stats['order_id'] / category_stats['product_id']

    seller_category = seller_category.merge(category_stats[['product_category','m']], on='product_category')

    seller_category['bayes_score'] = (seller_category['v'] / (seller_category['v'] + seller_category['m'])) * seller_category['R'] \
                                      + (seller_category['m'] / (seller_category['v'] + seller_category['m'])) * C

    top_sellers = (
        seller_category
        .sort_values(['product_category', 'bayes_score'], ascending=[True, False])
        .groupby('product_category', group_keys=False)
        .head(3)
        .to_dict(orient='records')
    )

    worst_sellers = (
        seller_category
        .sort_values(['product_category', 'bayes_score'], ascending=[True, True])
        .groupby('product_category', group_keys=False)
        .head(3)
        .to_dict(orient='records')
    )

    # 4 - Distribution of review_scores for each product category

    categories = ml_data['product_category'].unique()
    reviews_per_category = []
    for category in categories:
        review_bins = (
            ml_data[ml_data['product_category'] == category]['review_score']
            .value_counts()
            .reindex([1,2,3,4,5], fill_value=0)
            .rename(lambda x: str(x))
            .to_dict()
        )
        category_record = {"product_category" : category, **review_bins}
        reviews_per_category.append(category_record)

    # 5 - Histogram of average review_scores per seller in a category

    seller_avg = ml_data.groupby(['product_category','seller_id'])['review_score'].mean().reset_index()

    seller_reviews_per_category = []
    for category in categories:
        seller_review_bins = (
            seller_avg[seller_avg['product_category'] == category]['review_score']
            .value_counts()
            .reindex([1,2,3,4,5], fill_value=0)
            .rename(lambda x: str(x))
            .to_dict()
        )
        category_record = {"product_category" : category, **seller_review_bins}
        seller_reviews_per_category.append(category_record)

    return {
        "orders_per_category" : orders_per_category,
        "sellers_ranked" : seller_category.to_dict(orient='records'),
        "top_3_sellers" : top_sellers,
        "worst_3_sellers": worst_sellers,
        "reviews_per_category" : reviews_per_category,
        "seller_reviews_per_category" : seller_reviews_per_category,
    }