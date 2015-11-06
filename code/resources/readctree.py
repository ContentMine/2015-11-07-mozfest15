# import file io
import re
import os
from lxml import etree

import json
import pickle

# import data handling and preprocessing
from bs4 import BeautifulSoup
from nltk.tokenize import sent_tokenize

import networkx as nx
from networkx.algorithms import bipartite



class CProject(object):
    """
    Maps the CProject file structure to a data object.
    """
    def __init__(self, projectname):
        self.projectname = projectname
        self.projectfolder = os.path.join(os.getcwd(), projectname)
        self.size = self.get_size()
    
    def get_ctree(self, ctree_ID):
        return CTree(self.projectfolder, ctree_ID)
    
    
    def get_ctrees(self):
        for name in os.listdir(self.projectfolder):
            ctree = CTree(self.projectfolder, name)
            yield {ctree.ID: ctree}
    
    def get_size(self):
        """
        Returns size of dataset = number of ctrees.
        """
        i = 0
        for ct in self.get_ctrees():
            i += 1
        return i
        
    def get_title(self, ID):
        return self.get_ctree(ID).get_title()
        
    def create_network(self, plugin, query):
        """
        Creates the network between papers and plugin results.
        """
        
        B = nx.Graph()
        labels = {}

        for ct in self.get_ctrees():
            
            ctree_ID, ctree = ct.items()[0]

            results = ctree.show_results(plugin).get(query, [])

            if len(results) > 0:
                B.add_node(ctree_ID, bipartite=0)
                labels[str(ctree_ID)] = str(ctree_ID)

                for result in results:
                    B.add_node(result, bipartite=1)
                    labels[result] = result.encode("utf-8").decode("utf-8")
                    # add a link between a paper and author
                    B.add_edge(ctree_ID, result)

        self.B = B
        
        paper_nodes = set(n for n,d in B.nodes(data=True) if d['bipartite']==0)
        fact_nodes = set(B) - paper_nodes
        G = bipartite.weighted_projected_graph(B, fact_nodes)
        self.G = G
        
        return B
    


        
class CTree(object):
    """
    Maps the CTree file structure to a data object,
    provides some preprocessing and analysis methods.
    """
    
    def __init__(self, projectfolder, name):
        self.path = os.path.join(projectfolder, name)
        self.ID = name
        self.shtmlpath = self.get_shtmlpath()
        self.fulltextxmlpath = self.get_fxmlpath()
        self.resultspath = os.path.join(self.path, "results")
        self.available_plugins = self.get_plugins()
        self.plugin_queries = self.get_queries()
        self.results = self.get_results()
        self.entities = self.load_entities()
    
    def load_entities(self):
        try:
            with open(os.path.join(os.getcwd(), self.path, "entities"), "r") as dumpfile:
                return json.load(dumpfile)
        except:
            return []
    
    def get_shtmlpath(self):
        return os.path.join(self.path, "scholarly.html")
    
    def get_fxmlpath(self):
        return os.path.join(self.path, "fulltext.xml")
    
    def get_plugins(self):
        """
        Returns a dict of available ami-plug-results.
        ['sequence', 'regex', 'gene']
        """
        try:
            return os.listdir(self.resultspath)
        except:
            return []
    
    def get_queries(self):
        """
        Returns a dict of plugin:types,
        where plugin is an ami-plugin and types are the
        queries that have been run.
        {'regex': set(['clintrialids']), 
        'gene': set(['human']), 
        'sequence': set(['carb3', 'prot3', 'dna', 'prot'])}
        """
        return {plugin:set(os.listdir(os.path.join(self.resultspath, plugin))) for plugin in self.available_plugins}
            
    
    def get_results(self):
        results = {}
        for plugin, queries in self.plugin_queries.items():
            results[plugin] = {}
            for query in queries:
                results[plugin][query] = self.read_resultsxml(os.path.join(self.resultspath, plugin, query, "results.xml"))
        return results
        
        
    def read_resultsxml(self, filename):
        try:
            with open(filename, 'r') as infile:
                tree = etree.parse(infile)
            root = tree.getroot()
            results = root.findall('result')
            return [res.attrib.get("value0") for res in results]
        except:
            return []
    
    
    def show_results(self, plugin):
        if plugin == "entities":
            return self.entities
        
        else:
            return self.results.get(plugin)
    
    def get_soup(self):
        with open(self.shtmlpath, "r") as infile:
            return BeautifulSoup(infile)
    
    def get_section(self, section_title):
        """
        Returns a section of shtml,
        tokenized into sentences
        """
        section = []
        for sec in self.get_soup().find_all():
            if sec.string == section_title:
                for sib in sec.next_siblings:
                    section.append(sib.string)
        try:
            section = " ".join(section)
            section = " ".join(section.split())
        except:
            section = ""
        return section
        
    def get_authors(self):
        authors = []
        contrib_group = self.get_soup().find_all("div", {"tagx":"contrib-group"})
        for meta in contrib_group:
            for author in  meta.find_all("meta", {"name":"citation_author"}):
                authors.append(author.get("content"))
        return authors
    
    def get_acknowledgements(self):
        return self.get_section("Acknowledgements")
    
    def query_soup(self, tag, text):
        """
        Finds tags containing a certain text.
        """
        
        return self.get_soup().find_all(tag, text = re.compile(text))
    
    
    def find_tag(self, tag, attr):
        text = [""]
        tags = self.get_soup().find(tag, attr)
        if tags:
            for p in tags.find_all("p"):
                if p.string:
                    text.append(p.string)
        text = " ".join(text)
        return " ".join(text.split())
    
    def get_competing_interests(self):
        cis = []
        for ci in self.query_soup("b", "Competing interests"):
            cis.append(ci.find_next().string)
        try:
            text = " ".join(cis)
        except:
            text = ""
        text = " ".join(text.split())
        return text
    
    def get_abstract(self):
        abstract = []
        for ab in self.get_soup().find_all("div", {"tag":"abstract"}):
            for p in ab.find_all("p"):
                abstract.append(p.string)
        try:
            return " ".join(abstract)
        except:
            return ""
    
    def get_title(self):
        return self.get_soup().find("title").string