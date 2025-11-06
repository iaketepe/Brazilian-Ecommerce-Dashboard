import runner
from db import DB
import sys

db = DB()

if not(db.is_connected()):
    print("!DB -> Ending Prog...")
    sys.exit(1)


if not(db.select_exists("TEST_ACT1","metrics")):
    #runner = Runner(db)
    #runner.run()
    print("Db exists but no data")
else:
    print("DB exists")
    r = runner.Runner(db)
    r.start()
