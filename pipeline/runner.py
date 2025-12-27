from pipeline.running import storage
# from pipeline.running import processor


class Runner:
    def __init__(self, db):
        self.db = db

    def start(self):
        try:
            # storage.store(TEST,ACT1)->ACT2->ACT3
            storage.store(self.db, "TEST", "ACT1")
        except Exception as e:
            print(e)