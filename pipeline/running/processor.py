from pipeline.running import ingestion

dfs = ingestion.ingest()

# ACT 1:

# 1: review scores overall average
review_score_avg = dfs['olist_order_reviews_dataset']['review_score'].mean()

