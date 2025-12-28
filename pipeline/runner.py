from pipeline.running import storage
from pipeline.utils import gittool
from datetime import datetime, timezone


class Runner:
    def __init__(self, db):
        self.db = db

    def start(self):
        dt = datetime.now(timezone.utc)
        error_message = "N/A"
        try:
            with self.db._conn.transaction():
                schema_base = "TEST"
                act_names = ['ACT1']
                print("before storage module")
                for act_name in act_names:
                    storage.store(self.db, schema_base, act_name)
            status = "SUCCESS"
        except Exception as e:
            print(e)
            status = "FAILURE"
            error_message = str(e)

        run_date = dt.date()
        run_time = datetime.now(timezone.utc) - dt

        pipeline_run = [{
            "status": status,
            "code_version" : gittool.get_git_version(),
            "date": run_date,
            "time_elapsed": run_time,
            "error_message" : error_message
        }]

        metadata_schema_name = schema_base + "_" + "METADATA"
        self.db.create_schema(metadata_schema_name)
        self.db.create_pipeline_runs_table(metadata_schema_name)
        self.db.write_to_table(metadata_schema_name,"pipeline_runs", pipeline_run)