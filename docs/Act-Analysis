
## ACT Analysis
For my dashboard, I wanted to make my metrics make sense. So at each stage I asked a question to help improve focus across the acts.

Here are the questions:
- How are we doing?
- Why are things as they are?
- How well can we predict the future?


### ACT 1
The focus of this act is to showcase the good and the bad. Since this is for a e-commerce platform, it makes sense alot of that will be seen through either finance related metrics or order/delivery transactions. So after exploring my data, I grounded my ideas through the following metrics:

- Annual Revenue Projections
- Customer Satifaction (through average review scores)
- Order Policy KPIs
- Order Status

#### Calculating Annual Revenue
Since there was no direct column for revenue, I had to calculate it by cross-referencing my orders ('olist_orders_dataset.csv) with my transactions ('olist_order_payments_dataset.csv), aggregating them to get an approximate result. 

In order to do this though, I would need to preprocess my order timestamps, converting them from string to DateTime. However, this posed a new challenge, which order timestamp should I use for my analysis? Initially, I was planning on using order_purchase_timestamp, but since multiple transactions exist for a given order (paying in installments), I wasn't sure using it would give me an accurate result. Also, transaction records have no timetamp directly associated, so I can't traverse them to find the last transaction date for approximation.

In the end, my best option was to use the order_delivered_customer_date since that was the date has most likely chance of everything being resolved.

#### Calculating Revenue Over Time
After calculating the annual revenue, I believed it was important to showcase the growth of revenue projections over time. So I copied my df_delievered_revenue dataframe, converted the timestamp data into objects so I could group the records by their respective month. Afterwards, I used the .cumsum() to get a set the a growing sum over time. This also optimizes storage usage because I'm binning the datapoints to each month instead of adding every single datapoint directly.

#### Average Customer Review Score
The Average review score showcases the review score people usually give us after a delivered order. I calculated it by take the mean of the review sores for each order.

#### Order Policy KPIs
The point of these KPIs was to have indicators that would apply to the real world orders. Situations that tie back to how well supply chains meet delivery expectations, how well certain payment features are being upheld, etc.

For this I had three metrics:
- Orders paid in full with installments
  - Measures the fraction of delivered orders that were fully paid, even if the customer used installments.
  - Calculated by merging delivered revenue data with item prices and counting orders where payment_value >= price.
  - Provides insight into financial reliability for the platform.
- Orders shipped from Seller to Carrier before deadline
  - Measures how reliably sellers hand off orders to carriers on or before the shipping limit date.
  - Calculated by merging delivered orders with seller shipping limits and counting orders where order_delivered_carrier_date ≤ shipping_limit_date.
  - Indicates seller compliance and efficiency in the fulfillment process.
- Orders delivered from Carrier to Customer before deadline
  - Measures the timeliness of deliveries to customers.
  - Calculated by comparing order_delivered_customer_date with order_estimated_delivery_date and counting on-time deliveries.
  - Reflects customer experience and the platform’s ability to meet delivery promises.


### ACT 2
The focus of this act is to elaborate on Act 1 and bring more context. After realizing the sellers, customers and order could be traced back to their geography, I realized I could showcase this context through geodata. 

This is why I focused on the following metrics:
- Seller Distribution
- Customer Distribution
- Average Review Score (By State)

These three allow for a better look of how we're performing across the nation.

#### Seller Distribution
By seeing the distribution of our sellers, we could understand more on our sellers. If most of our sellers are located in a similar location, then it allows us to do research later on why that's the case. It can also reduce scope for logistical issues since most of them would likely use similar 'routes' for delivery. Another factor is what I like to call a 'seller desert'. There may be locations where we have very little or no sellers. If that is the case, then we can ask questions on how to reach out or why we have no sellers in that location.

To calculate this, I started out by grouping the sellers by their state, counting their respective numbers. Next, I merged the counts with a reference table mapping state names to their state 'codes'. This reference table would also account for the outcome of states without sellers. Finally, I converted the seller counts to integers to make the data clear.

#### Customer Distribution
The reasoning for this metric is similar to the previous one. We can understand more about our customers, even think about where most of customers are, where most aren't take action based on that information.  The approach was similar to the seller distribution as well.

#### Average Review Score (By State)
It's easy to look at an e-commerce platform as just one thing. Sometimes, though its better to look at it as a group of state-wide selling systems. Each system adheres to the platform's values flexibly, with their own logistics, sellers, etc. So, if we focus on the average review scores for the sellers in those states, it may give us a view into how well each 'system' is doing.

