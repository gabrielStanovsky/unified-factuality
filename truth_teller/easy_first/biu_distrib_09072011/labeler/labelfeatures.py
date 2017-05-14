
class AnEdgeLabelPlusSuffixesFeatureExtractor: #{{{
   '''
   like AnEdgeLabelFeatureExtractor, but look for -ing and -ly
   '''
   def __init__(self):
      pass
   def extract(self,child,parent,sent,deps=None,par=None,prel=None):
      fs = []
      F = fs.append

      ctag = child['tag']
      cform = child['form']
      ptag = parent['tag']
      pform = parent['form']

      cid = child['id']
      pid = parent['id']
      slen = len(sent)

      cm1 = sent[cid-1] if cid > 0        else None
      cm2 = sent[cid-2] if cid > 1        else None
      cp1 = sent[cid+1] if cid < slen-1   else None
      cp2 = sent[cid+2] if cid < slen-2   else None
      pm1 = sent[pid-1] if pid > 0        else None
      pm2 = sent[pid-2] if pid > 1        else None
      pp1 = sent[pid+1] if pid < slen-1   else None
      pp2 = sent[pid+2] if pid < slen-2   else None

      # standard word/pos features
      F("ct_%s" % ctag)
      F("pt_%s" % ptag)
      F("cf_%s" % cform)
      if cform.endswith("ing"): F("cf_-ing")
      F("pf_%s" % pform)
      if pform.endswith("ing"): F("pf_-ing")
      F("ptct_%s_%s" % (ptag,ctag))
      F("pfcf_%s_%s" % (pform,cform))
      F("pfct_%s_%s" % (pform,ctag))
      if pform.endswith("ing"): F("pfct_-ing_%s" % ctag)
      F("ptcf_%s_%s" % (ptag,cform))
      if cform.endswith("ing"): F("cfpt_-ing_%s" % ptag)

      if cm1:
         F("cm1p_%s"       %  (cm1['tag']))
         F("cm1p_pc_%s_%s" %  (cm1['tag'],ctag))
         F("cm1f_%s"       %  (cm1['form']))

      if cm2:
         F("cm2p_%s"       %  (cm2['tag']))
         F("cm2p_pc_%s_%s" %  (cm2['tag'],ctag))
         F("cm2f_%s"       %  (cm2['form']))
         F("cm2p_cm1p_%s_%s" % (cm2['tag'],cm1['tag'])) #??

      if cp1:
         F("cp1p_%s"       %  (cp1['tag']))
         F("cp1p_pc_%s_%s" %  (cp1['tag'],ctag))
         F("cp1f_%s"       %  (cp1['form']))

      if cp2:
         F("cp2p_%s"       %  (cp2['tag']))
         F("cp2p_pc_%s_%s" %  (cp2['tag'],ctag))
         F("cp2f_%s"       %  (cp2['form']))
         F("cp2p_cp1p_%s_%s" % (cp2['tag'],cp1['tag'])) #??

      if cm1 and cp1:
         F("cm1t_ct_cp1t_%s_%s_%s" % (cm1['tag'],ctag,cp1['tag']))

      if pm1:
         F("pm1p_%s"       %  (pm1['tag']))
         F("pm1p_pp_%s_%s" %  (pm1['tag'],ptag))
         F("pm1f_%s"       %  (pm1['form']))

      if pm2:
         F("pm2p_%s"       %  (pm2['tag']))
         F("pm2p_pp_%s_%s" %  (pm2['tag'],ptag))
         F("pm2f_%s"       %  (pm2['form']))

      if pp2:
         F("pp1p_%s"       %  (pp1['tag']))
         F("pp1p_pp_%s_%s" %  (pp1['tag'],ptag))
         F("pp1f_%s"       %  (pp1['form']))

      if pp2:
         F("pp2p_%s"       %  (pp2['tag']))
         F("pp2p_pp_%s_%s" %  (pp2['tag'],ptag))
         F("pp2f_%s"       %  (pp2['form']))
     
      if pm1 and pp1:
         F("pm1t_ct_pp1t_%s_%s_%s" % (pm1['tag'],ptag,pp1['tag']))

      # POS in between
      for mid in sent[min(cid,pid)+1:max(cid,pid)]:
         mtag = mid['tag']
         F("ct_pt_mt_%s_%s_%s"   % (ctag,mtag,ptag))
         F("ct_mt_%s_%s"         % (ctag,mtag))
         F("mt_pt_%s_%s"         % (mtag,ptag))
         F("mt_%s"               % (mtag))

      # conjoin everything with direction
      dr = "_L" if child['id']>parent['id'] else "_R"
      dfs = ["%s%s" % (f,dr) for f in fs]

      # add only direction
      fs.append(dr)

      return fs + dfs
#}}}

