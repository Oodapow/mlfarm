# fdpclust.py - http://www.graphviz.org/content/fdpclust

from graphviz import Graph

g = Graph('G', filename='a.gv', engine='fdp', graph_attr={'compound': 'true'})


with g.subgraph(name='cluster=A', graph_attr={'label':'cluster=a'}) as a:
    pass
with g.subgraph(name='cluster=B', graph_attr={'label':'cluster=b'}) as b:
    with b.subgraph(name='cluster=C', graph_attr={'label':'cluster=c'}) as c:
        pass
        with c.subgraph(name='cluster=D', graph_attr={'label':'cluster=d'}) as d:
            with d.subgraph(name='cluster=E', graph_attr={'label':'cluster=e'}) as e:
                pass
            pass
    pass


print(g)
g.view()