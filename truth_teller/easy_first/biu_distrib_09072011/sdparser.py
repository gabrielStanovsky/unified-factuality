#!/usr/bin/env python

"""
parse to stanford-dependencies using the easy-first parser + labeler
"""
import copy
import sys

def read_tagged(fh):
   for line in fh:
      #res = (x.rsplit("_",1) for x in line.strip().split())
      ## the 'CD' default is workaround for a stanford-tagger bug of 
      ## not tagging "(213)" in "The_DT editor_NN is_VBZ Carlos_NNP Selva_NNP in_IN Los_NNP Angeles_NNP at_IN (213) 237-7832_CD ._."
      res = (x.rsplit("_",1) if '_' in x else (x,'CD') for x in line.strip().split()) 
      res = [{'form':f,'id':id,'tag':t} for id,(f,t) in enumerate(res,1)]
      yield res

def stanford_out(sent,extra):
   toks={0:None}
   for tok in sent:
      toks[tok['id']]=tok
   
   for tok in sent:
      parent = toks[tok['pparent']]
      if parent is None: continue #ROOT
      print "%s(%s-%s, %s-%s)" % (tok['prel'],parent['form'],parent['id'],tok['form'],tok['id'])

   extra = list(extra)
   if extra: print "==="
   for rel,par,ch in extra:
      print "%s(%s-%s, %s-%s)" % (rel, par['form'],par['id'],ch['form'],ch['id'])
   print

def conll_out(sent,extra=None,outf=sys.stdout):
   from pio import io
   for rel,par,chl in extra:
      newchl = copy.copy(chl)
      newchl['tag'] = 'COIDX_%s' % chl['id']
      newchl['id'] = len(sent)+1
      newchl['pparent'] = par['id']
      newchl['prel'] = rel
      sent.append(newchl)
   io.out_conll(sent,parent='pparent',out=outf)


def stanford_out_order(sent,extra):
   toks={0:None}
   for tok in sent:
      toks[tok['id']]=tok
   
   for tok in sent:
      parent = toks[tok['pparent']]
      if parent is None: continue #ROOT
      print "%s(%s-%s, %s-%s) ||| %s" % (tok['prel'],parent['form'],parent['id'],tok['form'],tok['id'],tok['order'])

   extra = list(extra)
   if extra: print "==="
   for rel,par,ch in extra:
      print "%s(%s-%s, %s-%s)" % (rel, par['form'],par['id'],ch['form'],ch['id'])
   print

if __name__=='__main__':
   import os.path
   HERE = os.path.dirname(__file__)
   from add_extra_rels import extra_deps
   import sys
   sys.path.append(os.path.join(HERE,"easyfirst"))
   import easyfirst
   sys.path.append(os.path.join(HERE,"labeler"))
   import eflabeler
   from pio import io
   import time

   if '-conll' in sys.argv:
      reader = io.conll_to_sents
   else:
      reader = read_tagged

   if '-order' in sys.argv:
      ORDER=True
   else: 
      ORDER=False

   if '-noextra' in sys.argv:
      EXTRA=False
   else:
      EXTRA=True
   
   #PARSE_MODEL=os.path.join(HERE,"models","stn.2-21.stntag")
   #LABEL_MODEL=os.path.join(HERE,"models","labeler.model")
   PARSE_MODEL=os.path.join(HERE,"models","sd165.2-2-21.stntag.stnfeaturesplus.sp10.model")
   LABEL_MODEL=os.path.join(HERE,"models","sd165.2-2-21.labeler.sp10.4")

   TEST_SENTS = reader(sys.stdin)

   labeler = eflabeler.SimpleSentenceLabeler(eflabeler.Labeler.load(LABEL_MODEL), fext=eflabeler.AnEdgeLabelFeatureExtractor6())
   parser = easyfirst.make_parser(PARSE_MODEL, "FINAL")

   stime = time.time()
   for sent in TEST_SENTS:
      if ORDER:
         deps,order=parser.parse2(sent)
         for p,c,o in order:
            sent[c-1]['order']=o
      else:
         deps=parser.parse(sent)
      deps.annotate(sent)
      labeler.label(sent, par='pparent',prelout='prel',sent_guides=None)
      # add extra rels
      if EXTRA:
         extra = extra_deps(sent,par='pparent')
      else: extra = []
      if ORDER:
         stanford_out_order(sent,extra)
      else:
         #stanford_out(sent,extra)
        conll_out(sent,extra)
   #print >> sys.stderr, time.time()-stime,"seconds"