class AnEdgeLabelFeatureExtractor: #{{{
   def __init__(self):
      pass
   def extract(self,child,parent,sent,deps=None,par=None,prel=None):
      fs = []
      F = fs.append

      ctag = child['tag']
      cform = child['form']
      ptag = parent['tag']
      pform = parent['form']

      cid = child['id']
      pid = parent['id']
      slen = len(sent)

      cm1 = sent[cid-1] if cid > 0        else None
      cm2 = sent[cid-2] if cid > 1        else None
      cp1 = sent[cid+1] if cid < slen-1   else None
      cp2 = sent[cid+2] if cid < slen-2   else None
      pm1 = sent[pid-1] if pid > 0        else None
      pm2 = sent[pid-2] if pid > 1        else None
      pp1 = sent[pid+1] if pid < slen-1   else None
      pp2 = sent[pid+2] if pid < slen-2   else None

      # standard word/pos features
      F("ct_%s" % ctag)
      F("pt_%s" % ptag)
      F("cf_%s" % cform)
      F("pf_%s" % pform)
      F("ptct_%s_%s" % (ptag,ctag))
      F("pfcf_%s_%s" % (pform,cform))
      F("pfct_%s_%s" % (pform,ctag))
      F("ptcf_%s_%s" % (ptag,cform))

      if cm1:
         F("cm1p_%s"       %  (cm1['tag']))
         F("cm1p_pc_%s_%s" %  (cm1['tag'],ctag))
         F("cm1f_%s"       %  (cm1['form']))

      if cm2:
         F("cm2p_%s"       %  (cm2['tag']))
         F("cm2p_pc_%s_%s" %  (cm2['tag'],ctag))
         F("cm2f_%s"       %  (cm2['form']))
         #F("cm2p_cm1p_%s_%s" % (cm2['tag'],cm1['tag'])) ??

      if cp1:
         F("cp1p_%s"       %  (cp1['tag']))
         F("cp1p_pc_%s_%s" %  (cp1['tag'],ctag))
         F("cp1f_%s"       %  (cp1['form']))

      if cp2:
         F("cp2p_%s"       %  (cp2['tag']))
         F("cp2p_pc_%s_%s" %  (cp2['tag'],ctag))
         F("cp2f_%s"       %  (cp2['form']))
         #F("cp2p_cp1p_%s_%s" % (cp2['tag'],cp1['tag'])) ??

      if cm1 and cp1:
         F("cm1t_ct_cp1t_%s_%s_%s" % (cm1['tag'],ctag,cp1['tag']))

      if pm1:
         F("pm1p_%s"       %  (pm1['tag']))
         F("pm1p_pp_%s_%s" %  (pm1['tag'],ptag))
         F("pm1f_%s"       %  (pm1['form']))

      if pm2:
         F("pm2p_%s"       %  (pm2['tag']))
         F("pm2p_pp_%s_%s" %  (pm2['tag'],ptag))
         F("pm2f_%s"       %  (pm2['form']))

      if pp2:
         F("pp1p_%s"       %  (pp1['tag']))
         F("pp1p_pp_%s_%s" %  (pp1['tag'],ptag))
         F("pp1f_%s"       %  (pp1['form']))

      if pp2:
         F("pp2p_%s"       %  (pp2['tag']))
         F("pp2p_pp_%s_%s" %  (pp2['tag'],ptag))
         F("pp2f_%s"       %  (pp2['form']))
     
      if pm1 and pp1:
         F("pm1t_ct_pp1t_%s_%s_%s" % (pm1['tag'],ptag,pp1['tag']))

      # POS in between
      for mid in sent[min(cid,pid)+1:max(cid,pid)]:
         mtag = mid['tag']
         F("ct_pt_mt_%s_%s_%s"   % (ctag,mtag,ptag))
         F("ct_mt_%s_%s"         % (ctag,mtag))
         F("mt_pt_%s_%s"         % (mtag,ptag))
         F("mt_%s"               % (mtag))

      # conjoin everything with direction
      dr = "_L" if child['id']>parent['id'] else "_R"
      dfs = ["%s%s" % (f,dr) for f in fs]

      # add only direction
      fs.append(dr)

      return fs + dfs
#}}}

class AnEdgeLabelFeatureExtractor2: #{{{
   '''
   Try looking at children of child
   '''
   def __init__(self):
      pass
   def extract(self,child,parent,sent,deps=None,par='parent',prel='prel'):
      fs = []
      F = fs.append

      ctag = child['tag']
      cform = child['form']
      ptag = parent['tag']
      pform = parent['form']

      cid = child['id']
      pid = parent['id']
      slen = len(sent)

      siblings = [t for t in sent if t[par]==pid and t['id']!=cid]

      cm1 = sent[cid-1] if cid > 0        else None
      cm2 = sent[cid-2] if cid > 1        else None
      cp1 = sent[cid+1] if cid < slen-1   else None
      cp2 = sent[cid+2] if cid < slen-2   else None
      pm1 = sent[pid-1] if pid > 0        else None
      pm2 = sent[pid-2] if pid > 1        else None
      pp1 = sent[pid+1] if pid < slen-1   else None
      pp2 = sent[pid+2] if pid < slen-2   else None

      # standard word/pos features
      F("ct_%s" % ctag)
      F("pt_%s" % ptag)
      F("cf_%s" % cform)
      F("pf_%s" % pform)
      F("ptct_%s_%s" % (ptag,ctag))
      F("pfcf_%s_%s" % (pform,cform))
      F("pfct_%s_%s" % (pform,ctag))
      F("ptcf_%s_%s" % (ptag,cform))

      for sib in siblings:
         F("sp_%s"       %  (sib['tag']))
         F("sp_pc_%s_%s" %  (sib['tag'],ctag))
         F("sp_pp_%s_%s" %  (sib['tag'],ptag))
         F("sf_%s"       %  (sib['form']))
      if not siblings:
         F("nosib_cp_%s" % ctag)
         F("nosib_pp_%s" % ptag)
      # TODO: look at children of child and parent of parent?

      if cm1:
         F("cm1p_%s"       %  (cm1['tag']))
         F("cm1p_pc_%s_%s" %  (cm1['tag'],ctag))
         F("cm1f_%s"       %  (cm1['form']))

      if cm2:
         F("cm2p_%s"       %  (cm2['tag']))
         F("cm2p_pc_%s_%s" %  (cm2['tag'],ctag))
         F("cm2f_%s"       %  (cm2['form']))
         #F("cm2p_cm1p_%s_%s" % (cm2['tag'],cm1['tag'])) ??

      if cp1:
         F("cp1p_%s"       %  (cp1['tag']))
         F("cp1p_pc_%s_%s" %  (cp1['tag'],ctag))
         F("cp1f_%s"       %  (cp1['form']))

      if cp2:
         F("cp2p_%s"       %  (cp2['tag']))
         F("cp2p_pc_%s_%s" %  (cp2['tag'],ctag))
         F("cp2f_%s"       %  (cp2['form']))
         #F("cp2p_cp1p_%s_%s" % (cp2['tag'],cp1['tag'])) ??

      if cm1 and cp1:
         F("cm1t_ct_cp1t_%s_%s_%s" % (cm1['tag'],ctag,cp1['tag']))

      if pm1:
         F("pm1p_%s"       %  (pm1['tag']))
         F("pm1p_pp_%s_%s" %  (pm1['tag'],ptag))
         F("pm1f_%s"       %  (pm1['form']))

      if pm2:
         F("pm2p_%s"       %  (pm2['tag']))
         F("pm2p_pp_%s_%s" %  (pm2['tag'],ptag))
         F("pm2f_%s"       %  (pm2['form']))

      if pp2:
         F("pp1p_%s"       %  (pp1['tag']))
         F("pp1p_pp_%s_%s" %  (pp1['tag'],ptag))
         F("pp1f_%s"       %  (pp1['form']))

      if pp2:
         F("pp2p_%s"       %  (pp2['tag']))
         F("pp2p_pp_%s_%s" %  (pp2['tag'],ptag))
         F("pp2f_%s"       %  (pp2['form']))
     
      if pm1 and pp1:
         F("pm1t_ct_pp1t_%s_%s_%s" % (pm1['tag'],ptag,pp1['tag']))

      # POS in between
      for mid in sent[min(cid,pid)+1:max(cid,pid)]:
         mtag = mid['tag']
         F("ct_pt_mt_%s_%s_%s"   % (ctag,mtag,ptag))
         F("ct_mt_%s_%s"         % (ctag,mtag))
         F("mt_pt_%s_%s"         % (mtag,ptag))
         F("mt_%s"               % (mtag))

      # conjoin everything with direction
      dr = "_L" if child['id']>parent['id'] else "_R"
      dfs = ["%s%s" % (f,dr) for f in fs]

      # add only direction
      fs.append(dr)

      return fs + dfs
