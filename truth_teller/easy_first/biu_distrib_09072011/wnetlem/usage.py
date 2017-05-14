import wordnet as wn
w=wn.WordNetCorpusReader("data/")
print w.morphy("book",w.NOUN)
