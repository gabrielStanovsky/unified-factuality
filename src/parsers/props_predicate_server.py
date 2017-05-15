#!/usr/bin/env python
#coding:utf8
from bottle import route, run, get, post, request, response, static_file
import sys
props_path = "../props"
sys.path.insert(0, props_path)
# After adding the props path we can import its packages and load parsers
from props.webinterface.log import log
import props.applications.run  
import bottle
from props.applications.viz_tree import DepTreeVisualizer
from props.applications.run import load_berkeley
from props.applications.run import parseSentences

from props.applications.run import load_berkeley
import os.path
import codecs
from cStringIO import StringIO
import sys,time,datetime
from subprocess import call
import svg_stack as ss
from props.applications.run import parseSentences

try:
    PORT=int(sys.argv[1])
except:
    PORT=8081



def is_single_word_predicate(node):
    """
    Return true iff the node represents a single-word, non-implicit, predicate
    """
    return node.isPredicate \
        and (len(node.text) == 1) \
        and (not node.is_implicit())

def ent_to_str(ent, default):
    """
    Return a string representation of a single word entry.
    Also replaces the DEFAULT label with the default value
    """
    ent[2] = (ent[2] \
              if ent[2] != Truth_teller_factuality_annotator.DEFAULT \
              else default)
    return '\t'.join(map(str,ent))

def _get_props_predicate_indices(sent):
    """
    Get PropS' predicate indices for a given sentence
    """
    graph = single_sentence_props(sent)
    return  ",".join(map(str,
                         [node.text[0].index - 1
                          for node in graph.nodes()
                          if is_single_word_predicate(node)]))

def single_sentence_props(sent):
    """
    Return a graph representation of a single sentence with PropS
    """
    g,tree = parseSentences(sent, props_path)[0]
    return g

@get('/tparse')
def tparse():
    print "in tparse"
    sent = request.GET.get('text','').strip()
    print sent
    sents = sent.strip().replace(". ",".\n").replace("? ","?\n").replace("! ","!\n").split("\n")
    sent = sents[0]
    gs = parseSentences(sent)
    g,tree = gs[0]
    print "returning...." 
    return _get_props_predicate_indices(sent)


load_berkeley()
print("sanity check = {}".format(_get_props_predicate_indices("John refused to run")))
run(host='',port=PORT)
