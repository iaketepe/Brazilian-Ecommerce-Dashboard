## ACT 4
import pandas as pd
import numpy as np
import shap
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from tensorflow import keras
from tensorflow.keras import layers

def initializing_dataset(dfs):
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

def convert_timestamp(column):
  return pd.to_datetime(column, errors='coerce')

def setting_up_calculations(dfs):
    ml_data = initializing_dataset(dfs)

    ml_data['order_purchase_timestamp'] = convert_timestamp(ml_data['order_purchase_timestamp'])
    ml_data['order_delivered_customer_date'] = convert_timestamp(ml_data['order_delivered_customer_date'])
    ml_data['order_estimated_delivery_date'] = convert_timestamp(ml_data['order_estimated_delivery_date'])

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
            'product_category',
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

    return X, y

def splitting_the_data(dfs):
    X, y = setting_up_calculations(dfs)

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    X_train = X_train.astype('float32')
    X_test = X_test.astype('float32')

    y_train = y_train.astype('float32')
    y_test = y_test.astype('float32')

    return X_train, X_test, y_train, y_test

def running_LR(X_train, X_test, y_train, y_test):
    model = LinearRegression()

    model.fit(X_train, y_train)

    #preds = model.predict(X_test)

    #print("MSE:", mean_squared_error(y_test, preds))
    #print("MAE:", mean_absolute_error(y_test, preds))
    return model

def running_NN(X_train, X_test, y_train, y_test):
    model = keras.Sequential([
        layers.Dense(64, activation='relu', input_shape=[X_train.shape[1]]),
        layers.Dense(32, activation='relu'),
        layers.Dense(1)
    ])

    model.compile(
        optimizer='adam',
        loss='mse',
        metrics=['mae']
    )

    history = model.fit(
        X_train.values,
        y_train.values,
        validation_split=0.2,
        epochs=50,
        verbose=1
    )

    #model.evaluate(X_test.values, y_test.values)

    return model, history

def evaluate_model(model_name, y_true, y_pred):

    mae = mean_absolute_error(y_true, y_pred)
    mse = mean_squared_error(y_true, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_true, y_pred)

    return {
        "model_name" : model_name,
        "MAE": mae,
        "MSE": mse,
        "RMSE": rmse,
        "R2": r2
    }

def calculate(dfs):
    X_train, X_test, y_train, y_test = splitting_the_data(dfs)

    # LR model
    linear_model = running_LR(X_train, X_test, y_train, y_test)
    y_pred_lr = linear_model.predict(X_test)

    # NN model
    model, history = running_NN(X_train, X_test, y_train, y_test)
    y_pred_nn = model.predict(X_test).flatten()

    # evaluation_metrics
    lr_metrics = evaluate_model("sklearn_linear_regression", y_test, y_pred_lr)
    nn_metrics = evaluate_model("tfkeras_seq_neural_network", y_test, y_pred_nn)

    # actual_predicted
    y_pred_rounded = np.round(y_pred_lr).astype(int)
    y_pred_nn_rounded = np.round(y_pred_nn).astype(int)

    # Define bins (1-5)
    bins = [1, 2, 3, 4, 5]

    # Count actual reviews per score
    actual_counts = pd.Series(y_test).value_counts().reindex(bins, fill_value=0).rename(lambda x: str(x)).to_dict()

    # Count predicted nn reviews per score
    pred_counts_nn = pd.Series(y_pred_nn_rounded).value_counts().reindex(bins, fill_value=0).rename(lambda x: str(x)).to_dict()

    # Count predicted lr reviews per score
    pred_counts_lr = pd.Series(y_pred_rounded).value_counts().reindex(bins, fill_value=0).rename(lambda x: str(x)).to_dict()


    # 10_important_features

    feature_importance = pd.DataFrame({
        "model_name" : "sklearn_linear_regression",
        "feature": X_train.columns,
        "importance": linear_model.coef_
    })

    feature_importance["abs_importance"] = feature_importance["importance"].abs()

    feature_importance = feature_importance.sort_values(
        by="abs_importance",
        ascending=False
    )

    top_features = feature_importance.head(10).to_dict(orient="records")

    # Use a small background dataset for reference
    X_background = X_train.sample(100, random_state=42).values

    explainer = shap.GradientExplainer(model, X_background)

    # Compute SHAP values on a small test subset
    X_eval = X_test.sample(100, random_state=42).values
    shap_values = explainer.shap_values(X_eval)

    shap_values_array = np.squeeze(shap_values)  # shape: (n_eval_samples, n_features)

    shap_importance = np.mean(shap_values_array, axis=0)

    # For single-output regression
    shap_abs_importance = np.abs(np.mean(shap_values_array, axis=0))

    importance_df = pd.DataFrame({
        "model_name": "tfkeras_seq_neural_network",
        "feature": X_test.columns,
        "importance": shap_importance,
        "abs_importance" : shap_abs_importance
    }).sort_values(by="abs_importance", ascending=False)

    top_features_nn = importance_df.head(10).to_dict(orient="records")

    return {
        "actual_predicted": [
            {"model_name" : "actual_values", **actual_counts},
            {"model_name": "sklearn_linear_regression", **pred_counts_lr},
            {"model_name": "tfkeras_seq_neural_network", **pred_counts_nn},
        ],
        "evaluation_metrics" : [lr_metrics, nn_metrics],
        "important_features" : top_features + top_features_nn
    }