#}}}

class AnEdgeLabelFeatureExtractor3: #{{{
   '''
   Try looking at children of child
   '''
   def __init__(self):
      pass
   def extract(self,child,parent,sent,deps=None,par='parent',prel='prel'):
      fs = []
      F = fs.append

      ctag = child['tag']
      cform = child['form']
      ptag = parent['tag']
      pform = parent['form']

      cid = child['id']
      pid = parent['id']
      slen = len(sent)

      siblings = [t for t in sent if t[par]==pid and t['id']!=cid]
      grandchl = [t for t in sent if t[par]==cid]
      parpar   = sent[parent[par]] if pid != 0 else None

      cm1 = sent[cid-1] if cid > 0        else None
      cm2 = sent[cid-2] if cid > 1        else None
      cp1 = sent[cid+1] if cid < slen-1   else None
      cp2 = sent[cid+2] if cid < slen-2   else None
      pm1 = sent[pid-1] if pid > 0        else None
      pm2 = sent[pid-2] if pid > 1        else None
      pp1 = sent[pid+1] if pid < slen-1   else None
      pp2 = sent[pid+2] if pid < slen-2   else None

      # standard word/pos features
      F("ct_%s" % ctag)
      F("pt_%s" % ptag)
      F("cf_%s" % cform)
      F("pf_%s" % pform)
      F("ptct_%s_%s" % (ptag,ctag))
      F("pfcf_%s_%s" % (pform,cform))
      F("pfct_%s_%s" % (pform,ctag))
      F("ptcf_%s_%s" % (ptag,cform))

      for sib in siblings:
         F("sp_%s"       %  (sib['tag']))
         F("sp_pc_%s_%s" %  (sib['tag'],ctag))
         F("sp_pp_%s_%s" %  (sib['tag'],ptag))
         F("sf_%s"       %  (sib['form']))
      if not siblings:
         F("nosib_cp_%s" % ctag)
         F("nosib_pp_%s" % ptag)
      # TODO: look at children of child and parent of parent?
      for grn in grandchl:
         F("gp_%s"       %  (grn['tag']))
         F("gp_pc_%s_%s" %  (grn['tag'],ctag))
         F("gp_pp_%s_%s" %  (grn['tag'],ptag))
         F("gf_%s"       %  (grn['form']))
      if parpar:
         F("prpr_%s"       %  (parpar['tag']))
         F("prpr_pc_%s_%s" %  (parpar['tag'],ctag))
         F("prpr_pp_%s_%s" %  (parpar['tag'],ptag))
         F("prpr_%s"       %  (parpar['form']))

      if cm1:
         F("cm1p_%s"       %  (cm1['tag']))
         F("cm1p_pc_%s_%s" %  (cm1['tag'],ctag))
         F("cm1f_%s"       %  (cm1['form']))

      if cm2:
         F("cm2p_%s"       %  (cm2['tag']))
         F("cm2p_pc_%s_%s" %  (cm2['tag'],ctag))
         F("cm2f_%s"       %  (cm2['form']))
         #F("cm2p_cm1p_%s_%s" % (cm2['tag'],cm1['tag'])) ??

      if cp1:
         F("cp1p_%s"       %  (cp1['tag']))
         F("cp1p_pc_%s_%s" %  (cp1['tag'],ctag))
         F("cp1f_%s"       %  (cp1['form']))

      if cp2:
         F("cp2p_%s"       %  (cp2['tag']))
         F("cp2p_pc_%s_%s" %  (cp2['tag'],ctag))
         F("cp2f_%s"       %  (cp2['form']))
         #F("cp2p_cp1p_%s_%s" % (cp2['tag'],cp1['tag'])) ??

      if cm1 and cp1:
         F("cm1t_ct_cp1t_%s_%s_%s" % (cm1['tag'],ctag,cp1['tag']))

      if pm1:
         F("pm1p_%s"       %  (pm1['tag']))
         F("pm1p_pp_%s_%s" %  (pm1['tag'],ptag))
         F("pm1f_%s"       %  (pm1['form']))

      if pm2:
         F("pm2p_%s"       %  (pm2['tag']))
         F("pm2p_pp_%s_%s" %  (pm2['tag'],ptag))
         F("pm2f_%s"       %  (pm2['form']))

      if pp2:
         F("pp1p_%s"       %  (pp1['tag']))
         F("pp1p_pp_%s_%s" %  (pp1['tag'],ptag))
         F("pp1f_%s"       %  (pp1['form']))

      if pp2:
         F("pp2p_%s"       %  (pp2['tag']))
         F("pp2p_pp_%s_%s" %  (pp2['tag'],ptag))
         F("pp2f_%s"       %  (pp2['form']))
     
      if pm1 and pp1:
         F("pm1t_ct_pp1t_%s_%s_%s" % (pm1['tag'],ptag,pp1['tag']))

      # POS in between
      for mid in sent[min(cid,pid)+1:max(cid,pid)]:
         mtag = mid['tag']
         F("ct_pt_mt_%s_%s_%s"   % (ctag,mtag,ptag))
         F("ct_mt_%s_%s"         % (ctag,mtag))
         F("mt_pt_%s_%s"         % (mtag,ptag))
         F("mt_%s"               % (mtag))

      # conjoin everything with direction
      dr = "_L" if child['id']>parent['id'] else "_R"
      dfs = ["%s%s" % (f,dr) for f in fs]

      # add only direction
      fs.append(dr)

      return fs + dfs
#}}}

