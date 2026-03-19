import plotly.graph_objects as go
import plotly.express as px
import pandas as pd



class Act3:
    def __init__(self, actData):
        # Promote each table to an attribute
        for table_name, table in actData.items():
            setattr(self, table_name, table)

    def __getitem__(self, table_name):
        return getattr(self, table_name)

