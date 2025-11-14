from pipeline import runner
from pipeline.db import DB
import sys

db = DB()

if not(db.is_connected()):
    print("!DB -> Ending Prog...")
    sys.exit(1)


if not(db.select_exists_schema("TEST_ACT1")):
    print("Db exists but no data")
    r = runner.Runner(db)
    r.start()
else:
    print("DB exists")