class AnEdgeLabelFeatureExtractor4: #{{{
   '''
   Try looking at children of child
   '''
   def __init__(self):
      pass
   def extract(self,child,parent,sent,deps=None,par='parent',prel='prel'):
      fs = []
      F = fs.append

      ctag = child['tag']
      cform = child['form']
      ptag = parent['tag']
      pform = parent['form']

      cid = child['id']
      pid = parent['id']
      slen = len(sent)

      #siblings = [t for t in sent if t[par]==pid and t['id']!=cid]
      grandchl = [t for t in sent if t[par]==cid]
      #parpar   = sent[parent[par]] if pid != 0 else None

      cm1 = sent[cid-1] if cid > 0        else None
      cm2 = sent[cid-2] if cid > 1        else None
      cp1 = sent[cid+1] if cid < slen-1   else None
      cp2 = sent[cid+2] if cid < slen-2   else None
      pm1 = sent[pid-1] if pid > 0        else None
      pm2 = sent[pid-2] if pid > 1        else None
      pp1 = sent[pid+1] if pid < slen-1   else None
      pp2 = sent[pid+2] if pid < slen-2   else None

      # standard word/pos features
      F("ct_%s" % ctag)
      F("pt_%s" % ptag)
      F("cf_%s" % cform)
      F("pf_%s" % pform)
      F("ptct_%s_%s" % (ptag,ctag))
      F("pfcf_%s_%s" % (pform,cform))
      F("pfct_%s_%s" % (pform,ctag))
      F("ptcf_%s_%s" % (ptag,cform))

      #for sib in siblings:
      #   F("sp_%s"       %  (sib['tag']))
      #   F("sp_pc_%s_%s" %  (sib['tag'],ctag))
      #   F("sp_pp_%s_%s" %  (sib['tag'],ptag))
      #   F("sf_%s"       %  (sib['form']))
      #if not siblings:
      #   F("nosib_cp_%s" % ctag)
      #   F("nosib_pp_%s" % ptag)
      # TODO: look at children of child and parent of parent?
      for grn in grandchl:
         F("gp_%s"       %  (grn['tag']))
         F("gp_pc_%s_%s" %  (grn['tag'],ctag))
         F("gp_pp_%s_%s" %  (grn['tag'],ptag))
         F("gf_%s"       %  (grn['form']))
      #if parpar:
      #   F("prpr_%s"       %  (parpar['tag']))
      #   F("prpr_pc_%s_%s" %  (parpar['tag'],ctag))
      #   F("prpr_pp_%s_%s" %  (parpar['tag'],ptag))
      #   F("prpr_%s"       %  (parpar['form']))

      if cm1:
         F("cm1p_%s"       %  (cm1['tag']))
         F("cm1p_pc_%s_%s" %  (cm1['tag'],ctag))
         F("cm1f_%s"       %  (cm1['form']))

      if cm2:
         F("cm2p_%s"       %  (cm2['tag']))
         F("cm2p_pc_%s_%s" %  (cm2['tag'],ctag))
         F("cm2f_%s"       %  (cm2['form']))
         #F("cm2p_cm1p_%s_%s" % (cm2['tag'],cm1['tag'])) ??

      if cp1:
         F("cp1p_%s"       %  (cp1['tag']))
         F("cp1p_pc_%s_%s" %  (cp1['tag'],ctag))
         F("cp1f_%s"       %  (cp1['form']))

      if cp2:
         F("cp2p_%s"       %  (cp2['tag']))
         F("cp2p_pc_%s_%s" %  (cp2['tag'],ctag))
         F("cp2f_%s"       %  (cp2['form']))
         #F("cp2p_cp1p_%s_%s" % (cp2['tag'],cp1['tag'])) ??

      if cm1 and cp1:
         F("cm1t_ct_cp1t_%s_%s_%s" % (cm1['tag'],ctag,cp1['tag']))

      if pm1:
         F("pm1p_%s"       %  (pm1['tag']))
         F("pm1p_pp_%s_%s" %  (pm1['tag'],ptag))
         F("pm1f_%s"       %  (pm1['form']))

      if pm2:
         F("pm2p_%s"       %  (pm2['tag']))
         F("pm2p_pp_%s_%s" %  (pm2['tag'],ptag))
         F("pm2f_%s"       %  (pm2['form']))

      if pp2:
         F("pp1p_%s"       %  (pp1['tag']))
         F("pp1p_pp_%s_%s" %  (pp1['tag'],ptag))
         F("pp1f_%s"       %  (pp1['form']))

      if pp2:
         F("pp2p_%s"       %  (pp2['tag']))
         F("pp2p_pp_%s_%s" %  (pp2['tag'],ptag))
         F("pp2f_%s"       %  (pp2['form']))
     
      if pm1 and pp1:
         F("pm1t_ct_pp1t_%s_%s_%s" % (pm1['tag'],ptag,pp1['tag']))

      # POS in between
      for mid in sent[min(cid,pid)+1:max(cid,pid)]:
         mtag = mid['tag']
         F("ct_pt_mt_%s_%s_%s"   % (ctag,mtag,ptag))
         F("ct_mt_%s_%s"         % (ctag,mtag))
         F("mt_pt_%s_%s"         % (mtag,ptag))
         F("mt_%s"               % (mtag))

      # conjoin everything with direction
      dr = "_L" if child['id']>parent['id'] else "_R"
      dfs = ["%s%s" % (f,dr) for f in fs]

      # add only direction
      fs.append(dr)

      return fs + dfs
#}}}

