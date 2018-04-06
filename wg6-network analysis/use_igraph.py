import os
from scipy import stats as st
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

igraph.plot(graph)
print("Network diameter is {}".format(graph.diameter()))
print("Network average closeness is {}".format(np.mean(graph.closeness())))
print("Network average network betweenness "
      "is {}".format(np.mean(graph.betweenness())))
print("Network density is {}".format(graph.density()))
print("Network average degree is {}".format(np.mean(graph.degree(mode=1))))
print("Network reciprocity is {}".format(graph.reciprocity()))
print("Network average transitivity "
      "is {}".format(graph.transitivity_avglocal_undirected()))
print("Network eccentricity is {}".format(np.mean(graph.eccentricity())))
avg_shortest = []
for v in graph.vs:
	avg_shortest.append(np.mean([len(i) for i in
	                             graph.get_all_shortest_paths(v)]))
print("Network average distance between nodes "
      "is {}".format(np.mean(avg_shortest)))

#find hubsize
hubsize = graph.hub_score()
graph.vs["size"] = [int(h*50) for h in hubsize]
igraph.plot(graph, layout="large")
authority = graph.authority_score()
graph.vs["size"] = [int(h*50) for h in authority]
igraph.plot(graph, layout="large")
diameter_path = graph.get_diameter()
graph.vs["size"] = [10 for h in authority]
diameter_edges = []
for id, v in enumerate(diameter_path):
	graph.vs[v]["size"] = 20
	graph.vs[v]["color"] = "red"
	if id+1<len(diameter_path):
		edge = graph.get_eid(v, diameter_path[id+1])
		graph.es[edge]["width"] = 4
		graph.es[edge]["color"] = "red"
igraph.plot(graph, layout="large")
uGraph = graph.as_undirected()
uGraph.vs["name"] = list(string.ascii_uppercase)[:data.shape[0]]
largest_cliques = uGraph.largest_cliques()
largest_clique_name = [uGraph.vs["name"][i] for i in list(largest_cliques[0])]
print("The largest cliques in the undirected network "
      "contains {}".format(largest_clique_name))
print("The network contains {} maximal "
      "cliques".format(len(uGraph.maximal_cliques())))
print("The cohesion of the network is {}".format(uGraph.cohesion()))
clustering = uGraph.community_edge_betweenness().as_clustering()
print("the clustering of this network based on edge betweennes is as follows:")
print(clustering)
print("The components are a {}".format(uGraph.components()))
print("The loop edges are {}".format([uGraph.es[i]["name"] for i in
                                      range(len(uGraph.is_loop()))
                                      if uGraph.is_loop()[i] is True]))
triangles = uGraph.cliques(min=3, max=3)
print("There are {} triangles in the graph".format(len(triangles)))
contains_s = [s for s in triangles if uGraph.vs["name"].index("S") in s]
print("{} of them contain vertex S".format(len(contains_s)))
glo_clu = uGraph.transitivity_undirected()
print("the global clustering connection of this network is {}".format(glo_clu))
ave_clu = []
for _ in range(10):
	shuffled_data = data[:]
	np.random.shuffle(shuffled_data)
	for row in shuffled_data:
		np.random.shuffle(row)
		row = list(row)
	list_data = []
	for rid, row in enumerate(shuffled_data):
		list_row = []
		for iid, i in enumerate(row):
			if rid==iid:
				list_row.append(0)
			else:
				list_row.append(int(i))
		list_data.append(list_row)
	rand_graph = Graph.Adjacency(list_data, mode="MAX")
	ave_clu.append(rand_graph.transitivity_undirected())
p_value =st.ttest_1samp(ave_clu, glo_clu)[1]
if p_value < 0.05:
	print("The clustering is statistically significantly different from random"
	      " clustering with a p-value of {}".format(p_value))
else:
	print("The clustering is statistically not significantly different from "
	      "random clustering with a p-value of {}".format(p_value))

rewiring_probability = np.logspace(-3., -1., 10)
closeness_centrality = np.zeros_like(rewiring_probability)
g = igraph.Graph.Lattice([1,50], nei=8, directed=False,
	mutual=True, circular=True)
E = g.ecount()

for ii, p in enumerate(rewiring_probability):
	h = g.copy() # creates a deepcopy
	n = int(p * E)
	h.rewire(n=n, mode="simple")
	closeness_centrality[ii] = np.mean(h.closeness())

igraph.plot(h, layout="circle")