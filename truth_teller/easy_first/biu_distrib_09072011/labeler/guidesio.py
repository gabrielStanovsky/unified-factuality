def read_guides(base_name, guide_names):
   '''
   return:
   an iteration of dictionaries mapping guide_names to sent
   each item in the iteration is
   {'parser_a' : sent1parseda,
    'parser_b' : sent1parsedb,
    ...}

   '''
   guides = {}
   for g in guide_names:
      fname = "%s.%s" % (base_name, g)
      sents = list(io.conll_to_sents(file(fname)))
      guides[g]=sents
   names_sents = guides.items()
   names = [n  for n,ss in names_sents]
   sents = [ss for n,ss in names_sents]
   for parses in zip(*sents):
      d = dict(zip(names,parses))
      yield d
   #return guides

