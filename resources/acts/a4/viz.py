import plotly.graph_objects as go
import plotly.express as px
import pandas as pd


class Act4:
    def __init__(self, simpledb):
        self.simpledb = simpledb
        self.models = sorted(pd.DataFrame(self.simpledb.get_table("TEST_ACT4", "evaluation_metrics"))['model_name'].unique().tolist())

        self.update()

    def update(self, category=None):
        self.model = category or self.models[0]

        #self.actual_predicted = self.simpledb.get_filtered_table("TEST_ACT4", "10_important_features", "model_name", "actual_values") + self.simpledb.get_filtered_table("TEST_ACT4", "10_important_features", "model_name", self.model)
        self.important_features = self.simpledb.get_filtered_table("TEST_ACT4", "10_important_features", "model_name", self.model)
        self.model_eval = self.simpledb.get_filtered_table("TEST_ACT4", "evaluation_metrics", "model_name", self.model)

    def get_models(self):
        return self.models

    def actual_predicted(self):
        df = pd.DataFrame(self.actual_predicted)
        actual_values = df[df['model_name'] == 'actual_values']
        predicted_values = df[df['model_name'] == self.model]
        fig = px.line()
        return fig

    def get_10_important_features(self):
        fig = px.bar(self.important_features, x="importance", y="feature", barmode='relative', orientation="v")
        return fig

    def get_model_evals(self):
        df = pd.DataFrame(self.model_eval.copy())
        df = df.drop(columns=['model_name'], errors='ignore')

        row_data = df.to_dict(orient='records')

        column_defs = [
            {"field": col, "headerName": col.replace("_", " ")}
            for col in df.columns
        ]

        return row_data, column_defs