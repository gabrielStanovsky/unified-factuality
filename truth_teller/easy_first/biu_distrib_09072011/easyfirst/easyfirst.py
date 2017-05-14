## Copyright 2010 Yoav Goldberg
##
## This file is part of easyfirst
##
##    easyfirst is free software: you can redistribute it and/or modify
##    it under the terms of the GNU General Public License as published by
##    the Free Software Foundation, either version 3 of the License, or
##    (at your option) any later version.
##
##    easyfirst is distributed in the hope that it will be useful,
##    but WITHOUT ANY WARRANTY; without even the implied warranty of
##    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##    GNU General Public License for more details.
##
##    You should have received a copy of the GNU General Public License
##    along with easyfirst.  If not, see <http://www.gnu.org/licenses/>.

import math
import random
import sys
import os.path
from collections import defaultdict
from itertools import izip,islice

from deps import DependenciesCollection
sys.path.append(os.path.join(os.path.dirname(__file__),"../shared"))
from ml.ml import MulticlassModel, MultitronParameters 

from pio import io
import isprojective 

from common import PAD,ROOT

from moduleloader import load_module

class Oracle: #{{{
   def __init__(self):
      self.sent = None
      self.childs = defaultdict(set)

   def allow_connection(self, sent, deps, parent, child):
      if self.sent != sent:
         self.sent = sent
         self.childs = defaultdict(set)
         for tok in sent:
            self.childs[tok['parent']].add((tok['parent'],tok['id']))

      if child['parent'] != parent['id']: 
         return False
      # if child didn't collect all it's childs, it can't connect.
      if len(self.childs[child['id']] - deps.deps) > 0:
         return False
      return True
   #}}}

