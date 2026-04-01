from pipeline.running import ingestion
from resources.acts.a1 import proc as a1_proc
from resources.acts.a2 import proc as a2_proc
from resources.acts.a3 import proc as a3_proc
from resources.acts.a4 import proc as a4_proc

dfs = ingestion.ingest()

acts = {}

acts["ACT1"] = a1_proc.calculate(dfs)
acts["ACT2"] = a2_proc.calculate(dfs)
acts["ACT3"] = a3_proc.calculate(dfs)
acts["ACT4"] = a4_proc.calculate(dfs)
# acts["ACT3"] = a3proc.calculate(dfs)