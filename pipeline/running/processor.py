from pipeline.running import ingestion
from resources.acts import a1, a2, a3, a4

dfs = ingestion.ingest()

acts = {}

acts["ACT1"] = a1.proc.calculate(dfs)
acts["ACT2"] = a2.proc.calculate(dfs)
acts["ACT3"] = a3.proc.calculate(dfs)
acts["ACT4"] = a4.proc.calculate(dfs)
# acts["ACT3"] = a3proc.calculate(dfs)