To analyze average review scores by state, I first merged order review scores with their corresponding orders and linked each order to its seller and the seller’s state. For orders with multiple sellers, I aggregated to select a single seller and state per order. I then calculated the average review score for each seller state, ensuring that all states were included by merging with a reference table and filling missing values with 0. Finally, I combined this with the seller and customer geographic distributions to create a state-level dataset containing seller counts, customer counts, and average review scores, ready for visualization on the dashboard.

### ACT 3
The question, "Why are things as they are" is much deeper than I thought. In Act 2, I tried to approach this from a external, geographical context. However, I never ended up looking at it from a more internal one. This act is more focused on that. By analyzing data through the lense of  product categories, I can understand the 'Why' on a deeper level.

#### Number of Orders
To understand demand across the platform, I calculated the number of orders per product category. This was done by grouping the dataset by product_category and counting the number of associated order_id values. This metric serves as a baseline indicator of category performance, highlighting which categories drive the most activity on the platform. It also provides useful context when compared with revenue-based metrics from Act 1, helping differentiate between high-volume and high-value categories.

#### Platform Order Share
While raw order counts are useful, it's difficult to understand the impact a given category has immediately. To address this, I calculated a proportion for each category. This was done by dividing the number of orders in each category by the total number of orders across the platform. It provides a clearer understanding of category dominance and platform concentration.

#### Best and Worst 3 Sellers
To evaluate seller performance more accurately, I implemented a Bayesian-adjusted scoring system rather than relying on simple averages. First, I grouped the data by both product_category and seller_id, calculating the number of reviews and the average review score for each seller. I then computed a global average review score across the entire dataset and introduced a category-specific weighting factor to account for differences in review volume.

Using these components, I calculated a Bayesian score that balances each seller’s individual performance with the overall platform average. This approach reduces the impact of low-sample-size bias and produces more stable rankings. Based on this score, I identified the top 3 and worst 3 sellers within each category. This provides insight into both high-performing sellers who drive positive customer experiences and underperforming sellers who may introduce risk to the platform.

#### Distribution of Product Review Scores
To better understand customer sentiment, I analyzed the distribution of review scores within each product category. For each category, I counted the number of reviews corresponding to each score from 1 to 5. This reveals the full shape of a categories customer feedback. By examining these distributions, it becomes possible to identify whether a category meeting satisfaction expectations.

#### Distribution of Seller Average Product Review Scores
In addition to analyzing individual reviews, I examined the distribution of average review scores at the seller level within each category. I first calculated the mean review score for each seller, then grouped these averages into discrete bins between 1 to 5. This provides insight into how seller performance is distributed across a platform's category.

This metric helps determine whether strong performance is widespread or concentrated among a small number of sellers. When cross-referenced with the previous distribution, it becomes a powerful tool for observing blindspots in platform market trends. For example, if a category had very low levels of customer satisfaction. However, most sellers provided high levels of satisfaction, then it may allow us to think about questioning our recommendations systems or other policies.

NOTE: When it came to visualizing this metric. Dash had a bit of trouble displaying data at the ends of the range (1, 5). So I had to expand the range to make the entire result visible.

### ACT 4
The question for this act was how well can we predict the future? Since this is for an ecommerce platform, it makes sense to see that as, "How aligned are we with customer expectations?" To keep things straightforward, I focused on using machine learning to predict order review scores based on certain features:

Some of the features include:

Order Item Features
- Photo Quantity
- Price
- Product Category

Item Logistical Features
- Delivery Distance (Through differences in customer and seller locations)
- Delivery Time (From Order Purchase To Delivery)

To improve model prediction, I designed features that map on to a sort of 'delivery policy'. 

These features focused on:
- Early Deliveries
- Late Deliveries

They were designed using an exponential function, quickly scaling to signal more extreme cases. 

I also made different models to assess prediction changes through different algorithms:
- Linear Regression
- Keras Sequential Neural Network

#### Model Accuracy: Actual Vs Predicted
I used a line chart to display compare how well a given model predicted the number of cases for a set of review scores.


#### The 10 Most Predictive Features By This Model
I believed, it was important to understand which features impacted a models decisions. For that reason I created a bar chart that shows the 10 features a model weighted the most. I allowed feature importance to be negative or positive. This shows not only shows how important the feature was the model. It shows how the model interpreted that feature. For example, if a feature had a positive value it means that the higher the value observed the more likely the model would rate the score positively. The opposite is true with the negative.  

#### Evaluation Metrics
I had each model go through a set of evaluation metric assessments, to understand how well it was performing functionally.

I used the following metrics:
- MAE (Mean Absolute Error)
- MSE (Mean Squared Error)
- RMSE (Root Mean Squared Error)
- R² (Coefficient of Determination)
