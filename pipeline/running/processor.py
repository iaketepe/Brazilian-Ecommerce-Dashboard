from pipeline.running import ingestion

dfs = ingestion.ingest()

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
df_delivered_revenue = df_delivered_revenue.sort_values('order_delivered_customer_date')

df_delivered_revenue['cumulative_revenue'] = df_delivered_revenue['payment_value'].cumsum()

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

