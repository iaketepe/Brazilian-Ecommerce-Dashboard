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

Result: I chose designing a service-based application based on option B, since I believe that would be closer to real world workflows.


## Choosing Technologies



### Web App Design
Finally, I have designing my dashboard as a web app. I had two options:
  - Streamlit
    - Simple to use
    - Very limited (Difficult to interact with html directly)
  - Dash
    - More Complicated
    - Customizable

Choosing between using Streamlit and Dash was one of toughest choices I had to make for this project. In fact, I was originally planning on using streamlit since my architecture design makes my web app need to render my analysis instead of processing it. So there wasn't much difference between the two. However, as I was developing, I realized that streamlit's more limited web design tools actually made it difficult to design. So I decided switching to Dash would be better long term.

