# import network analysis
import networkx as nx
from networkx.algorithms import bipartite

# import drawing library
import matplotlib.pyplot as plt

import os
import telnetlib
import json
import re

from nltk.tokenize import sent_tokenize



layout=nx.spring_layout



def extract_ne(ctree, text):
    with open(os.path.join(ctree.path, "entities"), "w") as dumpfile:
        json.dump(get_NE(ctree, text), dumpfile)


def get_NE(ctree, text):
    """
    Returns found entities, where ne is one of ["PERSON", "ORGANIZATION", "LOCATION"].
    """
    
    ctree_entities = {}

    for entity_type in ["PERSON", "ORGANIZATION", "LOCATION"]:
        ctree_entities[entity_type] = set()
    
    for sent in sent_tokenize(text):
        tagged_tokens = tag_NE(sent)
        
        
        for entity_type in ["PERSON", "ORGANIZATION", "LOCATION"]:
            
            entities = [tt[0] for tt in tagged_tokens if tt[1] == entity_type]
            ctree_entities.get(entity_type).update(loop_over_ngrams(entities, sent))
        
            
    return {k:list(v) for k, v in ctree_entities.items()}

    
def tag_NE(sentence):
    """
    This analysis only works with a locally running server instance of the Stanford NER Parser,
    http://nlp.stanford.edu/software/CRF-NER.shtml
    """
    if sentence:
        HOST = "127.0.0.1"
        PORT = 9190

        sent_string = sentence+"\n"
        tncon = telnetlib.Telnet(HOST, PORT)
        tncon.write(bytes(sent_string.encode("utf-8")))

        tagged_tokens = tncon.read_all().decode("utf-8").split()
        # tagged_tokens is a list of tokens like ["word/PERSON", "word/O", "word/LOCATION"]

        tagged_tokens = [tuple(token.split("/")) for token in tagged_tokens]
        # creates a list of tuples from tokens like [("word", "PERSON"), ...]
        try:
            tagged_tokens = [tt for tt in tagged_tokens if tt[1] != "O" and len(tt) == 2]
            return tagged_tokens
        except:
            return []
        
        
def loop_over_ngrams(tokens, text):
    """
    Creates entities of length up to four out of found entities,
    and searches for them first, e.g. Federal Reserve Bank.
    If an entity like Federal Reserve exists, it will not be 
    searched for separately.
    """
    ngram_entities = []

    tokens_found = set()


    def create_ngrams(tokens, n):
        ngramslist = []
        for i in range(len(tokens)-n+1):
            ngramslist.append(" ".join(tokens[i:i+n]))
        return ngramslist


    def find_tokens(ngrams):
        for ngram in ngrams:
            check = 0
            if tokens_found:
                for tf in tokens_found:
                    if ngram in tf:
                        check += 1
                if check == 0:
                    find_occurrences(ngram)
            else:
                find_occurrences(ngram)


    def find_occurrences(gram):
        try:
            occurrences = [{"start":m.start(0), "end":m.end(0)} 
                                   for m in re.finditer(gram, text)]
        except Exception, e:
            print gram, e
            occurrences = []
        if occurrences:
            tokens_found.add(gram)


    find_tokens(create_ngrams(tokens, 8))
    find_tokens(create_ngrams(tokens, 7))
    find_tokens(create_ngrams(tokens, 6))
    find_tokens(create_ngrams(tokens, 5))
    find_tokens(create_ngrams(tokens, 4))
    find_tokens(create_ngrams(tokens, 3))
    find_tokens(create_ngrams(tokens, 2))
    find_tokens(tokens)

    return tokens_found


def create_network(CProject, plugin, query):
        """
        Creates the network between papers and plugin results.
        
        Args: CProject object
              plugin = "string"
              query = "string"
        
        Returns: (bipartite_graph, monopartite_graph, paper_nodes, fact_nodes)
        """
        
        B = nx.Graph()
        labels = {}

        for ct in CProject.get_ctrees():
            
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

        
        paper_nodes = set(n for n,d in B.nodes(data=True) if d['bipartite']==0)
        fact_nodes = set(B) - paper_nodes
        G = bipartite.weighted_projected_graph(B, fact_nodes)
        
        return B, G, paper_nodes, fact_nodes
    

def plotGraph(graph, color="r", figsize=(12, 8)):
    
    labels = {n:n for n in graph.nodes()}
    
    d = nx.degree_centrality(graph)
    
    layout=nx.spring_layout
    pos=layout(graph)
    
    plt.figure(figsize=figsize)
    plt.subplots_adjust(left=0,right=1,bottom=0,top=0.95,wspace=0.01,hspace=0.01)
    
    # nodes
    nx.draw_networkx_nodes(graph,pos,
                            nodelist=graph.nodes(),
                            node_color=color,
                            node_size=[v * 250 for v in d.values()],
                            alpha=0.8)
                            
    nx.draw_networkx_edges(graph,pos,
                           with_labels=False,
                           edge_color=color,
                           width=0.50
                        )
    
    if graph.order() < 1000:
        nx.draw_networkx_labels(graph,pos, labels)
    return plt
    

def plotBipartiteGraph(graph, color1="r", color2="b", figsize=(12, 8)):
 
    labels = {n:n for n in graph.nodes()}
    
    d = nx.degree_centrality(graph)
    
    layout=nx.spring_layout
    pos=layout(graph)

    bot_nodes, top_nodes = bipartite.sets(graph)

    plt.figure(figsize=figsize)
    plt.subplots_adjust(left=0,right=1,bottom=0,top=0.95,wspace=0.01,hspace=0.01)
    
    # nodes
    nx.draw_networkx_nodes(graph,pos,
                            nodelist=bot_nodes,
                            node_color=color1,
                            node_size=[v * 350 for v in d.values()],
                            alpha=0.8)
    nx.draw_networkx_nodes(graph,pos,
                            nodelist=top_nodes,
                            node_color=color2,
                            node_size=[v * 350 for v in d.values()],
                            alpha=0.8)
    
    nx.draw_networkx_edges(graph,pos,
                           with_labels=True,
                           edge_color=color1,
                           width=1.0
                        )
    
    if graph.order() < 1000:
        nx.draw_networkx_labels(graph,pos, labels)
        
    return plt

    
def create_subgraph(cproject, B, G, target):
    
    sg = nx.Graph()
    sg.add_node(target)
    
    for ID in B.neighbors(target):
        sg.add_node(ID)
        sg.add_edge(target, ID)
        for author in cproject.get_ctree(ID).get_authors():
            if not author in sg.nodes():
                sg.add_node(author)
            sg.add_edge(ID, author)
            
    for neighbor in G.neighbors(target):
        sg.add_node(neighbor)
        sg.add_edge(target, neighbor)
        for ID in B.neighbors(neighbor):
            sg.add_node(ID)
            sg.add_edge(neighbor, ID)
            for author in cproject.get_ctree(ID).get_authors():
                if not author in sg.nodes():
                    sg.add_node(author)
                sg.add_edge(ID, author)
    
    return sg

def save_graph(graph, color):
    plotGraph(graph, color, figsize=(36, 23)).savefig("Your-Graph.png")

