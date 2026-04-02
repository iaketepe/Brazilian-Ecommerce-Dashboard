from prefect import flow, task
from pipeline import runner
from pipeline.db import DB
import sys

@task
def setup_db():
    db = DB()

    if not(db.is_connected()):
        print("!DB -> Ending Prog...")
        sys.exit(1)
    return db

@task
def execute_runner(db):
    try:
        r = runner.Runner(db)
        r.start()
    except Exception as e:
        print(e)
        sys.exit(1)

@flow
def main():
    db = setup_db()
    execute_runner(db)

if __name__ == "__main__":
    main()

#if not(db.select_exists_schema("TEST_ACT1") and db.select_exists_schema("TEST_ACT2")):
    #print("Db exists but incomplete data")

#else:
    #print("DB exists")
