import kagglehub
import os

# Download latest version

path = kagglehub.dataset_download("olistbr/brazilian-ecommerce")

print("Path to dataset files:", path)

print("Files:", os.listdir(path))

import pandas as pd

# Dictionary to store DataFrames
dfs = {}

# Load each CSV into a DataFrame
for filename in os.listdir(path):
    file = os.path.join(path, filename)
    df_name = filename.replace('.csv', '')  # e.g., olist_customers_dataset
    dfs[df_name] = pd.read_csv(file)







# ACT 1:

# 1: review scores overall average
review_score_avg = dfs['olist_order_reviews_dataset']['review_score'].mean()

