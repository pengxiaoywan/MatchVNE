import os
import pickle
import sys
import graph_u
from vne_u import create_vne


class Extract:
    def get_graphs(self, req_no = 5):     # USE THIS DEFINATION FOR AUTOMATION & comment line no 10
        current = os.path.dirname(os.path.realpath(__file__))
        sys.path.append(os.path.join(os.path.dirname(current), "P3_ALIB_MASTER"))
        current = os.path.join(
            os.path.dirname(current),
            "P3_ALIB_MASTER",
            "input",
            "KK_Aarnet.pickle", #senario_RedBestel  # For sample
        )
        with open(current, "rb") as f:
            data = pickle.load(f)
        para = graph_u.Parameters(500, 1000, 200, 1000, 0, 100, 0, 100, 1, 1)  #BW,CRB,Location X and y, delay 1,1 for dealy 50,100 Parameters for subsrate graph BW ,CRB, Location,Delay
        #graph_u.Parameters(500, 1000, 200, 1000, 0, 100, 0, 100, 1, 1) Original
        # For Example 20, 50, 5, 30, 0, 100, 0, 100, 1, 1
        try:
            substrate = graph_u.Graph(
                len(data.scenario_list[0].substrate.nodes),
                data.scenario_list[0].substrate.edges,
                para,
            )
        except:
            substrate = graph_u.Graph(
                data.get("substrate").nodes,
                data.get("substrate").edges,
                para,
            )
        vne_list = create_vne(no_requests = req_no)   # USE THIS STATEMENT FOR AUTOMATION & comment line no 28
        return substrate, vne_list

def for_automate(req_no = 5):
    x = Extract()
    substrate, vne_list = x.get_graphs(req_no)
    return substrate, vne_list


if __name__ == "__main__":
    for_automate(req_no=5)