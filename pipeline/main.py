from pipeline import runner
from pipeline.db import DB
import sys

db = DB()

if not(db.is_connected()):
    print("!DB -> Ending Prog...")
    sys.exit(1)


if not(db.select_exists_schema("TEST_ACT1") and db.select_exists_schema("TEST_ACT2")):
    print("Db exists but incomplete data")
    r = runner.Runner(db)
    r.start()
else:
    print("DB exists")
