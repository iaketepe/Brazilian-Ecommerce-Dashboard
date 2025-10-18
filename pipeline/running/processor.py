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

# 1: review scores overall average
review_score_avg = dfs['olist_order_reviews_dataset']['review_score'].mean()

