#!/usr/bin/python
# coding=utf-8

import urllib
import re
import json
import logging

logging.basicConfig(filename="logs/collect.txt", filemode="a", level=logging.INFO, format="[ %(asctime)s ] %(levelname)s : %(message)s")

SLACKWARE_VERSION = "14.0"

URL_BASE = "http://slackbuilds.org/repository"

def get_list_categories(version=SLACKWARE_VERSION):
    html = urllib.urlopen("{}/{}/".format(URL_BASE, version)).read()
    categories = re.findall("<a href=\"/repository/{}/([^/]+)/\" class=\"category-link\">[^<]+</a>".format(version), html)
    return categories 

def get_list_applications(category, version=SLACKWARE_VERSION):
    html = urllib.urlopen("{}/{}/{}/".format(URL_BASE, version, category)).read()
    applications = re.findall("<a href=\"/repository/{}/({}/[^/]+)/\">[^<]+</a>".format(version, category), html)
    applications = map(urllib.unquote, applications)
    return applications

def get_list_dependencies(application, version=SLACKWARE_VERSION):
    html = urllib.urlopen("{}/{}/{}/".format(URL_BASE, version, application)).read()
    search_dependencies = re.search("<p>This requires: (.+?)</p>", html)
    if search_dependencies is not None:
        dependencies = re.findall("<a href=\'/repository/{}/([^/]+/[^/]+)/\'>[^<]+</a>".format(version), search_dependencies.group(1))
    else:
        dependencies = []
    return dependencies

def get_graph_dependencies():
    logging.info("GRAPH CREATION STARTED")
    categories = get_list_categories()
    logging.info("Found {} categories".format(len(categories)))
    applications = []
    for category in categories:
        category_applications = get_list_applications(category) 
        logging.info("Category {} found {} applications".format(category, len(category_applications)))
        applications.extend(category_applications)
    logging.info("Found {} applications".format(len(applications)))
    graph = {}
    for application in applications:
        application_dependencies = get_list_dependencies(application) 
        logging.info("Application {} found {} dependencies".format(application, len(application_dependencies)))
        graph[application] = application_dependencies
    logging.info("GRAPH CREATION FINISHED")
    return graph

if __name__ == "__main__":

    graph = get_graph_dependencies()

    outfile = open("data/graph.json", "w")
    json.dump(graph, outfile, indent=4)
    outfile.close()

