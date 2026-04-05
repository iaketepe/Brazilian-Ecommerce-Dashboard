from pipeline import runner
from pipeline.db import DB

def main():
    db = DB()
    r = runner.Runner(db)
    r.start()

main()
