import plotly.graph_objects as go
import plotly.express as px
import pandas as pd


class Act4:
    def __init__(self, simpledb):
        self.simpledb = simpledb
        self.models = sorted(pd.DataFrame(self.simpledb.get_table("TEST_ACT4", "evaluation_metrics"))['model_name'].unique().tolist())

        self.update()

    def update(self, model_name=None):
        self.model = model_name or self.models[0]

        self.actual_predicted = self.simpledb.get_filtered_table("TEST_ACT4", "actual_predicted", "model_name", "actual_values") + self.simpledb.get_filtered_table("TEST_ACT4", "actual_predicted", "model_name", self.model)
        self.important_features = self.simpledb.get_filtered_table("TEST_ACT4", "important_features", "model_name", self.model)
        self.model_eval = self.simpledb.get_filtered_table("TEST_ACT4", "evaluation_metrics", "model_name", self.model)

    def get_model(self):
        return self.model

    def get_models(self):
        return self.models

    def get_actual_predicted(self):
        df = pd.DataFrame(self.actual_predicted)
        # Keep only actual vs predicted model
        # Melt bins into long format
        plot_df = df.melt(
            id_vars=['model_name'],
            value_vars=['1', '2', '3', '4', '5'],  # the bin columns
            var_name='Review Score',  # new column for bins
            value_name='Count'  # new column for counts
        )
        fig = px.line(plot_df, x='Review Score', y='Count', color='model_name', line_shape='linear', markers=True)
        fig.update_layout(title="Model Accuracy: Actual Vs Predicted")
        return fig

    def get_10_important_features(self):
        df = pd.DataFrame(self.important_features.copy())
        df = df.sort_values(by="abs_importance", ascending=False)
        df = df.rename(columns={"importance": "Feature Importance", "feature" : "Feature"})
        fig = px.bar(df, x="Feature Importance", y="Feature", barmode='relative', orientation="h", title="The 10 Most Predictive Features By This Model")
        fig.update_layout(yaxis=dict(autorange="reversed"))
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