class AnEdgeLabelFeatureExtractor5: #{{{
   '''
   Try looking at children of child
   '''
   def __init__(self):
      pass
   def extract(self,child,parent,sent,deps=None,par='parent',prel='prel'):
      fs = []
      F = fs.append

      ctag = child['tag']
      cform = child['form']
      ptag = parent['tag']
      pform = parent['form']

      cid = child['id']
      pid = parent['id']
      slen = len(sent)

      #siblings = [t for t in sent if t[par]==pid and t['id']!=cid]
      #grandchl = [t for t in sent if t[par]==cid]
      parpar   = sent[parent[par]] if pid != 0 else None

      cm1 = sent[cid-1] if cid > 0        else None
      cm2 = sent[cid-2] if cid > 1        else None
      cp1 = sent[cid+1] if cid < slen-1   else None
      cp2 = sent[cid+2] if cid < slen-2   else None
      pm1 = sent[pid-1] if pid > 0        else None
      pm2 = sent[pid-2] if pid > 1        else None
      pp1 = sent[pid+1] if pid < slen-1   else None
      pp2 = sent[pid+2] if pid < slen-2   else None

      # standard word/pos features
      F("ct_%s" % ctag)
      F("pt_%s" % ptag)
      F("cf_%s" % cform)
      F("pf_%s" % pform)
      F("ptct_%s_%s" % (ptag,ctag))
      F("pfcf_%s_%s" % (pform,cform))
      F("pfct_%s_%s" % (pform,ctag))
      F("ptcf_%s_%s" % (ptag,cform))

      #for sib in siblings:
      #   F("sp_%s"       %  (sib['tag']))
      #   F("sp_pc_%s_%s" %  (sib['tag'],ctag))
      #   F("sp_pp_%s_%s" %  (sib['tag'],ptag))
      #   F("sf_%s"       %  (sib['form']))
      #if not siblings:
      #   F("nosib_cp_%s" % ctag)
      #   F("nosib_pp_%s" % ptag)
      # TODO: look at children of child and parent of parent?
      #for grn in grandchl:
      #   F("gp_%s"       %  (grn['tag']))
      #   F("gp_pc_%s_%s" %  (grn['tag'],ctag))
      #   F("gp_pp_%s_%s" %  (grn['tag'],ptag))
      #   F("gf_%s"       %  (grn['form']))
      if parpar:
         F("prpr_%s"       %  (parpar['tag']))
         F("prpr_pc_%s_%s" %  (parpar['tag'],ctag))
         F("prpr_pp_%s_%s" %  (parpar['tag'],ptag))
         F("prpr_%s"       %  (parpar['form']))

      if cm1:
         F("cm1p_%s"       %  (cm1['tag']))
         F("cm1p_pc_%s_%s" %  (cm1['tag'],ctag))
         F("cm1f_%s"       %  (cm1['form']))

      if cm2:
         F("cm2p_%s"       %  (cm2['tag']))
         F("cm2p_pc_%s_%s" %  (cm2['tag'],ctag))
         F("cm2f_%s"       %  (cm2['form']))
         #F("cm2p_cm1p_%s_%s" % (cm2['tag'],cm1['tag'])) ??

      if cp1:
         F("cp1p_%s"       %  (cp1['tag']))
         F("cp1p_pc_%s_%s" %  (cp1['tag'],ctag))
         F("cp1f_%s"       %  (cp1['form']))

      if cp2:
         F("cp2p_%s"       %  (cp2['tag']))
         F("cp2p_pc_%s_%s" %  (cp2['tag'],ctag))
         F("cp2f_%s"       %  (cp2['form']))
         #F("cp2p_cp1p_%s_%s" % (cp2['tag'],cp1['tag'])) ??

      if cm1 and cp1:
         F("cm1t_ct_cp1t_%s_%s_%s" % (cm1['tag'],ctag,cp1['tag']))

      if pm1:
         F("pm1p_%s"       %  (pm1['tag']))
         F("pm1p_pp_%s_%s" %  (pm1['tag'],ptag))
         F("pm1f_%s"       %  (pm1['form']))

      if pm2:
         F("pm2p_%s"       %  (pm2['tag']))
         F("pm2p_pp_%s_%s" %  (pm2['tag'],ptag))
         F("pm2f_%s"       %  (pm2['form']))

      if pp2:
         F("pp1p_%s"       %  (pp1['tag']))
         F("pp1p_pp_%s_%s" %  (pp1['tag'],ptag))
         F("pp1f_%s"       %  (pp1['form']))

      if pp2:
         F("pp2p_%s"       %  (pp2['tag']))
         F("pp2p_pp_%s_%s" %  (pp2['tag'],ptag))
         F("pp2f_%s"       %  (pp2['form']))
     
      if pm1 and pp1:
         F("pm1t_ct_pp1t_%s_%s_%s" % (pm1['tag'],ptag,pp1['tag']))

      # POS in between
      for mid in sent[min(cid,pid)+1:max(cid,pid)]:
         mtag = mid['tag']
         F("ct_pt_mt_%s_%s_%s"   % (ctag,mtag,ptag))
         F("ct_mt_%s_%s"         % (ctag,mtag))
         F("mt_pt_%s_%s"         % (mtag,ptag))
         F("mt_%s"               % (mtag))

      # conjoin everything with direction
      dr = "_L" if child['id']>parent['id'] else "_R"
      dfs = ["%s%s" % (f,dr) for f in fs]

      # add only direction
      fs.append(dr)

      return fs + dfs
#}}}

class AnEdgeLabelFeatureExtractor6: #{{{
   '''
   Try looking at children of child
   '''
   def __init__(self):
      pass

   def extract(self,child,parent,sent,deps=None,par='parent',prel='prel'):
      fs = []
      F = fs.append

      ctag = child['tag']
      cform = child['form']
      ptag = parent['tag']
      pform = parent['form']

      cid = child['id']
      pid = parent['id']
      slen = len(sent)

      siblings = [t for t in sent if t[par]==pid and t['id']!=cid]
      grandchl = [t for t in sent if t[par]==cid]
      #parpar   = sent[parent[par]] if pid != 0 else None

      cm1 = sent[cid-1] if cid > 0        else None
      cm2 = sent[cid-2] if cid > 1        else None
      cp1 = sent[cid+1] if cid < slen-1   else None
      cp2 = sent[cid+2] if cid < slen-2   else None
      pm1 = sent[pid-1] if pid > 0        else None
      pm2 = sent[pid-2] if pid > 1        else None
      pp1 = sent[pid+1] if pid < slen-1   else None
      pp2 = sent[pid+2] if pid < slen-2   else None

      # standard word/pos features
      F("ct_%s" % ctag)
      F("pt_%s" % ptag)
      F("cf_%s" % cform)
      F("pf_%s" % pform)
      F("ptct_%s_%s" % (ptag,ctag))
      F("pfcf_%s_%s" % (pform,cform))
      F("pfct_%s_%s" % (pform,ctag))
      F("ptcf_%s_%s" % (ptag,cform))

      for sib in siblings:
         F("sp_%s"       %  (sib['tag']))
         F("sp_pc_%s_%s" %  (sib['tag'],ctag))
         F("sp_pp_%s_%s" %  (sib['tag'],ptag))
         F("sf_%s"       %  (sib['form']))
      if not siblings:
         F("nosib_cp_%s" % ctag)
         F("nosib_pp_%s" % ptag)
      # TODO: look at children of child and parent of parent?
      for grn in grandchl:
         F("gp_%s"       %  (grn['tag']))
         F("gp_pc_%s_%s" %  (grn['tag'],ctag))
         F("gp_pp_%s_%s" %  (grn['tag'],ptag))
         F("gf_%s"       %  (grn['form']))
      if not grandchl:
         F("nogrn_%s" % ctag)
         F("nogrn_pp_%s" % ptag)
      #if parpar:
      #   F("prpr_%s"       %  (parpar['tag']))
      #   F("prpr_pc_%s_%s" %  (parpar['tag'],ctag))
      #   F("prpr_pp_%s_%s" %  (parpar['tag'],ptag))
      #   F("prpr_%s"       %  (parpar['form']))

      if cm1:
         F("cm1p_%s"       %  (cm1['tag']))
         F("cm1p_pc_%s_%s" %  (cm1['tag'],ctag))
         F("cm1f_%s"       %  (cm1['form']))

      if cm2:
         F("cm2p_%s"       %  (cm2['tag']))
         F("cm2p_pc_%s_%s" %  (cm2['tag'],ctag))
         F("cm2f_%s"       %  (cm2['form']))
         #F("cm2p_cm1p_%s_%s" % (cm2['tag'],cm1['tag'])) ??

      if cp1:
         F("cp1p_%s"       %  (cp1['tag']))
         F("cp1p_pc_%s_%s" %  (cp1['tag'],ctag))
         F("cp1f_%s"       %  (cp1['form']))

      if cp2:
         F("cp2p_%s"       %  (cp2['tag']))
         F("cp2p_pc_%s_%s" %  (cp2['tag'],ctag))
         F("cp2f_%s"       %  (cp2['form']))
         #F("cp2p_cp1p_%s_%s" % (cp2['tag'],cp1['tag'])) ??

      if cm1 and cp1:
         F("cm1t_ct_cp1t_%s_%s_%s" % (cm1['tag'],ctag,cp1['tag']))

      if pm1:
         F("pm1p_%s"       %  (pm1['tag']))
         F("pm1p_pp_%s_%s" %  (pm1['tag'],ptag))
         F("pm1f_%s"       %  (pm1['form']))

      if pm2:
         F("pm2p_%s"       %  (pm2['tag']))
         F("pm2p_pp_%s_%s" %  (pm2['tag'],ptag))
         F("pm2f_%s"       %  (pm2['form']))

      if pp2:
         F("pp1p_%s"       %  (pp1['tag']))
         F("pp1p_pp_%s_%s" %  (pp1['tag'],ptag))
         F("pp1f_%s"       %  (pp1['form']))

      if pp2:
         F("pp2p_%s"       %  (pp2['tag']))
         F("pp2p_pp_%s_%s" %  (pp2['tag'],ptag))
         F("pp2f_%s"       %  (pp2['form']))
     
      if pm1 and pp1:
         F("pm1t_ct_pp1t_%s_%s_%s" % (pm1['tag'],ptag,pp1['tag']))

      # POS in between
      for mid in sent[min(cid,pid)+1:max(cid,pid)]:
         mtag = mid['tag']
         F("ct_pt_mt_%s_%s_%s"   % (ctag,mtag,ptag))
         F("ct_mt_%s_%s"         % (ctag,mtag))
         F("mt_pt_%s_%s"         % (mtag,ptag))
         F("mt_%s"               % (mtag))

      # conjoin everything with direction
      dr = "_L" if child['id']>parent['id'] else "_R"
      dfs = ["%s%s" % (f,dr) for f in fs]

      # add only direction
      fs.append(dr)

      return fs + dfs
