#!/usr/bin/env python
from bottle import route, run, get, post, request, response
import bottle
bottle.debug(True)
import os.path

MAIN = os.path.join(os.path.dirname(__file__),"form.html")

HERE = os.path.dirname(__file__)
from add_extra_rels import extra_deps
import sys
sys.path.append(os.path.join(HERE,"easyfirst"))
import easyfirst
sys.path.append(os.path.join(HERE,"labeler"))
import eflabeler
from pio import io
import time
from sdparser import *
import cStringIO

sys.path.append(os.path.join(HERE,"wnetlem"))
from wordnet import WN

reader = read_tagged

#PARSE_MODEL=os.path.join(HERE,"models","stn.2-21.stntag")
#LABEL_MODEL=os.path.join(HERE,"models","labeler.model")
PARSE_MODEL=os.path.join(HERE,"models","sd165.2-2-21.stntag.stnfeaturesplus.sp10.model")
LABEL_MODEL=os.path.join(HERE,"models","sd165.2-2-21.labeler.sp10.4")

labeler = eflabeler.SimpleSentenceLabeler(eflabeler.Labeler.load(LABEL_MODEL), fext=eflabeler.AnEdgeLabelFeatureExtractor6())
parser = easyfirst.make_parser(PARSE_MODEL, "FINAL")

def _lemmatize(sent,which={"V":lambda x:WN.morphy(x,WN.VERB),"J":lambda x:WN.morphy(x,WN.ADJ), "R":lambda x:WN.morphy(x,WN.ADV), "N":lambda x:WN.morphy(x,WN.NOUN)} ):
   for tok in sent:
      ttag=tok['tag'][0]
      if ttag in 'NAVR': tok['lem']=which[ttag](tok['form'])
      else: tok['lem']=None
      if not tok['lem']: tok['lem']=tok['form'].lower()

def _parse_tagged_text(tagged_text_str):
   fh = cStringIO.StringIO(tagged_text_str)
   fout = cStringIO.StringIO()
   for sent in read_tagged(fh):
      deps=parser.parse(sent)
      deps.annotate(sent)
      labeler.label(sent, par='pparent',prelout='prel',sent_guides=None)
      try: extra = extra_deps(sent,par='pparent')
      except:
         print >> sys.stderr,"error processing sentence, not adding extra deps"
         extra = []
      try: lemmatize = _lemmatize(sent)
      except: pass
      conll_out(sent,extra,fout)
   return fout.getvalue()

@route('/')
def index():
   return file(MAIN).read()

@post('/parse')
def parse():
   response.content_type = 'text/plain'
   tagged = request.forms.get("tagged_text")
   parsed = _parse_tagged_text(tagged)
   #print parsed
   return parsed

if len(sys.argv)==1:
	run(host='',port=8080)
else:
	run(host='',port=sys.argv[1])

