# Trade Offs and Changes

## Designing Project Structure
### One Stage vs Two Stage Application
- When I was planning my dashboard site, I needed to figure out the architecture so I could move forward. I had two ideas:
  - Monolithic application
  - Services-based application (I seperate the application into an 'app' and a pipeline, deploying both seperately and connecting them)
    #### Option A: App indirectly connects to the pipeline
      - Pipeline ingests data from Kaggle
      - Pipeline computes analysis (preprocessing, etc)
      - Pipeline sends analysis to DB
      - 'App' connects to DB, rendering data
    #### Option B: App directly connects to the pipeline
      - Pipeline ingests data from Kaggle
      - Pipeline computes analysis (preprocessing, etc)
      - Pipeline sends analysis to DB
      - 'App' requests DB info from Pipeline service, rendering data

Result: I chose designing a service-based application based on option A. After doing some research, I realized that option A was better because it increases the amount of abstraction between layers. This abstraction is, I believe makes option A closer to real world workflows.


## Stage Design

### Pipeline Design


### App Design
Finally, I've started to design my dashboard as a web app. I had two options:
  - Streamlit
    - Simple to use
    - Very limited (Difficult to interact with html directly)
  - Dash
    - More Complicated
    - Customizable

Choosing between using Streamlit and Dash was one of toughest choices I had to make for this project. In fact, I was originally planning on using streamlit since my architecture design makes my web app need to render my analysis instead of processing it. 

So there wasn't much difference between the two. However, as I was developing, I realized that streamlit's more limited web design tools actually made it difficult to design. So I decided switching to Dash would be better long term.


### Designing in Plotly Dash
Something I've realized is the subtle difference between using Plotly Dash vs HTML/CSS. For the most part its similar, you still write with CSS rules and HTML elements with Python as an intermediary. However, since Dash has its own ways of handling web design, I had to take a step back from designing and focus on understanding Dash. Methods I would have quickly applied like page wrapping (for min-width clamps), or patterns for absolute-relative elements wouldn't work as easily as they did.
 

## ACT Analysis
For my dashboard, I wanted to make my metrics make sense. So at each stage I asked a question to help improve focus across the acts.

Here are the questions:
- How are we doing?
- Why are things as they are?


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