#}}}

class AnEdgeLabelFeatureExtractor6SG: #{{{
   '''
   Try looking at children of child
   '''
   def __init__(self):
      pass

   def extract(self,child,parent,sent,deps=None,par='parent',prel='prel',guides=None):
      fs = []
      F = fs.append

      ctag = child['tag']
      cform = child['form']
      ptag = parent['tag']
      pform = parent['form']

      cid = child['id']
      pid = parent['id']
      slen = len(sent)

      siblings = [t for t in sent if t[par]==pid and t['id']!=cid]
      grandchl = [t for t in sent if t[par]==cid]
      #parpar   = sent[parent[par]] if pid != 0 else None

      cm1 = sent[cid-1] if cid > 0        else None
      cm2 = sent[cid-2] if cid > 1        else None
      cp1 = sent[cid+1] if cid < slen-1   else None
      cp2 = sent[cid+2] if cid < slen-2   else None
      pm1 = sent[pid-1] if pid > 0        else None
      pm2 = sent[pid-2] if pid > 1        else None
      pp1 = sent[pid+1] if pid < slen-1   else None
      pp2 = sent[pid+2] if pid < slen-2   else None

      # standard word/pos features
      F("ct_%s" % ctag)
      F("pt_%s" % ptag)
      F("cf_%s" % cform)
      F("pf_%s" % pform)
      F("ptct_%s_%s" % (ptag,ctag))
      F("pfcf_%s_%s" % (pform,cform))
      F("pfct_%s_%s" % (pform,ctag))
      F("ptcf_%s_%s" % (ptag,cform))

      for sib in siblings:
         F("sp_%s"       %  (sib['tag']))
         F("sp_pc_%s_%s" %  (sib['tag'],ctag))
         F("sp_pp_%s_%s" %  (sib['tag'],ptag))
         F("sf_%s"       %  (sib['form']))
      if not siblings:
         F("nosib_cp_%s" % ctag)
         F("nosib_pp_%s" % ptag)
      # TODO: look at children of child and parent of parent?
      for grn in grandchl:
         F("gp_%s"       %  (grn['tag']))
         F("gp_pc_%s_%s" %  (grn['tag'],ctag))
         F("gp_pp_%s_%s" %  (grn['tag'],ptag))
         F("gf_%s"       %  (grn['form']))
      if not grandchl:
         F("nogrn_%s" % ctag)
         F("nogrn_pp_%s" % ptag)
      #if parpar:
      #   F("prpr_%s"       %  (parpar['tag']))
      #   F("prpr_pc_%s_%s" %  (parpar['tag'],ctag))
      #   F("prpr_pp_%s_%s" %  (parpar['tag'],ptag))
      #   F("prpr_%s"       %  (parpar['form']))

      if cm1:
         F("cm1p_%s"       %  (cm1['tag']))
         F("cm1p_pc_%s_%s" %  (cm1['tag'],ctag))
         F("cm1f_%s"       %  (cm1['form']))

      if cm2:
         F("cm2p_%s"       %  (cm2['tag']))
         F("cm2p_pc_%s_%s" %  (cm2['tag'],ctag))
         F("cm2f_%s"       %  (cm2['form']))
         #F("cm2p_cm1p_%s_%s" % (cm2['tag'],cm1['tag'])) ??

      if cp1:
         F("cp1p_%s"       %  (cp1['tag']))
         F("cp1p_pc_%s_%s" %  (cp1['tag'],ctag))
         F("cp1f_%s"       %  (cp1['form']))

      if cp2:
         F("cp2p_%s"       %  (cp2['tag']))
         F("cp2p_pc_%s_%s" %  (cp2['tag'],ctag))
         F("cp2f_%s"       %  (cp2['form']))
         #F("cp2p_cp1p_%s_%s" % (cp2['tag'],cp1['tag'])) ??

      if cm1 and cp1:
         F("cm1t_ct_cp1t_%s_%s_%s" % (cm1['tag'],ctag,cp1['tag']))

      if pm1:
         F("pm1p_%s"       %  (pm1['tag']))
         F("pm1p_pp_%s_%s" %  (pm1['tag'],ptag))
         F("pm1f_%s"       %  (pm1['form']))

      if pm2:
         F("pm2p_%s"       %  (pm2['tag']))
         F("pm2p_pp_%s_%s" %  (pm2['tag'],ptag))
         F("pm2f_%s"       %  (pm2['form']))

      if pp2:
         F("pp1p_%s"       %  (pp1['tag']))
         F("pp1p_pp_%s_%s" %  (pp1['tag'],ptag))
         F("pp1f_%s"       %  (pp1['form']))

      if pp2:
         F("pp2p_%s"       %  (pp2['tag']))
         F("pp2p_pp_%s_%s" %  (pp2['tag'],ptag))
         F("pp2f_%s"       %  (pp2['form']))
     
      if pm1 and pp1:
         F("pm1t_ct_pp1t_%s_%s_%s" % (pm1['tag'],ptag,pp1['tag']))

      # POS in between
      for mid in sent[min(cid,pid)+1:max(cid,pid)]:
         mtag = mid['tag']
         F("ct_pt_mt_%s_%s_%s"   % (ctag,mtag,ptag))
         F("ct_mt_%s_%s"         % (ctag,mtag))
         F("mt_pt_%s_%s"         % (mtag,ptag))
         F("mt_%s"               % (mtag))

      # guides features
      for gf in guides[(pid,cid)]:
         F("g_%s" % gf)
         F("g_%s_%s_%s" % (gf, ctag, ptag))

      # conjoin everything with direction
      dr = "_L" if child['id']>parent['id'] else "_R"
      dfs = ["%s%s" % (f,dr) for f in fs]

      # add only direction
      fs.append(dr)

      return fs + dfs
