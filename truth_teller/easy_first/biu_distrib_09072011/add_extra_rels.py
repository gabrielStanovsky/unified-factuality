#!/usr/bin/env python

"""
add the "extra" non-tree relations to a projective parse.

ref: 
   ref : referent
   A referent of the head of an NP is the relative word introducing the relative clause modifying
   the NP.
   "I saw the book which you bought" ref (book, which)

   from (rcmod, rc_parent, rc_child)  [rcmod, book, bought]
      return: (ref, rc_parent, rc_child[left_most]

   
xsubj:
   xsubj : controlling subject
   A controlling subject is the relation between the head of a open clausal complement (xcomp) and the external subject of that clause.
   "Tom likes to eat fish" xsubj (eat, Tom)

   from (xcomp, x_parent, x_child)   [xcomp, likes, eat]
      return (xsubj, x_child, x_parent[subject])

dobj:
   rcmod where child does not have a dobj: make parent the dobj?  (the *way* he is *behaving*)
"""
from collections import defaultdict
import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__),"shared"))
from common import ROOT

relativizers = set("that what which who whom whose".split())

def extra_deps(sent, no_adj_xsubj=True,par='parent'):
   rsent = [ROOT]+sent
   childs = defaultdict(list)
   for tok in sent:
      childs[tok[par]].append(tok)
   
   extracted=set()
   for tok in sent:
      if tok['prel']=='rcmod':
         # ref
         ## NOTE/TODO: 'whose' is not just the child, but the left-most grand*child
         for child in childs[tok['id']]:
            if child['form'].lower() in relativizers:
               yield ("ref",rsent[tok[par]],child)
               extracted.add((tok[par],child['id']))
               break
         
         # check also the left-most grad**child
         leftmost=childs[tok['id']]
         while leftmost and childs[leftmost[0]['id']]:
            leftmost = childs[leftmost[0]['id']]
         if leftmost and leftmost[0]['form'].lower() in relativizers and (tok[par],leftmost[0]['id']) not in extracted:
            yield ("ref",rsent[tok[par]],leftmost[0])

         # dobj:
         # an rcmod where the child is a verb and has no dobj, make the parent the dobj
         #This creates many bad ones
         #if tok['tag'] in ('VBZ','VBD','VB'):
         #   has_dobj=False
         #   for child in childs[tok['id']]:
         #      if child['prel']=='dobj': 
         #         has_dobj=True
         #         break
         #   if not has_dobj:
         #      yield ("dobj",tok,rsent[tok['parent']])

      # xsubj
      elif tok['prel']=='xcomp':
         ##TODO: support for conjunctions

         # verify tok has an aux/to child
         # and that it does not have a subject already (they allowed x to do y)
         found=False
         subj=False
         for child in childs[tok['id']]: 
            if child['prel']=='aux' and child['form']=='to':
               found=True
            if 'subj' in child['prel']:
               subj=True
               break
         if found and not subj:
            parent = rsent[tok[par]]
            if no_adj_xsubj and parent['tag'][0]=='J': continue # "they are *likely* to go"
            for child in childs[parent['id']]:
               if 'subj' in child['prel']:
                  yield ("xsubj",tok,child)

if __name__=='__main__':
   import sys
   sys.path.append("..")
   from pio import io
   from common import ROOT

   for i,sent in enumerate(io.conll_to_sents(sys.stdin)):
      for extra in extra_deps(sent):
         #print extra[0],extra[1]['form'],extra[2]['form']
         print i,"%s(%s-%s, %s-%s)" % (extra[0],extra[1]['form'],extra[1]['id'],extra[2]['form'],extra[2]['id'])
   


   
