import os

os.environ["path"] += ";C:\whut\cairo-windows-1.15.10\lib\x64"
import igraph
# from igraph import Graph
# import numpy as np
# import string
# import cffi
# cffi.FFI().dlopen('C:\whut\cairo-windows-1.15.10\lib\\x64\cairo.dll')
#
# # Load data and create graph
# data = np.genfromtxt('./sociogram-employees-un.csv', delimiter=',',dtype=None)
# graph = Graph.Adjacency(list(data), mode=igraph.ADJ_DIRECTED)
# graph.vs["name"] = list(string.ascii_uppercase)[:data.shape[0]]
# graph.vs["color"] = "yellow"
# graph.vs["shape"] = "sphere"
# print(graph)
# igraph.plot(graph)
name = 'cairo.dll'
# print(os.path.isfile(b'C:\whut\lib\cairo.def'))
for directory in os.environ['PATH'].split(os.pathsep):
	print(directory)
	fname = os.path.join(directory, name)
	print(fname)
	if os.path.isfile(fname):
		print(True)
	if fname.lower().endswith(".dll"):
		continue
	fname = fname + ".dll"
	if os.path.isfile(fname):
		print(True)
print(None)
