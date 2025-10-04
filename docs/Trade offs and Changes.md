# Trade Offs and Changes

## Designing Project Structure
### One Stage vs Two Stage Application
When I was planning my dashboard site, I needed to figure out the architecture so I could move forward. I had two ideas:
  Monolithic application (All of my data analysis, visualization and hosting are apart of one application deployed to the cloud)
  Services-based application (I seperate the application into an 'app' and a pipeline, deploying both seperately and connecting them)
    Option A: App indirectly connects to the pipeline
      - Pipeline ingests data from Kaggle
      - Pipeline computes analysis (preprocessing, etc)
      - Pipeline sends analysis to DB
      - 'App' connects to DB, rendering data
    Option B: App directly connects to the pipeline
      - Pipeline ingests data from Kaggle
      - Pipeline computes analysis (preprocessing, etc)
      - Pipeline sends analysis to DB
      - 'App' requests DB info from Pipeline service, rendering data
Since the project was simple, it could have been done as a monolithic project. However I believed it would be better to have services-based application option B,
since that mimics real world workflows.


## Choosing Technologies

## Streamlit vs Dash

Choosing between using Streamlit and Dash was one of toughest choices I had to make for this project. 
