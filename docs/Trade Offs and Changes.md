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

<img width="1176" height="411" alt="image" src="https://github.com/user-attachments/assets/37305b09-039e-49a9-90d0-72a5872dc7a0" />

### Pipeline Design
When it came to my pipeline, I had two things to consider, how data was going to be processed and when it would be processed.

#### Pipeline Runner Execution (The How)
To process my data, I had thought of it three parts:
- Ingestion: The subprocess of getting the data from the sources
- Analysis: The subprocess of cleaning, and manipulating the data into actual metrics
- Storage: The subprocess of storing metrics in the cloud

I ended up designing these parts into modules so that they would integrate into my runner rather than be all on the same conceptual 'level'.

##### Ingestion
For ingestion, I had to make sure that I grabbed all of the neccesary data to send to my analysis module. So I used kagglehub to source the data, and then I combined the files all into a list of dataframes. This makes it easier for my analysis module to focus on cleaning and processing directly.

##### Analysis
For analysis, I had to make sure that I cleaned the data, obtained metrics from it and organized it into a simple data structure that could be sent to my storage module. Since there was a lot of data, I focused on cleaning on a 'needs to do' basis rather than a full clean. 

In terms of the actual analysis, that can be seen in the 'ACT Analysis' segment below. Other than that, the only thing left I had to cover was organizing the data so it could be sent to storage. I thought of it in 3 segments:

Acts - the data structure that holds a list of acts
Act - A given set of metrics/kpis
Metrics - The recently analyzed data needed for the visualization of a given metric

I opted for Acts and Act types to be dictionaries. This is because of the O(1) access and there wasn't much need for index based traversal. The metrics I chose to have as list of records where each record was a dictionary. This was done so creating tables for metric data would be simple since I could rely on index based traversal. In terms of the records being dictionaries, this was also fine because they were lightweight and relied on the same columns so abstracting how I can reference that information would become easier for storage.

##### Storage



An interesting note from this is at runtime, there would be a recursive aspect to executing the process.

For the most part the process stays as follows: Ingestion -> Analysis -> Storage.

However it became more like this: Storage -> Analysis -> Ingestion -> Analysis -> Storage

This was due to how importing works. When you import python will run the module you imported before running the rest of the current program. So it would go into storage, then into analysis (on import) than into ingestion (on import) and recursively return back to storage with all the necessary metrics.

#### Pipeline Operations (The When)
To make sure my pipeline would only process data when necessary I thought it was important to decide when to monitor or run. Originally, I thought about this in the form of two seperate classes monitor and runner. However, as I continued to map out my design, I realized some problems with having discrete classes for them. The monitor checks that I was doing clashed with the error handling (transaction management, etc) I had already thought of implementing in the storage module. So I ended up not creating a definitive monitor class and adopted a more conservative philosophy when it came to data storage.

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

### 

## ACT Analysis

### ACT 1
#### Calculating Annual Revenue
Since there was no direct column for revenue, I had to calculate it by cross-referencing my orders ('olist_orders_dataset.csv) with my transactions ('olist_order_payments_dataset.csv), aggregating them to get an approximate result. 

In order to do this though, I would need to preprocess my order timestamps, converting them from string to DateTime. However, this posed a new challenge, which order timestamp should I use for my analysis? Initially, I was planning on using order_purchase_timestamp, but since multiple transactions exist for a given order (paying in installments), I wasn't sure using it would give me an accurate result. Also, transaction records have no timetamp directly associated, so I can't traverse them to find the last transaction date for approximation.

In the end, my best option was to use the order_delivered_customer_date since that was the date has most likely chance of everything being resolved.