#}}}

class AnEdgeLabelFeatureExtractor6Lex: #{{{
   '''
   Try looking at children of child
   '''
   def __init__(self):
      pass
   def extract(self,child,parent,sent,deps=None,par='parent',prel='prel'):
      def lextag(tok):
         try:
            return tok['lextag']
         except KeyError:
            for tok in sent:
               tag = tok['tag']
               ltag = "%s-%s" % (tag,tok['form']) if tag in ['IN','TO','CC'] else tag
               tok['lextag'] = ltag
            return tok['lextag']
      fs = []
      F = fs.append

      ctag = lextag(child)
      cform = child['form']
      ptag = lextag(parent)
      pform = parent['form']

      cid = child['id']
      pid = parent['id']
      slen = len(sent)

      siblings = [t for t in sent if t[par]==pid and t['id']!=cid]
      grandchl = [t for t in sent if t[par]==cid]
      #parpar   = sent[parent[par]] if pid != 0 else None

      cm1 = sent[cid-1] if cid > 0        else None
      cm2 = sent[cid-2] if cid > 1        else None
      cp1 = sent[cid+1] if cid < slen-1   else None
      cp2 = sent[cid+2] if cid < slen-2   else None
      pm1 = sent[pid-1] if pid > 0        else None
      pm2 = sent[pid-2] if pid > 1        else None
      pp1 = sent[pid+1] if pid < slen-1   else None
      pp2 = sent[pid+2] if pid < slen-2   else None

      # standard word/pos features
      F("ct_%s" % ctag)
      F("pt_%s" % ptag)
      F("cf_%s" % cform)
      F("pf_%s" % pform)
      F("ptct_%s_%s" % (ptag,ctag))
      F("pfcf_%s_%s" % (pform,cform))
      F("pfct_%s_%s" % (pform,ctag))
      F("ptcf_%s_%s" % (ptag,cform))


      for sib in siblings:
         F("sp_%s"       %  (lextag(sib)))
         F("sp_pc_%s_%s" %  (lextag(sib),ctag))
         F("sp_pp_%s_%s" %  (lextag(sib),ptag))
         F("sf_%s"       %  (sib['form']))
      if not siblings:
         F("nosib_cp_%s" % ctag)
         F("nosib_pp_%s" % ptag)
      # TODO: look at children of child and parent of parent?
      for grn in grandchl:
         F("gp_%s"       %  (lextag(grn)))
         F("gp_pc_%s_%s" %  (lextag(grn),ctag))
         F("gp_pp_%s_%s" %  (lextag(grn),ptag))
         F("gf_%s"       %  (grn['form']))
      if not grandchl:
         F("nogrn_%s" % ctag)
         F("nogrn_pp_%s" % ptag)
      #if parpar:
      #   F("prpr_%s"       %  (parpar['tag']))
      #   F("prpr_pc_%s_%s" %  (parpar['tag'],ctag))
      #   F("prpr_pp_%s_%s" %  (parpar['tag'],ptag))
      #   F("prpr_%s"       %  (parpar['form']))

      if cm1:
         F("cm1p_%s"       %  (lextag(cm1)))
         F("cm1p_pc_%s_%s" %  (lextag(cm1),ctag))
         F("cm1f_%s"       %  (cm1['form']))

      if cm2:
         F("cm2p_%s"       %  (lextag(cm2)))
         F("cm2p_pc_%s_%s" %  (lextag(cm2),ctag))
         F("cm2f_%s"       %  (cm2['form']))
         #F("cm2p_cm1p_%s_%s" % (cm2['tag'],cm1['tag'])) ??

      if cp1:
         F("cp1p_%s"       %  (lextag(cp1)))
         F("cp1p_pc_%s_%s" %  (lextag(cp1),ctag))
         F("cp1f_%s"       %  (cp1['form']))

      if cp2:
         F("cp2p_%s"       %  (lextag(cp2)))
         F("cp2p_pc_%s_%s" %  (lextag(cp2),ctag))
         F("cp2f_%s"       %  (cp2['form']))
         #F("cp2p_cp1p_%s_%s" % (cp2['tag'],cp1['tag'])) ??

      if cm1 and cp1:
         F("cm1t_ct_cp1t_%s_%s_%s" % (lextag(cm1),ctag,lextag(cp1)))

      if pm1:
         F("pm1p_%s"       %  (lextag(pm1)))
         F("pm1p_pp_%s_%s" %  (lextag(pm1),ptag))
         F("pm1f_%s"       %  (pm1['form']))

      if pm2:
         F("pm2p_%s"       %  (lextag(pm2)))
         F("pm2p_pp_%s_%s" %  (lextag(pm2),ptag))
         F("pm2f_%s"       %  (pm2['form']))

      if pp2:
         F("pp1p_%s"       %  (lextag(pp1)))
         F("pp1p_pp_%s_%s" %  (lextag(pp1),ptag))
         F("pp1f_%s"       %  (pp1['form']))

      if pp2:
         F("pp2p_%s"       %  (lextag(pp2)))
         F("pp2p_pp_%s_%s" %  (lextag(pp2),ptag))
         F("pp2f_%s"       %  (pp2['form']))
     
      if pm1 and pp1:
         F("pm1t_ct_pp1t_%s_%s_%s" % (lextag(pm1),ptag,lextag(pp1)))

      # POS in between
      for mid in sent[min(cid,pid)+1:max(cid,pid)]:
         mtag = lextag(mid)
         F("ct_pt_mt_%s_%s_%s"   % (ctag,mtag,ptag))
         F("ct_mt_%s_%s"         % (ctag,mtag))
         F("mt_pt_%s_%s"         % (mtag,ptag))
         F("mt_%s"               % (mtag))

      # conjoin everything with direction
      dr = "_L" if child['id']>parent['id'] else "_R"
      dfs = ["%s%s" % (f,dr) for f in fs]

      # add only direction
      fs.append(dr)

      return fs + dfs
