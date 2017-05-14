from common import PAD,ROOT
## trying to add some SD specific features on top of the English ones

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


class BaselineFeatureExtractor: # {{{
   LANG='ENG'
   def __init__(self):
      self.versions = None
      self.vocab = set()

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
      #LANG = self.LANG
      CC = ['CC','CONJ']
      IN = ['IN']

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
      f1_ctag = f1['tag'] 
      f2_ctag = f2['tag'] 
      p1_ctag = p1['tag'] 
      n1_ctag = n1['tag'] 
      n2_ctag = n2['tag'] 
      p2_ctag = p2['tag'] 
      if f1_tag in IN: f1_tag = "%s_%s" % (f1_tag,f1_form)
      if f2_tag in IN: f2_tag = "%s_%s" % (f2_tag,f2_form)
      if p1_tag in IN: p1_tag = "%s_%s" % (p1_tag,p1_form)
      if p2_tag in IN: p2_tag = "%s_%s" % (p2_tag,p2_form)
      if n1_tag in IN: n1_tag = "%s_%s" % (n1_tag,n1_form)
      if n2_tag in IN: n2_tag = "%s_%s" % (n2_tag,n2_form)


      ## @@@ Hurts performance with small training set. benefit with large!
      if p2_tag in CC: p2_tag = "%s%s" % (p2_tag,p2_form)
      if n2_tag in CC: n2_tag = "%s%s" % (n2_tag,n2_form)
      ####

      left_child=deps.left_child
      f1lc = left_child(f1)
      if f1lc: f1lc=f1lc['tag']
      f2lc = left_child(f2)
      if f2lc: f2lc=f2lc['tag']
      n1lc = left_child(n1) 
      if n1lc: n1lc=n1lc['tag']
      n2lc = left_child(n2) 
      if n2lc: n2lc=n2lc['tag']
      p1lc = left_child(p1) 
      if p1lc: p1lc=p1lc['tag']
      p2lc = left_child(p2) 
      if p2lc: p2lc=p2lc['tag']

      ## TO-VERB (to keep, to go,...)
      if f1_tag[0]=='V' and f1lc=='TO': f1_tag="%s_TO" % f1_tag
      if f2_tag[0]=='V' and f2lc=='TO': f2_tag="%s_TO" % f2_tag
      if p1_tag[0]=='V' and p1lc=='TO': p1_tag="%s_TO" % p1_tag
      if p2_tag[0]=='V' and p2lc=='TO': p2_tag="%s_TO" % p2_tag
      if n1_tag[0]=='V' and n1lc=='TO': n1_tag="%s_TO" % n1_tag
      if n2_tag[0]=='V' and n2lc=='TO': n2_tag="%s_TO" % n2_tag

      f1rc_form=None
      right_child=deps.right_child
      f1rc = right_child(f1) 
      if f1rc: 
         f1rc_form=f1rc['form']
         f1rc=f1rc['tag']

      f2rc_form=None
      f2rc = right_child(f2) 
      if f2rc: 
         f2rc_form=f2rc['form']
         f2rc=f2rc['tag']

      n1rc_form=None
      n1rc = right_child(n1) 
      if n1rc: 
         n1rc_form=n1rc['form']
         n1rc=n1rc['tag']

      n2rc = right_child(n2) 
      if n2rc: n2rc=n2rc['tag']
      p1rc = right_child(p1) 
      if p1rc: p1rc=p1rc['tag']
      p2rc = right_child(p2) 
      if p2rc: p2rc=p2rc['tag']

      # this should help in cases of A CC B D, telling B not to B->D if CC is not built yet and in matching type
      # hope this helps (Many money managers and (some traders had already left))
      #if f1_tag in CC: f1_tag = "%s-%s-%s-%s" % (f1_form,f1_tag,f1lc,f1rc)
      #if f2_tag in CC: f2_tag = "%s-%s-%s-%s" % (f2_form,f2_tag,f2lc,f2rc)
      #if p1_tag in CC: p1_tag = "%s-%s-%s-%s" % (p1_form,p1_tag,p1lc,p1rc)
      #if n1_tag in CC: n1_tag = "%s-%s-%s-%s" % (n1_form,n1_tag,n1lc,n1rc)

      append = features.append

      # lengths
      f1id=f1['id']
      f2id=f2['id']
      n1id=n1['id']
      p1id=p1['id']
      n2id=n2['id']
      p2id=p2['id']
      append("lp1f1_%s" % (f1id-p1id))
      append("lf1f2_%s" % (f2id-f1id))
      append("lf2n1_%s" % (n1id-f2id))
      append("lp2p1_%s" % (p1id-p2id))
      append("ln1n2_%s" % (n2id-n1id))

      append("lp1f1_%s_%s_%s" % (f1id-p1id,f1_tag,p1_tag))
      append("lf1f2_%s_%s_%s" % (f2id-f1id,f2_tag,f1_tag))
      append("lf2n1_%s_%s_%s" % (n1id-f2id,n1_tag,f2_tag))
      append("lp2p1_%s_%s_%s" % (p1id-p2id,p1_tag,p2_tag))
      append("ln1n2_%s_%s_%s" % (n2id-n1id,n2_tag,n1_tag))
      

      # "am I a word or more?" features
      sf1 = left_child(f1)==None and right_child(f1)==None
      sf2 = left_child(f2)==None and right_child(f2)==None
      sp1 = left_child(p1)==None and right_child(p1)==None
      sp2 = left_child(p2)==None and right_child(p2)==None
      sn1 = left_child(n1)==None and right_child(n1)==None
      sn2 = left_child(n2)==None and right_child(n2)==None

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
      append("Af1tf2t_%s_%s_%s_%s" % (f1_tag,f2_tag,f1lc,f2lc))
      append("Ap1tf1t_%s_%s_%s_%s" % (p1_tag,f1_tag,p1lc,f1lc))
      append("Ap1tf2t_%s_%s_%s_%s" % (p1_tag,f2_tag,p1lc,f2lc))
      append("Af2tn1t_%s_%s_%s_%s" % (f2_tag,n1_tag,f2lc,n1lc))
      append("Af1tn1t_%s_%s_%s_%s" % (f1_tag,n1_tag,f1lc,n1lc))

      append("Bf1tf2t_%s_%s_%s_%s" % (f1_tag,f2_tag,f1lc,f2rc))
      append("Bp1tf1t_%s_%s_%s_%s" % (p1_tag,f1_tag,p1lc,f1rc))
      append("Bp1tf2t_%s_%s_%s_%s" % (p1_tag,f2_tag,p1lc,f2rc))
      append("Bf2tn1t_%s_%s_%s_%s" % (f2_tag,n1_tag,f2lc,n1rc))
      append("Bf1tn1t_%s_%s_%s_%s" % (f1_tag,n1_tag,f1lc,n1rc))

      append("Cf1tf2t_%s_%s_%s_%s" % (f1_tag,f2_tag,f1rc,f2lc))
      append("Cp1tf1t_%s_%s_%s_%s" % (p1_tag,f1_tag,p1rc,f1lc))
      append("Cp1tf2t_%s_%s_%s_%s" % (p1_tag,f2_tag,p1rc,f2lc))
      append("Cf2tn1t_%s_%s_%s_%s" % (f2_tag,n1_tag,f2rc,n1lc))
      append("Cf1tn1t_%s_%s_%s_%s" % (f1_tag,n1_tag,f1rc,n1lc))

      append("Df1tf2t_%s_%s_%s_%s" % (f1_tag,f2_tag,f1rc,f2rc))
      append("Dp1tf1t_%s_%s_%s_%s" % (p1_tag,f1_tag,p1rc,f1rc))
      append("Dp1tf2t_%s_%s_%s_%s" % (p1_tag,f2_tag,p1rc,f2rc))
      append("Df2tn1t_%s_%s_%s_%s" % (f2_tag,n1_tag,f2rc,n1rc))
      append("Df1tn1t_%s_%s_%s_%s" % (f1_tag,n1_tag,f1rc,n1rc))

      # only triples
      append("1rDf1tf2t_%s_%s_%s" % (f1_tag,f2_tag,f1rc))
      append("1rDp1tf1t_%s_%s_%s" % (p1_tag,f1_tag,p1rc))
      append("1rDp1tf2t_%s_%s_%s" % (p1_tag,f2_tag,p1rc))
      append("1rDf2tn1t_%s_%s_%s" % (f2_tag,n1_tag,f2rc))
      append("1rDf1tn1t_%s_%s_%s" % (f1_tag,n1_tag,f1rc))
      append("1lDf1tf2t_%s_%s_%s" % (f1_tag,f2_tag,f1lc))
      append("1lDp1tf1t_%s_%s_%s" % (p1_tag,f1_tag,p1lc))
      append("1lDp1tf2t_%s_%s_%s" % (p1_tag,f2_tag,p1lc))
      append("1lDf2tn1t_%s_%s_%s" % (f2_tag,n1_tag,f2lc))
      append("1lDf1tn1t_%s_%s_%s" % (f1_tag,n1_tag,f1lc))
      # 
      append("2rDf1tf2t_%s_%s_%s" % (f1_tag,f2_tag,f2rc))
      append("2rDp1tf1t_%s_%s_%s" % (p1_tag,f1_tag,f1rc))
      append("2rDp1tf2t_%s_%s_%s" % (p1_tag,f2_tag,f2rc))
      append("2rDf2tn1t_%s_%s_%s" % (f2_tag,n1_tag,n1rc))
      append("2rDf1tn1t_%s_%s_%s" % (f1_tag,n1_tag,n1rc))
      append("2lDf1tf2t_%s_%s_%s" % (f1_tag,f2_tag,f2lc))
      append("2lDp1tf1t_%s_%s_%s" % (p1_tag,f1_tag,f1lc))
      append("2lDp1tf2t_%s_%s_%s" % (p1_tag,f2_tag,f2lc))
      append("2lDf2tn1t_%s_%s_%s" % (f2_tag,n1_tag,n1lc))
      append("2lDf1tn1t_%s_%s_%s" % (f1_tag,n1_tag,n1lc))

      # 4gram tags
      append("A1_%s_%s_%s"    % (       f2_tag,f2rc,n1_tag))  # not described
      append("A2_%s_%s_%s_%s" % (f1_tag,f2_tag,f2rc,n1_tag))

      append("A3_%s_%s_%s"    % (f1_tag       ,f1lc,p1_tag)) # not described
      append("A4_%s_%s_%s_%s"    % (f1_tag,f2_tag,f1lc,p1_tag))

      append("A5_%s_%s_%s_%s"    % (f2_tag,f2rc,n1_tag,n2_tag))
      append("A6_%s_%s_%s_%s"    % (f1_tag,f1lc,p1_tag,p2_tag))

      # 5gram tags
      append("A7_%s_%s_%s_%s"    % (p1_tag,f1_tag,f2_tag,n1_tag))

      append("A8_%s_%s_%s_%s_%s"    % (f1_tag,f2_tag,f2rc,n1_tag,n2_tag))
      append("A9_%s_%s_%s_%s_%s"    % (f2_tag,f1_tag,f1lc,p1_tag,p2_tag))


      ## SD conjunctions 
      ##
      ## f1 CC n1
      ##
      ## should I connect f1 as parent of CC?
      if f2_ctag in CC:
         append("conj1_%s_%s_%s" % (f2_form, f1_tag, n1_tag))
         append("conj2_%s_%s_%s" % (f2_form, f1_ctag, n1_ctag))
         append("conj3_%s_%s" % (f2_form, f1_ctag==n1_ctag))
      ## f1_CC f2  -- should I connect f1 as parent of f2?
      if f1rc and f1rc.split("_")[0] in CC:
         append("Cconj1_%s_%s" % (f1_tag, f2_tag))
         append("Cconj2_%s_%s_%s" % (f1_tag, f1rc, f2_tag))
         append("Cconj3_%s_%s_%s_%s" % (f1_tag, f1rc, f2_tag, f2lc))
         append("Cconj4_%s_%s_%s_%s" % (f1_tag, f1rc, f2_tag, f2rc))
         append("Cconj5_%s_%s_%s_%s_%s" % (f1_tag, f1rc, f2_tag, f2lc, f2rc))
         append("Cconj6_%s_%s" % (f1rc, f1_tag==f2_tag))
         append("Cconj7_%s_%s" % (f1rc, f1_tag[0]==f2_tag[0]))


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

      for (fst,snd,typ) in [(f1,f2,"f1f2")]: #,(f1,n1,"f1n1"),(p1,f2,"p1f2")]: # the last two are too much
         if fst is PAD or snd is PAD: continue
         f=sent.index(fst)
         t=sent.index(snd)
         fstt=fst['tag']
         sndt=snd['tag']
         lo1 = sent[f-1] if f>0 else PAD
         ro1 = sent[f+1] if f+1<len(sent) else PAD
         lo2 = sent[t-1] if t>0 else PAD
         ro2 = sent[t+1] if t+1<len(sent) else PAD
         append("%s_ngbrs1_%s_%s_%s" % (typ,lo1['tag'],fstt,sndt))
         append("%s_ngbrs1_%s_%s_%s_%s" % (typ,lo1['tag'],fstt,sndt,ro2['tag']))
         append("%s_ngbrs2_%s_%s_%s" % (typ,lo1['tag'],sndt,ro2['tag']))
         append("%s_ngbrs3_%s_%s_%s" % (typ,lo1['tag'],fstt,ro2['tag']))
         append("%s_ngbrs4_%s_%s_%s" % (typ,fstt,sndt,ro2['tag']))

         append("%s_Angbrs1_%s_%s_%s" % (typ,ro1['tag'],fstt,lo2['tag']))
         append("%s_Angbrs1_%s_%s_%s_%s" % (typ,ro1['tag'],fstt,lo2['tag'],sndt))
         append("%s_Angbrs2_%s_%s_%s" % (typ,fstt,ro1['tag'],sndt))
         append("%s_Angbrs3_%s_%s_%s" % (typ,fstt,lo2['tag'],sndt))
         append("%s_Angbrs4_%s_%s_%s" % (typ,ro1['tag'],lo2['tag'],sndt))

         append("%s_Bngbrs1_%s_%s_%s_%s" % (typ,lo1['tag'],fstt,lo2['tag'],sndt))
         append("%s_Bngbrs2_%s_%s_%s_%s" % (typ,fstt,ro1['tag'],sndt,ro2['tag']))

      return features
   #}}}

FeaturesExtractor = BaselineFeatureExtractor
