from dash import Dash, html, dcc, Output, Input, State
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from app.simpleDB import SimpleDB
from resources.acts import a1, a2

class TableWrapper:
    def __init__(self, tableData):
        self.tableData = tableData
        self._lookup = {rec['name']: rec['value'] for rec in tableData}

    def __getattr__(self, name):
        return self._lookup.get(name)

    def __getitem__(self, name):
        return self._lookup.get(name)

class Visualizer:
    def __init__(self): #, theme="light"):
        #self.theme = theme
        self.simpledb = SimpleDB()

        order_status_data = self.simpledb.get_table("BED_ACT1","order_status")
        gd = pd.DataFrame(self.simpledb.get_table("BED_ACT2","geo_distributions"))
        gd['review_score'] = gd['review_score'].astype(float)


        self.acts = {"act_1" : a1.viz.Act1({
            "metrics" : TableWrapper(self.simpledb.get_table("BED_ACT1","metrics")),
            "order_status" : pd.Series(order_status_data[0]),
            "cumulative_revenue" : self.simpledb.get_table("BED_ACT1","cumulative_revenue"),
        }),
        #"act_2" : Act2({"geo_distributions" : self.simpledb.get_table("BED_ACT2","geo_distributions")})}
        "act_2": a2.viz.Act2({"geo_distributions": gd})}

    def get_Acts(self):
        return self.acts


visualizer = Visualizer()