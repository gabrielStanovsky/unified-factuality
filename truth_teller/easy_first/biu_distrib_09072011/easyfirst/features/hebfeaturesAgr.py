from common import PAD,ROOT
"""
like hebfeatures, but with N-J agreement
"""
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


def is_male(morph):
   return 'M' in morph or 'B' in morph
def is_female(morph):
   return 'F' in morph or 'B' in morph
def is_single(morph):
   return 'S' in morph 
def is_plural(morph):
   return 'P' in morph 

def agree_g(m1,m2):
   if is_male(m1) and is_male(m2):
      return True
   if is_female(m1) and is_female(m2):
      return True
   return False

def agree_n(m1,m2):
   if is_single(m1) and is_single(m2):
      return True
   if is_plural(m1) and is_plural(m2):
      return True
   return False

class BaselineFeatureExtractor: # {{{ 
   LANG='HEB'
   def __init__(self):
      self.versions = None

   def extract(self,parsed,deps,i,sent=None):
      """
      i=T4:
         should I connect T4 and T5 in:
            t1 t2 t3 T4 T5 t6 t7 t8
         ?
         focus: f1=T4 f2=T5
         previous: p1=t3 p2=t2
         next:     n1=t6 n2=t7
      returns (feats1,feats2)
      where feats1 is a list of features for connecting T4->T5  (T4 is child)
      and   feats2 is a list of features for connecting T4<-T5  (T5 is child)
      """
      LANG = self.LANG
      CC = ['CC','CONJ']
      IN = [] # for Hebrew: do't lexicalize the prepositions (works better.. and we already get this info in bigram features..)
      j=i+1
      features=[]

      f1=parsed[i]
      f2=parsed[j]
      n1=parsed[j+1] if j+1 < len(parsed) else PAD
      n2=parsed[j+2] if j+2 < len(parsed) else PAD
      p1=parsed[i-1] if i-1 > 0 else PAD
      p2=parsed[i-2] if i-2 > 0 else PAD

      f1_form = f1['form'] 
      f2_form = f2['form'] 
      p1_form = p1['form'] 
      n1_form = n1['form'] 
      n2_form = n2['form'] 
      p2_form = p2['form'] 

      f1_tag = f1['tag'] 
      f2_tag = f2['tag'] 
      p1_tag = p1['tag'] 
      n1_tag = n1['tag'] 
      n2_tag = n2['tag'] 
      p2_tag = p2['tag'] 
      if f1_tag in IN: f1_tag = "%s%s" % (f1_tag,f1_form)
      if f2_tag in IN: f2_tag = "%s%s" % (f2_tag,f2_form)
      if p1_tag in IN: p1_tag = "%s%s" % (p1_tag,p1_form)
      if p2_tag in IN: p2_tag = "%s%s" % (p2_tag,p2_form)
      if n1_tag in IN: n1_tag = "%s%s" % (n1_tag,n1_form)
      if n2_tag in IN: n2_tag = "%s%s" % (n2_tag,n2_form)


      f1lc = deps.left_child(f1)
      if f1lc: f1lc=f1lc['tag']
      f2lc = deps.left_child(f2)
      if f2lc: f2lc=f2lc['tag']
      n1lc = deps.left_child(n1) 
      if n1lc: n1lc=n1lc['tag']
      n2lc = deps.left_child(n2) 
      if n2lc: n2lc=n2lc['tag']
      p1lc = deps.left_child(p1) 
      if p1lc: p1lc=p1lc['tag']
      p2lc = deps.left_child(p2) 
      if p2lc: p2lc=p2lc['tag']

      f1rc_form=None
      f1rc = deps.right_child(f1) 
      if f1rc: 
         f1rc_form=f1rc['form']
         f1rc=f1rc['tag']

      f2rc_form=None
      f2rc = deps.right_child(f2) 
      if f2rc: 
         f2rc_form=f2rc['form']
         f2rc=f2rc['tag']

      n1rc_form=None
      n1rc = deps.right_child(n1) 
      if n1rc: 
         n1rc_form=n1rc['form']
         n1rc=n1rc['tag']

      n2rc = deps.right_child(n2) 
      if n2rc: n2rc=n2rc['tag']
      p1rc = deps.right_child(p1) 
      if p1rc: p1rc=p1rc['tag']
      p2rc = deps.right_child(p2) 
      if p2rc: p2rc=p2rc['tag']

      append = features.append

      # N-J agreement:
      for which,a,b in (("f1f2",f1,f2),("f1n1",f1,n1),("p1f2",p1,f2),("p2f1",p2,f1),("f2n1",f2,n1)): # YG: 84.2
      #for which,a,b in (("f1f2",f1,f2),("f1n1",f1,n1),("p1f2",p1,f2),("p2f1",p2,f1),("f2n1",f2,n1), ("p1f1",p1,f1)): # YG: added last pair recently. for some reason it was missing. (84)
      #for which,a,b in (("f1f2",f1,f2),("f1n1",f1,n1),("p1f2",p1,f2)): # YG: try with some less (83.9)
         if a['tag'][0]=='N' and b['tag'][0]=='J':
            append("NJ_NA_%s_%s" % (which,agree_n(a['morph'],b['morph'])))
            append("NJ_GA_%s_%s" % (which,agree_g(a['morph'],b['morph'])))

      # lengths
      append("lp1f1_%s" % (f1['id']-p1['id']))
      append("lf1f2_%s" % (f2['id']-f1['id']))
      append("lf2n1_%s" % (n1['id']-f2['id']))
      append("lp2p1_%s" % (p1['id']-p2['id']))
      append("ln1n2_%s" % (n2['id']-n1['id']))

      append("lp1f1_%s_%s_%s" % (f1['id']-p1['id'],f1_tag,p1_tag))
      append("lf1f2_%s_%s_%s" % (f2['id']-f1['id'],f2_tag,f1_tag))
      append("lf2n1_%s_%s_%s" % (n1['id']-f2['id'],n1_tag,f2_tag))
      append("lp2p1_%s_%s_%s" % (p1['id']-p2['id'],p1_tag,p2_tag))
      append("ln1n2_%s_%s_%s" % (n2['id']-n1['id'],n2_tag,n1_tag))
      

      # "am I a word or more?" features
      sf1 = deps.left_child(f1)==None and deps.right_child(f1)==None
      sf2 = deps.left_child(f2)==None and deps.right_child(f2)==None
      sp1 = deps.left_child(p1)==None and deps.right_child(p1)==None
      sp2 = deps.left_child(p2)==None and deps.right_child(p2)==None
      sn1 = deps.left_child(n1)==None and deps.right_child(n1)==None
      sn2 = deps.left_child(n2)==None and deps.right_child(n2)==None

      append("sf1_%s_%s" % (f1_tag,sf1))
      append("sf2_%s_%s" % (f2_tag,sf2))
      append("sn1_%s_%s" % (n1_tag,sn1))
      append("sn2_%s_%s" % (n2_tag,sn2))
      append("sp1_%s_%s" % (p1_tag,sp1))
      append("sp2_%s_%s" % (p2_tag,sp2))

      # lens
      span = deps.span
      append("lenf1_%s_%s" % (f1_tag,span(f1)))
      append("lenf2_%s_%s" % (f2_tag,span(f2)))
      append("lenn1_%s_%s" % (n1_tag,span(n1)))
      append("lenn2_%s_%s" % (n2_tag,span(n2)))
      append("lenp1_%s_%s" % (p1_tag,span(p1)))
      append("lenp2_%s_%s" % (p2_tag,span(p2)))

      # unigram
      if f1_form: append("f1w_%s" % (f1_form))
      if f2_form: append("f2w_%s" % (f2_form))
      if p1_form: append("p1w_%s" % (p1_form))
      if p2_form: append("p2w_%s" % (p2_form))
      if n1_form: append("n1w_%s" % (n1_form))
      if n2_form: append("n2w_%s" % (n2_form))

      append("f1t_%s" % (f1_tag))
      append("f2t_%s" % (f2_tag))
      append("p1t_%s" % (p1_tag))
      append("p2t_%s" % (p2_tag))
      append("n1t_%s" % (n1_tag))
      append("n2t_%s" % (n2_tag))

      # bigram
      append("f1tf2t_%s_%s" % (f1_tag,f2_tag))

      append("p1tf1t_%s_%s" % (p1_tag,f1_tag))
      append("p1tf2t_%s_%s" % (p1_tag,f2_tag))

      append("f2tn1t_%s_%s" % (f2_tag,n1_tag))
      append("f1tn1t_%s_%s" % (f1_tag,n1_tag))

      # w bigram
      if f1_form and f2_form: append("f1tf2t_%s_%s" % (f1_form,f2_form))
      if p1_form and p2_form: append("p1tf1t_%s_%s" % (p1_form,f1_form))
      if p1_form and f2_form: append("p1tf2t_%s_%s" % (p1_form,f2_form))
      if p2_form and n1_form: append("f2tn1t_%s_%s" % (f2_form,n1_form))
      if f1_form and n1_form: append("f1tn1t_%s_%s" % (f1_form,n1_form))
      # w bigram t-w
      if f2_form: append("f1tf2t_%s_%s" % (f1_tag,f2_form))
      if f1_form: append("p1tf1t_%s_%s" % (p1_tag,f1_form))
      if f2_form: append("p1tf2t_%s_%s" % (p1_tag,f2_form))
      if n1_form: append("f2tn1t_%s_%s" % (f2_tag,n1_form))
      if n1_form: append("f1tn1t_%s_%s" % (f1_tag,n1_form))
      if f1_form: append("f1tf2t_%s_%s" % (f1_form,f2_tag))
      if p1_form: append("p1tf1t_%s_%s" % (p1_form,f1_tag))
      if p1_form: append("p1tf2t_%s_%s" % (p1_form,f2_tag))
      if f2_form: append("f2tn1t_%s_%s" % (f2_form,n1_tag))
      if f1_form: append("f1tn1t_%s_%s" % (f1_form,n1_tag))

      # bigram+left/right child

      append("f1tf2t_%s_%s_%s_%s" % (f1_tag,f2_tag,f1lc,f2lc))
      append("p1tf1t_%s_%s_%s_%s" % (p1_tag,f1_tag,p1lc,f1lc))
      append("p1tf2t_%s_%s_%s_%s" % (p1_tag,f2_tag,p1lc,f2lc))
      append("f2tn1t_%s_%s_%s_%s" % (f2_tag,n1_tag,f2lc,n1lc))
      append("f1tn1t_%s_%s_%s_%s" % (f1_tag,n1_tag,f1lc,n1lc))

      append("f1tf2t_%s_%s_%s_%s" % (f1_tag,f2_tag,f1lc,f2rc))
      append("p1tf1t_%s_%s_%s_%s" % (p1_tag,f1_tag,p1lc,f1rc))
      append("p1tf2t_%s_%s_%s_%s" % (p1_tag,f2_tag,p1lc,f2rc))
      append("f2tn1t_%s_%s_%s_%s" % (f2_tag,n1_tag,f2lc,n1rc))
      append("f1tn1t_%s_%s_%s_%s" % (f1_tag,n1_tag,f1lc,n1rc))

      append("f1tf2t_%s_%s_%s_%s" % (f1_tag,f2_tag,f1rc,f2lc))
      append("p1tf1t_%s_%s_%s_%s" % (p1_tag,f1_tag,p1rc,f1lc))
      append("p1tf2t_%s_%s_%s_%s" % (p1_tag,f2_tag,p1rc,f2lc))
      append("f2tn1t_%s_%s_%s_%s" % (f2_tag,n1_tag,f2rc,n1lc))
      append("f1tn1t_%s_%s_%s_%s" % (f1_tag,n1_tag,f1rc,n1lc))

      append("f1tf2t_%s_%s_%s_%s" % (f1_tag,f2_tag,f1rc,f2rc))
      append("p1tf1t_%s_%s_%s_%s" % (p1_tag,f1_tag,p1rc,f1rc))
      append("p1tf2t_%s_%s_%s_%s" % (p1_tag,f2_tag,p1rc,f2rc))
      append("f2tn1t_%s_%s_%s_%s" % (f2_tag,n1_tag,f2rc,n1rc))
      append("f1tn1t_%s_%s_%s_%s" % (f1_tag,n1_tag,f1rc,n1rc))

      #90.16 at 20, with these, big train set. (very similar w/o)
      IN = ['IN','PREPOSITION'] # Hebrew: try only here

      if f2['tag']  in  IN:
         append("PP1_%s_%s_%s" % (f1_form,f2_form,f2rc))
         append("PP2_%s_%s_%s" % (p1_form,f2_form,f2rc))
      if f1['tag']  in  IN:
         append("PP3_%s_%s_%s" % (p1_form,f1_form,f1rc))
      if n1['tag']  in  IN:
         append("PP4_%s_%s_%s" % (f2_form,n1_form,n1rc))
         append("PP5_%s_%s_%s" % (f1_form,n1_form,n1rc))

      if f2['tag']  in  IN:
         append("PP1_%s_%s_%s" % (f1_tag,f2_form,f2rc_form))
         append("PP2_%s_%s_%s" % (p1_tag,f2_form,f2rc_form))
      if f1['tag']  in  IN:
         append("PP3_%s_%s_%s" % (p1_tag,f1_form,f1rc_form))
      if n1['tag']  in  IN:
         append("PP4_%s_%s_%s" % (f2_tag,n1_form,n1rc_form))
         append("PP5_%s_%s_%s" % (f1_tag,n1_form,n1rc_form))

      return features
   #}}}

FeaturesExtractor = BaselineFeatureExtractor
print "loading features"
