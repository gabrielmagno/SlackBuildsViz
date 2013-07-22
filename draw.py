#!/usr/bin/python
# coding=utf-8

import json
import re
import collections
import networkx as nx
import pygraphviz as pgv

colors = {"libraries":    "gold2",         
          "system":       "firebrick1",    
          "network":      "navy",          
          "development":  "forestgreen",   
          "perl":         "deeppink",      
          "games":        "darkorchid1",   
          "desktop":      "dodgerblue1",   
          "audio":        "navajowhite4",  
          "python":       "darkorange",    
          "graphics":     "lawngreen",     
          "multimedia":   "brown",         
          "academic":     "crimson",       
          "misc":         "grey37",        
          "office":       "darkorchid4",   
          "haskell":      "deeppink4",     
          "accessibility":"darkturquoise", 
          "business":     "grey10",        
          "ham":          "grey",          
          "ruby":         "darkorange3",   
        }


def graph_nx2pgv(nx_graph):
    """Convert a DiGraph from Networkx into a directed AGraph from pygraphviz"""
    pgv_graph = pgv.AGraph(directed=True)
    for node, attribute in nx_graph.node.iteritems():
        pgv_graph.add_node(node, color=attribute["color"])
    for node_a, node_b in nx_graph.edges_iter():
        pgv_graph.add_edge(node_a, node_b)
    return pgv_graph


def dependency_resolution(graph, node):
    """Create the dependency list of a given node"""
    dependency_list = []
    dependents = [node]
    while len(dependents) > 0:
        dependent = dependents.pop()
        dependency_list.append(dependent)
        dependents.extend(graph.predecessors(dependent))
    dependency_list = nx.topological_sort(graph.subgraph(dependency_list))
    return dependency_list


# Read graph

infile = open("data/graph.json", "r")
graph_dict = json.load(infile)
infile.close()

complete_graph = nx.DiGraph()

for node in graph_dict.keys():
    category, node = node.split("/")
    complete_graph.add_node(node, color=colors[category])

for node, predecessors in graph_dict.iteritems():
    category, node = node.split("/")
    complete_graph.add_edges_from([(pred.split("/")[1], node) for pred in predecessors])

infofile = open("info/all.txt", "w")

# Draw complete graph

graph = graph_nx2pgv(complete_graph)

graph.draw("figs/all.pdf", prog="sfdp", args='-Nstyle=bold -Goverlap="prism100000"')

infofile.write("Complete Graph: {} nodes, {} edges\n".format(complete_graph.number_of_nodes(), complete_graph.number_of_edges()))


# Draw WCCs

components = nx.weakly_connected_component_subgraphs(complete_graph)

subgraphs = collections.defaultdict(nx.DiGraph)
for i, component in enumerate(components):
    for node in component.nodes_iter():
        subgraphs[len(component)].add_node(node, color=complete_graph.node[node]["color"])
    for node_a, node_b in component.edges_iter():
        subgraphs[len(component)].add_edge(node_a, node_b)

for i, (n, subgraph) in enumerate(sorted(subgraphs.items(), key=lambda a: a[0])):
    infofile.write("Weakly Connected Components #{}: {} components of size {}, total number of nodes = {}\n".format(i+1, len(subgraph)/n, n, len(subgraph)))
    graph = graph_nx2pgv(subgraph)
    if n == 1:
        graph.draw("figs/wcc_{}.pdf".format(i+1), prog="sfdp")
    else:
        graph.draw("figs/wcc_{}.pdf".format(i+1), prog="dot")

# Draw dependency graphs

dependency_list_sizes = {}
for node in complete_graph.nodes_iter():
    
    dependency_list = dependency_resolution(complete_graph, node)
    dependency_list_sizes[node] = len(dependency_list)
   
    outfile = open("queues/{}.sqf".format(node), "w")
    outfile.write("\n".join(dependency_list))
    outfile.close()

    graph = graph_nx2pgv(complete_graph.subgraph(dependency_list))
    graph.draw("queues/{}.png".format(node), prog="dot", args='-Nstyle="filled" -Nfillcolor="white" -Gbgcolor="transparent"')

for i, (node, n) in enumerate(sorted(dependency_list_sizes.items(), key=lambda a: a[1], reverse=True)):
    infofile.write("Dependency Graph #{}: node \"{}\", number of nodes = {}\n".format(i+1, node, n))


infofile.close()

