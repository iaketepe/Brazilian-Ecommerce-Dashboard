from dash import Dash, html, dcc, Output, Input, State
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from app.simpleDB import SimpleDB
from resources.acts import a1, a2, a3

class Visualizer:
    def __init__(self): #, theme="light"):
        #self.theme = theme
        self.simpledb = SimpleDB()

        gd = pd.DataFrame(self.simpledb.get_table("BED_ACT2","geo_distributions"))
        gd['review_score'] = gd['review_score'].astype(float)


        self.acts = {"act_1" : a1.viz.Act1(self.simpledb),
        "act_2": a2.viz.Act2({"geo_distributions": gd}),
        }

    def get_Acts(self):
        return self.acts


visualizer = Visualizer()