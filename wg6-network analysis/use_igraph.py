import os

os.environ["path"] += ";C:\whut\cairo-windows-1.15.10\lib\x64"
import igraph
from igraph import Graph
import numpy as np
import string
# Load data and create graph
data = np.genfromtxt('./sociogram-employees-un.csv', delimiter=',',dtype=None)
# print(data)
graph = Graph()
graph = Graph.Read_Adjacency('./sociogram-employees-un.csv', ',')
graph.vs["name"] = list(string.ascii_uppercase)[:data.shape[0]]
graph.vs["label"] = graph.vs["name"]
graph.vs["color"] = "yellow"
graph.vs["shape"] = "circle"

# igraph.plot(graph)
print("Network diameter is {}".format(graph.diameter()))
print("Network average closeness is {}".format(np.mean(graph.closeness())))
print("Network average network betweenness is {}".format(np.mean(graph.betweenness())))
print("Network density is {}".format(graph.density()))
print("Network average degree is {}".format(np.mean(graph.degree(mode=1))))
print("Network reciprocity is {}".format(graph.reciprocity()))
print("Network average transitivity is {}".format(graph.transitivity_avglocal_undirected()))
print("Network eccentricity is {}".format(np.mean(graph.eccentricity())))
avg_shortest = []
for v in graph.vs:
	avg_shortest.append(np.mean([len(i) for i in graph.get_all_shortest_paths(v)]))
	print(v.attribute_names())
print("Network average distance between nodes is {}".format(np.mean(avg_shortest)))

#find hubsize
hubsize = graph.hub_score()
graph.vs["size"] = [int(h*50) for h in hubsize]
# igraph.plot(graph, layout="large")
authority = graph.authority_score()
graph.vs["size"] = [int(h*50) for h in authority]
# igraph.plot(graph, layout="large")
diameter_path = graph.get_diameter()
graph.vs["size"] = [10 for h in authority]
diameter_edges = []
for id, v in enumerate(diameter_path):
	graph.vs[v]["size"] = 20
	graph.vs[v]["color"] = "red"
	if id+1<len(diameter_path):
		edge = graph.get_eid(v, diameter_path[id+1])
		graph.es[edge]["width"] = 4
igraph.plot(graph, layout="large")


