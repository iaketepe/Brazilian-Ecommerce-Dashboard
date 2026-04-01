from pipeline.running import storage
from pipeline.utils import gittool
from datetime import datetime, timezone
from dotenv import load_dotenv
import os

load_dotenv()

class Runner:
    def __init__(self, db):
        self.db = db
        self.mode = os.getenv("MODE")

    def assign_base(self):
        if self.mode == "main":
            return "BED"
        return "TEST"

    def start(self):
        dt = datetime.now(timezone.utc)
        error_message = "N/A"
        try:
            with self.db._conn.transaction():
                schema_base = self.assign_base()
                act_names = ['ACT1','ACT2','ACT3','ACT4']
                for act_name in act_names:
                    storage.store(self.db, schema_base, act_name)
            status = "SUCCESS"
        except Exception as e:
            status = "FAILURE"
            error_message = str(e)

        run_date = dt.date()
        run_time = datetime.now(timezone.utc) - dt

        pipeline_run = [{
            "status": status,
            "code_version" : gittool.get_git_version(),
            "run_date": run_date,
            "time_elapsed": run_time,
            "error_message" : error_message
        }]

        metadata_schema_name = schema_base + "_" + "METADATA"

        with self.db._conn.transaction():
            self.db.create_schema(metadata_schema_name)
            self.db.create_pipeline_runs_table(metadata_schema_name)
            self.db.write_to_table(metadata_schema_name,"pipeline_runs", pipeline_run)