from pipeline.running import ingestion, act_processes
from act_processes import a1proc, a2proc, a3proc
import pandas as pd

dfs = ingestion.ingest()

acts = {}

acts["ACT1"] = a1proc.calculate(dfs)
acts["ACT2"] = a2proc.calculate(dfs)
acts["ACT3"] = a3proc.calculate(dfs)
# acts["ACT2"] = a2proc.calculate(dfs)
# acts["ACT3"] = a3proc.calculate(dfs)