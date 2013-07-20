SlackBuildsViz
==============

Scripts to collect and visualize dependency graphs from SlackBuilds.org

##Dependencies

* NetworkX (http://networkx.github.io/)
* PyGraphviz (http://networkx.lanl.gov/pygraphviz/)

##Execution

* ./collect.py - retrieves information from SlackBuilds.org and creates the dependency grpah
* ./draw.py - reads graph and draws the figures and create the queue files

##Files

* data/graph.json - complete dependency graph
* figs/all.pdf - figure of the complete dependency graph
* figs/wcc_*.pdf - figures of weakly connected components
* info/all.txt - information (number of nodes, edges, etc) about the subgraphs
* logs/* - logs of the scripts
* queues/[package_name].sqf - queue file for building package_name
* queues/[package_name].png - figure of the dependency graph of package_name

