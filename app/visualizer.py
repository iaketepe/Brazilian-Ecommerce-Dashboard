from app.simpleDB import SimpleDB
from resources.acts.a1 import viz as a1_viz
from resources.acts.a2 import viz as a2_viz
from resources.acts.a3 import viz as a3_viz
from resources.acts.a4 import viz as a4_viz
import plotly.io as pio

class Visualizer:
    def __init__(self): #, theme="light"):
        self.simpledb = SimpleDB()
        self.themeRefs = {
            "light" : pio.templates["plotly"],
            "dark" : pio.templates["plotly_dark"],
        }
        self.acts = {}

    def setup_act(self, act_name):
        if self.acts.get(act_name) is None:
            if act_name == "act_1":
                self.acts[act_name] = a1_viz.Act1(self.simpledb)
            elif act_name == "act_2":
                self.acts[act_name] = a2_viz.Act2(self.simpledb)
            elif act_name == "act_3":
                self.acts[act_name] = a3_viz.Act3(self.simpledb)
            elif act_name == "act_4":
                self.acts[act_name] = a4_viz.Act4(self.simpledb)
            else:
                self.acts[act_name] = a1_viz.Act1(self.simpledb)

    def get_Acts(self):
        return self.acts

    def get_theme(self, theme):
        if theme in self.themeRefs.keys():
            return self.themeRefs[theme]
        return self.themeRefs["light"]


visualizer = Visualizer()