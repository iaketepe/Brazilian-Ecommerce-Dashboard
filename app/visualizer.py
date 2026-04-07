from app.simpleDB import SimpleDB
from resources.acts.a1 import viz as a1_viz
from resources.acts.a2 import viz as a2_viz
from resources.acts.a3 import viz as a3_viz
from resources.acts.a4 import viz as a4_viz

class Visualizer:
    def __init__(self): #, theme="light"):
        #self.theme = theme
        self.simpledb = SimpleDB()

        self.acts = {
            "act_1" : a1_viz.Act1(self.simpledb),
            "act_2": a2_viz.Act2(self.simpledb),
            "act_3": a3_viz.Act3(self.simpledb),
            "act_4": a4_viz.Act4(self.simpledb),
        }

    def get_Acts(self):
        return self.acts


visualizer = Visualizer()