class Parser: #{{{
   def __init__(self, scorer, featExt, oracle=None):
      self.scorer=scorer
      self.featExt=featExt
      self.oracle=oracle

   def vis_parse(self, sent): #{{{
      deps = DependenciesCollection()
      parsed = sent[:]
      parsed=[ROOT]+parsed
      sent = [ROOT]+sent
      connections = 0
      mistake=False
      for tok in parsed: tok['s']=tok['form']
      fcache={}
      scache={}
      while len(parsed)>1:
         # find best action
         best = -9999999
         best_pair = None 
         scores = {}
         for i,(tok1,tok2) in enumerate(zip(parsed,parsed[1:])):
            tid=tok1['id']
            if tid in fcache:
               feats = fcache[tid]
            else:
               feats = self.featExt.extract(parsed,deps,i,sent)
               fcache[tid] = feats
            if tid in scache:
               s1,s2 = scache[tid]
            else:
               scr = self.scorer.get_scores(feats)
               s1 = scr[0]
               s2 = scr[1]
               scache[tid]=s1,s2
            if s1 > best:
               best = s1
               best_pair = (tok1,tok2)
            if s2 > best:
               best = s2
               best_pair = (tok2,tok1)
            scores[(i,i+1)]=s1
            scores[(i+1,i)]=s2
            
         c,p = best_pair
         # remove the neighbours of parent from the cache
         i = parsed.index(p)
         frm=i-4
         to=i+4
         if frm<0: frm = 0
         if to>=len(parsed):to=len(parsed)-1
         for tok in parsed[frm:to]:
            try:
               del fcache[tok['id']]
               del scache[tok['id']]
            except: pass
         ###
         yield (self.oracle,sent, parsed, deps, scores)
         # apply action
         deps.add(p,c)
         connections += 1
         parsed = [x for x in parsed if x!=c]
      yield (self.oracle,sent, parsed, deps, scores)
   #}}}
   def parse(self, sent): #{{{
      deps = DependenciesCollection()
      parsed = sent[:]
      parsed=[ROOT]+parsed
      sent = [ROOT]+sent
      scache={}
      fe=self.featExt.extract
      gscore=self.scorer.get_scores
      lp = len(parsed) 
      while lp>1:
         # find best action
         _pairs=[]
         for i,(tok1,tok2) in enumerate(izip(parsed,islice(parsed,1,None))): 
            tid=tok1['id']
            if tid in scache:
               s1,s2 = scache[tid]
            else:
               feats = fe(parsed,deps,i,sent)
               scr = gscore(feats)
               s1 = scr[0]
               s2 = scr[1]
               scache[tid]=s1,s2

            _pairs.append((s1,tok1,tok2,i+1))
            _pairs.append((s2,tok2,tok1,i))
            
         best,c,p,locidx = max(_pairs)
         # remove the neighbours of parent from the cache
         i = locidx
         frm=i-4
         to=i+4
         if frm<0: frm = 0
         if to>=lp:to=lp-1
         for tok in parsed[frm:to]: 
            try:
               del scache[tok['id']]
            except: pass
         # apply action
         deps.add(p,c)
         parsed.remove(c)
         lp-=1
      return deps

   #}}}

   def parse2(self, sent): #{{{
      deps = DependenciesCollection()
      parsed = sent[:]
      parsed=[ROOT]+parsed
      sent = [ROOT]+sent
      scache={}
      fe=self.featExt.extract
      gscore=self.scorer.get_scores
      lp = len(parsed) 
      anum=0
      order=[]
      while lp>1:
         anum+=1
         # find best action
         _pairs=[]
         for i,(tok1,tok2) in enumerate(izip(parsed,islice(parsed,1,None))): 
            tid=tok1['id']
            if tid in scache:
               s1,s2 = scache[tid]
            else:
               feats = fe(parsed,deps,i,sent)
               scr = gscore(feats)
               s1 = scr[0]
               s2 = scr[1]
               scache[tid]=s1,s2

            _pairs.append((s1,tok1,tok2,i+1))
            _pairs.append((s2,tok2,tok1,i))
            
         best,c,p,locidx = max(_pairs)
         # remove the neighbours of parent from the cache
         i = locidx
         frm=i-4
         to=i+4
         if frm<0: frm = 0
         if to>=lp:to=lp-1
         for tok in parsed[frm:to]: 
            try:
               del scache[tok['id']]
            except: pass
         # apply action
         deps.add(p,c)
         order.append((p['id'],c['id'],anum))
         parsed.remove(c)
         lp-=1
      return deps, order

   #}}}

   def train(self, sent): #{{{
      updates=0
      sent = [ROOT]+sent
      self.scorer.tick()
      deps = DependenciesCollection()
      parsed = sent[:]
      fcache = {}
      scache = {}
      while len(parsed)>1: #{{{
         # find best action
         best = -9999999
         best_pair = None 
         scored = []
         for i,(tok1,tok2) in enumerate(zip(parsed,parsed[1:])):
            tid = tok1['id']
            if tid in fcache:
               feats = fcache[tid]
            else:
               feats = self.featExt.extract(parsed,deps,i,sent)
               fcache[tid]=feats
            if tid in scache:
               s1,s2 = scache[tid]
            else:
               scores = self.scorer.get_scores(feats)
               s1 = scores[0]
               s2 = scores[1]
               scache[tid] = s1,s2
            scored.append((s1,0,feats,tok1,tok2))
            scored.append((s2,1,feats,tok2,tok1))
         scored=sorted(scored,key=lambda (s,cls,f,t1,t2):-s)
         s,cls,f,c,p = scored[0]

         if self.oracle.allow_connection(sent,deps,p,c):
            # remove the neighbours of parent from the cache
            i = parsed.index(p)
            frm=i-4
            to=i+4
            if frm<0: frm = 0
            if to>=len(parsed):to=len(parsed)-1
            for tok in parsed[frm:to]:
               try:
                  del fcache[tok['id']]
                  del scache[tok['id']]
               except: pass
            ###
            deps.add(p,c)
            parsed = [x for x in parsed if x!=c]
         else:
            scache = {} # clear the cache -- numbers changed..
            # find best allowable pair
            for s,gcls,gf,gc,gp in scored[1:]:
               if self.oracle.allow_connection(sent,deps,gp,gc):
                  break

            self.scorer.add(f,cls,-1)
            self.scorer.add(gf,gcls,1)

            updates+=1
            if updates>200:
               print "STUCK, probably because of incomplete feature set"
               print " ".join([x['form'] for x in sent])
               print " ".join([x['form'] for x in parsed])
               return
      #}}} end while
   #}}}
#}}}


