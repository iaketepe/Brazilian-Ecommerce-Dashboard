from pipeline.running import ingestion
from resources.acts.a1 import proc as a1_proc
from resources.acts.a2 import proc as a2_proc
from resources.acts.a3 import proc as a3_proc
from resources.acts.a4 import proc as a4_proc

def setup_act(act_name):
    dfs = ingestion.ingest()

    actsRef = {
        "ACT1" : a1_proc,
        "ACT2" : a2_proc,
        "ACT3" : a3_proc,
        "ACT4" : a4_proc,
    }

    return actsRef[act_name].calculate(dfs)

def setup_acts():
    dfs = ingestion.ingest()

    acts = {}

    acts["ACT1"] = a1_proc.calculate(dfs)
    acts["ACT2"] = a2_proc.calculate(dfs)
    acts["ACT3"] = a3_proc.calculate(dfs)
    acts["ACT4"] = a4_proc.calculate(dfs)
    # acts["ACT3"] = a3proc.calculate(dfs)

    return acts