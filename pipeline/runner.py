from pipeline.running import processor


class Runner:
    def __init__(self, db):
        self.db = db

    # def createDBAct(schema_name, schema array)
        #

    def start(self):
        try:
            # storage.store(ACT1)->ACT2->ACT3
            # if there is no data create the data myself
            schema = "TEST_ACT1"
            tables = ["metrics, order_status, cumulative_revenue"]
            # create schema
            self.db.create_schema(schema)
            # create tables
            for table in tables:
                self.db.create_table(schema, table)
            # write to table
            if self.db.select_exists("TEST_ACT1","metrics"):
                self.db.write_to_table("TEST_ACT1","metrics",processor.acts["ACT1"]["metrics"])
            if self.db.select_exists("TEST_ACT1","order_status"):
                self.db.write_to_table("TEST_ACT1","order_status",processor.acts["ACT1"]["order_status"])
            if self.db.select_exists("TEST_ACT1","cumulative_revenue"):
                self.db.write_to_table("TEST_ACT1","cumulative_revenue",processor.acts["ACT1"]["cumulative_revenue"])
        except Exception as e:
            print(e)