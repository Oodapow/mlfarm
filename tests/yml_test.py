import mlfarm.core
import os
import yaml
from graphviz import Graph

cfg = os.path.join(__file__, '..', 'config.yml')
with open(cfg, 'r') as f:
    cfg = yaml.safe_load(f)

def test():
    print(cfg)

    pv = mlfarm.core.PrintTableVisitor()
    print(pv.visit(cfg))

    
    g = Graph('G', filename='a.gv', engine='dot', graph_attr={'compound': 'true'})
    dv = mlfarm.core.GraphVisitor(g)
    dv.visit(cfg)
    print(g)
    g.view()

if __name__ == "__main__":
    test()