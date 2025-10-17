import kagglehub
import os
import pandas as pd

# Download latest version

def ingest():
    path = kagglehub.dataset_download("olistbr/brazilian-ecommerce")

    print("Path to dataset files:", path)

    print("Files:", os.listdir(path))

    # Dictionary to store DataFrames
    dfs = {}

    # Load each CSV into a DataFrame
    for filename in os.listdir(path):
        file = os.path.join(path, filename)
        df_name = filename.replace('.csv', '')  # e.g., olist_customers_dataset
        dfs[df_name] = pd.read_csv(file)
    return dfs


_ = """
import math

def stars_text(rating, max_stars=5):
    full_stars = int(rating)
    half_star = 1 if rating - full_stars >= 0.5 else 0
    empty_stars = max_stars - full_stars - half_star
    return "★" * full_stars + "☆" * empty_stars

avg_stars = stars_text(review_score_avg)
print(avg_stars)  # e.g., "★★★★☆"

"""