#}}}



class AnEdgeLabelFeatureExtractor6Prels: #{{{
   '''
   when considering sibling/grandchildren, consider also their labels.
   This assume some oredering where some labels are computer before other ones.
   This could be done bottom-up left-to-right, or in an "easy-first" manner.
   '''
   def __init__(self):
      pass
   def extract(self,child,parent,sent,deps=None,par='parent',prel='pprel'):
      fs = []
      F = fs.append

      ctag = child['tag']
      cform = child['form']
      ptag = parent['tag']
      pform = parent['form']

      cid = child['id']
      pid = parent['id']
      slen = len(sent)

      siblings = [t for t in sent if t[par]==pid and t['id']!=cid]
      grandchl = [t for t in sent if t[par]==cid]
      #parpar   = sent[parent[par]] if pid != 0 else None

      cm1 = sent[cid-1] if cid > 0        else None
      cm2 = sent[cid-2] if cid > 1        else None
      cp1 = sent[cid+1] if cid < slen-1   else None
      cp2 = sent[cid+2] if cid < slen-2   else None
      pm1 = sent[pid-1] if pid > 0        else None
      pm2 = sent[pid-2] if pid > 1        else None
      pp1 = sent[pid+1] if pid < slen-1   else None
      pp2 = sent[pid+2] if pid < slen-2   else None

      # standard word/pos features
      F("ct_%s" % ctag)
      F("pt_%s" % ptag)
      F("cf_%s" % cform)
      F("pf_%s" % pform)
      F("ptct_%s_%s" % (ptag,ctag))
      F("pfcf_%s_%s" % (pform,cform))
      F("pfct_%s_%s" % (pform,ctag))
      F("ptcf_%s_%s" % (ptag,cform))

      for sib in siblings:
         F("sp_%s"       %  (sib['tag']))
         F("sp_pc_%s_%s" %  (sib['tag'],ctag))
         F("sp_pp_%s_%s" %  (sib['tag'],ptag))
         F("sf_%s"       %  (sib['form']))
         # add relation label if exists
         sprel = "%s-%s" % (sib['tag'],sib.get(prel,"/NA/"))
         F("sp_%s"       %  (sprel))
         F("sp_pc_%s_%s" %  (sprel,ctag))
         F("sp_pp_%s_%s" %  (sprel,ptag))
      if not siblings:
         F("nosib_cp_%s" % ctag)
         F("nosib_pp_%s" % ptag)
      # TODO: look at children of child and parent of parent?
      for grn in grandchl:
         F("gp_%s"       %  (grn['tag']))
         F("gp_pc_%s_%s" %  (grn['tag'],ctag))
         F("gp_pp_%s_%s" %  (grn['tag'],ptag))
         F("gf_%s"       %  (grn['form']))
         # add relation label if exists
         gprel = "%s-%s" % (grn['tag'],grn.get(prel,"/NA/"))
         F("gp_%s"       %  (gprel))
         F("gp_pc_%s_%s" %  (gprel,ctag))
         F("gp_pp_%s_%s" %  (gprel,ptag))
      if not grandchl:
         F("nogrn_%s" % ctag)
         F("nogrn_pp_%s" % ptag)
      #if parpar:
      #   F("prpr_%s"       %  (parpar['tag']))
      #   F("prpr_pc_%s_%s" %  (parpar['tag'],ctag))
      #   F("prpr_pp_%s_%s" %  (parpar['tag'],ptag))
      #   F("prpr_%s"       %  (parpar['form']))

      if cm1:
         F("cm1p_%s"       %  (cm1['tag']))
         F("cm1p_pc_%s_%s" %  (cm1['tag'],ctag))
         F("cm1f_%s"       %  (cm1['form']))

      if cm2:
         F("cm2p_%s"       %  (cm2['tag']))
         F("cm2p_pc_%s_%s" %  (cm2['tag'],ctag))
         F("cm2f_%s"       %  (cm2['form']))
         #F("cm2p_cm1p_%s_%s" % (cm2['tag'],cm1['tag'])) ??

      if cp1:
         F("cp1p_%s"       %  (cp1['tag']))
         F("cp1p_pc_%s_%s" %  (cp1['tag'],ctag))
         F("cp1f_%s"       %  (cp1['form']))

      if cp2:
         F("cp2p_%s"       %  (cp2['tag']))
         F("cp2p_pc_%s_%s" %  (cp2['tag'],ctag))
         F("cp2f_%s"       %  (cp2['form']))
         #F("cp2p_cp1p_%s_%s" % (cp2['tag'],cp1['tag'])) ??

      if cm1 and cp1:
         F("cm1t_ct_cp1t_%s_%s_%s" % (cm1['tag'],ctag,cp1['tag']))

      if pm1:
         F("pm1p_%s"       %  (pm1['tag']))
         F("pm1p_pp_%s_%s" %  (pm1['tag'],ptag))
         F("pm1f_%s"       %  (pm1['form']))

      if pm2:
         F("pm2p_%s"       %  (pm2['tag']))
         F("pm2p_pp_%s_%s" %  (pm2['tag'],ptag))
         F("pm2f_%s"       %  (pm2['form']))

      if pp2:
         F("pp1p_%s"       %  (pp1['tag']))
         F("pp1p_pp_%s_%s" %  (pp1['tag'],ptag))
         F("pp1f_%s"       %  (pp1['form']))

      if pp2:
         F("pp2p_%s"       %  (pp2['tag']))
         F("pp2p_pp_%s_%s" %  (pp2['tag'],ptag))
         F("pp2f_%s"       %  (pp2['form']))
     
      if pm1 and pp1:
         F("pm1t_ct_pp1t_%s_%s_%s" % (pm1['tag'],ptag,pp1['tag']))

      # POS in between
      for mid in sent[min(cid,pid)+1:max(cid,pid)]:
         mtag = mid['tag']
         F("ct_pt_mt_%s_%s_%s"   % (ctag,mtag,ptag))
         F("ct_mt_%s_%s"         % (ctag,mtag))
         F("mt_pt_%s_%s"         % (mtag,ptag))
         F("mt_%s"               % (mtag))

      # conjoin everything with direction
      dr = "_L" if child['id']>parent['id'] else "_R"
      dfs = ["%s%s" % (f,dr) for f in fs]

      # add only direction
      fs.append(dr)

      return fs + dfs
#}}}
