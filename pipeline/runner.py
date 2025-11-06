from running import processor


class Runner:
    def __init__(self, db):
        self.db = db

    def start(self):
        try:
            self.db.write_to_table("TEST_ACT1","metrics",processor.acts["ACT1"]["metrics"])
        except Exception as e:
            print(e)