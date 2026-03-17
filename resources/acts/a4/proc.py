## ACT 4
import pandas as pd
import numpy as np

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

    ml_data.rename(columns={"product_category_name_english" : "product_category_name"},inplace=True)

    return ml_data


def calculate(dfs):
    ml_data = setting_up_calculations(dfs)

    ml_data['product_id'].value_counts()

    ml_data['is_delivered'] = ml_data['order_delivered_customer_date'].notnull().astype(int)

    ml_data['delivery_time'] = (
            ml_data['order_delivered_customer_date'] -
            ml_data['order_purchase_timestamp']
    ).dt.days

    ml_data['difference_delivery_time'] = (
            ml_data['order_delivered_customer_date'] -
            ml_data['order_estimated_delivery_date']
    ).dt.days

    ml_data['delivery_time'] = ml_data['delivery_time'].fillna(ml_data['delivery_time'].median())
    ml_data['difference_delivery_time'] = ml_data['difference_delivery_time'].fillna(0)
    ml_data['product_photos_qty'] = ml_data['product_photos_qty'].fillna(0)

    ml_data['delay_days'] = (
            ml_data['order_delivered_customer_date'] -
            ml_data['order_estimated_delivery_date']
    ).dt.days

    ml_data['delay_days'] = ml_data['delay_days'].clip(lower=0)

    ml_data['delay_days'] = ml_data['delay_days'].fillna(0)

    k = 3
    ml_data['delay_scaled'] = 1 - np.power(2, -ml_data['delay_days'] / k)

    ml_data['early_days'] = (
            ml_data['order_estimated_delivery_date'] -
            ml_data['order_delivered_customer_date']
    ).dt.days

    ml_data['early_days'] = ml_data['early_days'].clip(lower=0)

    ml_data['early_days'] = ml_data['early_days'].fillna(0)

    k = 3
    ml_data['early_scaled'] = 1 - np.power(2, -ml_data['early_days'] / k)

    ml_data = pd.get_dummies(
        ml_data,
        columns=[
            'product_category_name',
            'seller_state',
            'customer_state'
        ],
        drop_first=True
    )

    X = ml_data.drop(columns=[
        'review_score',
        'order_id',
        'product_id',
        'seller_id',
        'customer_id',
        'order_purchase_timestamp',
        'order_delivered_customer_date',
        'order_estimated_delivery_date'
    ])

    y = ml_data['review_score']

    ml_data.head()