class Model: #{{{
   def __init__(self, featuresFile, weightFile, iter=None):
      self._featuresFile = featuresFile
      self._weightFile = weightFile
      self._iter=iter

      featuresModule = load_module(featuresFile)
      self.fext = featuresModule.FeaturesExtractor()


   def save(self, filename):
      fh = file(filename,"w")
      fh.write("%s\n%s\n" % (self._featuresFile, self._weightFile))
      fh.close()

   @classmethod
   def load(cls, filename, iter=19):
      lines = file(filename,"r").readlines()
      dirname = os.path.dirname(filename)
      featuresFile = os.path.join(dirname,lines[0].strip())
      weightFile   = os.path.join(dirname,lines[1].strip())
      return cls(featuresFile, weightFile, iter)

   def weightsFile(self, iter):
      if iter is None: iter = self._iter
      return "%s.%s" % (self._weightFile, iter)

   def featureExtractor(self):
      return self.fext
#}}}

def train(sents, model, dev=None,ITERS=20,save_every=None):
   fext = model.featureExtractor()
   oracle=Oracle()
   scorer=MultitronParameters(2)
   parser=Parser(scorer, fext, oracle)
   for ITER in xrange(1,ITERS+1):
      print "Iteration",ITER,"[",
      for i,sent in enumerate(sents):
         if i%100==0: 
            print i,
            sys.stdout.flush()
         parser.train(sent) 
      print "]"
      if save_every and (ITER % save_every==0):
         print "saving weights at iter",ITER
         parser.scorer.dump_fin(file(model.weightsFile(ITER),"w"))
         if dev:
            print "testing dev"
            print "\nscore: %s" % (test(dev,model,ITER,quiet=True),)
      parser.scorer.dump_fin(file(model.weightsFile("FINAL"),"w"))

def test(sents,model,iter="FINAL",quiet=False,ignore_punc=False):
   fext = model.featureExtractor()
   import time
   good = 0.0
   bad  = 0.0
   complete = 0.0
   m=MulticlassModel(model.weightsFile(iter))
   start = time.time()
   parser=Parser(m,fext,Oracle())
   scores=[]
   for sent in sents:
      sent_good=0.0
      sent_bad =0.0
      no_mistakes=True
      if not quiet:
         print "@@@",good/(good+bad+1)
      deps=parser.parse(sent)
      sent = deps.annotate(sent)
      for tok in sent:
         if not quiet: print tok['id'], tok['form'], "_",tok['tag'],tok['tag'],"_",tok['pparent'],"_ _ _"
         if ignore_punc and tok['form'][0] in "'`,.-;:!?{}": continue
         if tok['parent']==tok['pparent']:
            good+=1
            sent_good+=1
         else:
            bad+=1
            sent_bad+=1
            no_mistakes=False
      if not quiet: print
      if no_mistakes: complete+=1
      scores.append((sent_good/(sent_good+sent_bad)))

   if not quiet:
      print "time(seconds):",time.time()-start
      print "num sents:",len(sents)
      print "complete:",complete/len(sents)
      print "macro:",sum(scores)/len(scores)
      print "micro:",good/(good+bad)
   return good/(good+bad), complete/len(sents)

def parse(sents,model,iter="FINAL"):
   fext = model.featureExtractor()
   m=MulticlassModel(model.weightsFile(iter))
   parser=Parser(m,fext,Oracle())
   for sent in sents:
      deps=parser.parse(sent)
      sent = deps.annotate(sent)
      for tok in sent:
         print tok['id'], tok['form'], "_",tok['tag'],tok['tag'],"_",tok['pparent'],"_ _ _"
      print 

def make_parser(modelfile,iter):
   weightsFile = "%s.weights" % (modelfile)
   modelfile = "%s.model" % (modelfile)
   model = Model.load(modelfile,iter)
   fext = model.featureExtractor()
   m=MulticlassModel(model.weightsFile(iter))
   parser=Parser(m,fext,Oracle())
   return parser

def load_sentences(filename,ONLY_PROJECTIVE=False):
   sents = [s for s in io.conll_to_sents(file(filename)) if (not ONLY_PROJECTIVE) or isprojective.is_projective(s)]
   return sents

