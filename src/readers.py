""" Usage:
    readers (--uw=FILENAME_WITHOUT_TYPE | --mt=FILENAME | --fb_path=FB_PATH) --out=OUT_FILENAME
"""

import sys
sys.path.append('../')
import os
from spacy.en import English
from collections import defaultdict
from bs4 import BeautifulSoup
import logging
from HTMLParser import HTMLParser
from unidecode import unidecode
from pprint import pprint
logging.basicConfig(level = logging.DEBUG)

nlp = English()

class Doc_with_factuality:
    """
    Abstraction over spaCy docuemnt which records factuality per token in a document.
    Note: this is obsolete if there's some way to add attributes to spaCy tokens
    """
    def __init__(self):
        self.factuality = defaultdict(lambda: '_')

    def set_doc(self, doc):
        """
        Record this document's parsed spacy output.
        """
        self.doc = doc

    def is_event(self, i):
        """
        Return True iff the token at index i is an event (meaning there's a factuality value in [-3, 3] associated with it)
        """
        return (self.factuality[i] != '_')

    def set_factuality(self, i, val):
        """
        Set the factuality value of token at index i
        """
        self.factuality[i] = val

    def get_factuality(self, i):
        """
        Set the factuality value of token at index i
        """
        return self.factuality[i]

class Word:
    """
    Container record class for storing word relevant information
    """
    def __init__(self,
                 t_id,
                 surface_form,
                 sent_id,
                 evaluate_func):
        """
        t_id - token id from the document
        surface_from - the textual representation of this word
        sent_id - the index of the sentence, taken from attribute in the xml
        evaluate_func - function to transform Meantime's values to float value
        """
        self.t_id = int(t_id)
        self.surface_form = surface_form
        self.sent_id = int(sent_id)
        self.feats = defaultdict(lambda : "_")
        self.html_parser = HTMLParser()
        self.evaluate_func = evaluate_func

    def conll(self):
        """
        A list of conll values
        The annotated factuality values according to:
        http://www.lrec-conf.org/proceedings/lrec2014/pdf/188_Paper.pdf
        """
        ## TODO: There are many attributes that seem relevant
        ## (e.g., "modality", ""attribution"")
        ## Should they be added as well?
        try:
            return map(str, [self.word_ind,    # Word index in sentence
                             unidecode(self.html_parser.unescape(self.surface_form)), # Surface form
                             self.evaluate_func(self.feats)])  # Factuality numerical value
        except:
            logging.debug("Problem with {}".format((self.surface_form,
                                                    self.feats)))
            raise

class Factbank:
    """
    Reads factbank annotation files, producing (as class members):
    - CONLL string represeting parse and factuality annotations.
    - FB values from "FactBank: a corpus annotated with event factuality" (Sauri, 2009)
    Committed Values:
    CT+ - According to the source, it is certainly the case that X.
    Our value: 3.0
    PR+ - According to the source, it is probably the case that X.
    Our value: 2.0
    PS+ - According to the source, it is possibly the case that X.
    Our value: 1.0
    CT- - According to the source, it is certainly not the case that X.
    Our value: -3.0
    PR- - According to the source it is probably not the case that X.
    Our value: -2.0
    PS- - According to the source it is possibly not the case that X.
    Our value: -1.0
    (Partially) Uncommitted Values:
    CTu - The source knows whether it is the case that X or that not X.
    Our value: 0.0
    Uu  - The source does not know what is the factual status of the
    event, or does not commit to it.
    Our value: 0.0
    """
    def __init__(self, fb_factvalue, tokens_tml, sentence_threshold = 3):
        """
        fb_factvalue - the patht to fb_factvalue.txt in Factbank
        tokens_tml - the patht to tokens_tml in Factbank
        sentence_threshold - Filter sentences shorter than this number
                             (This helps in removal of boiler plate sentences)
        """
        self.fact_annots = self.load_fact_annots(fb_factvalue)
        self.sentence_threshold = sentence_threshold
        self.conversion_dic = {
            "CT+": 3.0,
            "PR+": 2.0,
            "PS+": 1.0,
            'CTu': 0.0,
            'Uu' : 0.0,
            "PS-": -1.0,
            "PR-": -2.0,
            "CT-": -3.0
        }
        self.conll_txt = self.convert(tokens_tml)

    def __str__(self):
        return self.conll_txt

    def load_fact_annots(self, fb_factvalue):
        """
        Given an fb_factvalue file, returns a dictionary:
        filename -> sent_number -> entity -> source -> factuality value
        """
        ret = {}
        for line in open(fb_factvalue):
            line = line.strip()
            if not line:
                continue
            filename, sent_id, fvid, eId, \
            eiId, relSourceId, eText, \
            relSourceText, factValue = [eval(v) for v in line.split('|||')]
            if factValue:
                keys = [filename, sent_id, eId, relSourceText]
                ddict_app(ret, factValue, keys)
                assert len(ddict_get(ret, keys)) == 1,\
                    "More than one value by source: {}".format((keys, ddict_get(ret, keys)))
        return ret

    def to_float(self, fact_val):
        """
        Return a float factual value for a given textual input
        """
        return self.conversion_dic[fact_val]

    def consolidate_fact_value(self, filename, sent_number, entity_id):
        """
        Return the *float* factuality value of a given set of keys.
        Consolidates over the possibly multiple sources
        """
        opts = ddict_get(self.fact_annots,
                         [filename, sent_number, entity_id])

        ## TODO:
        ## Some weird sentences have conflicting pov's (e.g., ('APW19980301.0720.tml', 5, 'e3'))
        ## As a heuristic I prioritize commited values first
        ## adn chose the least commited option, which is conveniently adhers to
        ## alphabetical order:  PS, PR, CT

        commit_opts = sorted([list(opt)[0] for opt in opts.values()
                              if ('+' in list(opt)[0]) or ('-' in list(opt)[0])],
                             reverse = True)

        # if there are no commited values, return the first option
        return self.to_float(commit_opts[0]) if commit_opts\
            else self.to_float(list(opts.values()[0])[0])



    def convert(self, token_tml):
        """
        Convert a token_tml file to conll format
        """
        sents = []
        cur_sent = []
        last_sent = -1
        for line in open(token_tml):
            line = line.strip()
            if not line:
                continue
            fn, sent_id, tok_id, \
            surface_form, tmlTag, tmlTagId, tmlTagLoc = [eval(v) for v in line.split('|||')]
            cur_ent = [tok_id,
                       surface_form,
                       self.consolidate_fact_value(fn, sent_id, tmlTagId) \
                       if (tmlTag == 'EVENT')\
                          else  "_"]

            if sent_id != last_sent:
                if cur_sent:
                    toks = nlp(unicode(" ".join([word[1] for word in cur_sent])))
                    dep_feats = self.get_dep_feats(toks, cur_sent)
                    sents.append([fb_feat + dep_feat
                                  for (fb_feat, dep_feat) in zip(cur_sent, dep_feats)])
                cur_sent = [cur_ent]
            else:
                cur_sent.append(cur_ent)
            last_sent = sent_id

        return '\n\n'.join(['\n'.join(['\t'.join(map(str, word))
                                       for word in sent])
                            for sent in sents
                            if len(sent) > self.sentence_threshold]) + "\n\n"  # filter short sentences

    def get_dep_feats(self, toks, sent):
        """
        Return the required features to complete the conll format:
        1. POS
        2. Head index
        3. Head relations
        4. Lemma
        """
        self.align(toks, sent)
        assert(len(toks) == len(sent))  # After alignment there should be the of equal lengths
        return [[tok.tag_,
                 str(tok.head.i),
                 tok.dep_,
                 unidecode(tok.lemma_)] for tok in toks]

    def align(self, toks, sent):
        """
        Match between the spacy tokens in toks to the words in sent
        Might merge tokens in spacy in-place.
        """
        toks_ind = 0
        sent_ind = 0
        ret = []
        while sent_ind < len(sent):
 #           logging.debug("sent_ind = {}, toks_ind = {}".format(sent_ind, toks_ind))
            cur_tok = str(toks[toks_ind])
            cur_word = sent[sent_ind][1]
 #           logging.debug("{} vs. {}".format(cur_tok, cur_word))
 #           logging.debug("flag = {}".format(cur_word.endswith(cur_tok)))
            if (cur_tok == cur_word) or \
               (cur_word.endswith(cur_tok) and \
                (toks_ind >= (len(toks) -1) or ((cur_tok + str(toks[toks_ind + 1])) not in cur_word))):
                toks_ind += 1
                sent_ind += 1

            elif cur_tok in cur_word:
#                logging.debug("merging: {}".format(toks[toks_ind : toks_ind + 2]))
                toks[toks_ind : toks_ind + 2].merge()

            else:
                raise Exception("Unknown case: {}".format((toks,
                                                           cur_tok,
                                                           cur_word)))
        assert(toks_ind == len(toks))
        return ret

class Meantime:
    """
    Reads a Meantime annotation file, producing (as class members):
    - CONLL string represeting parse and factuality annotations.
    """
    def __init__(self, fn, translate_dic):
        """
        translate_dic is used to carry counts across Meantime instances
        """
        self.fn = fn
        self.translate_dic = translate_dic
        self.convert(self.fn)

    @staticmethod
    def get_translate_dic():
        """
        Convert Meantime's several axes into a single numerical fact.
        Following:
        http://www.lrec-conf.org/proceedings/lrec2014/pdf/188_Paper.pdf

        Fact: corresponds to the actual world.
        polarity: YES
        certainty: CERTAIN
        temporality: PAST/PRESENT
        Our value: 3.0

        Counterfact: does not correspond to the actual world.
        polarity: NO
        certainty: CERTAIN
        temporality: PAST/PRESENT
        Our value: -3.0

        Possibility (uncertain): could correspond to the actual world,
                                    but the source is not certain
        polarity: YES or NO
        certainty: POSSIBLE
        temporality: PAST/PRESENT or FUTURE
        Our value: +- 0.75 (depending on polarity)

        Possibility (future): could correspond to the actual world in the future
        polarity: YES or NO
        certainty: PROBABLE
        temporality: PAST/PRESENT or FUTURE
        Our value: +- 1.5 (depending on polarity)
        """
        translate_dic = defaultdict(lambda:  # polarity
                                         defaultdict(lambda: # certainty
                                                     defaultdict(lambda: # time
                                                                 [0, 0])))
        # (translate value, counter)
        translate_dic["POS"]["CERTAIN"]["NON_FUTURE"] = [3.0, 0]
        translate_dic["POS"]["CERTAIN"]["FUTURE"] = [3.0, 0]
        translate_dic["NEG"]["CERTAIN"]["NON_FUTURE"] = [-3.0, 0]
        translate_dic["NEG"]["CERTAIN"]["FUTURE"] = [-3.0, 0]
        translate_dic["POS"]["POSSIBLE"]["NON_FUTURE"] = [0.75, 0]
        translate_dic["POS"]["POSSIBLE"]["FUTURE"] = [0.75, 0]
        translate_dic["NEG"]["POSSIBLE"]["NON_FUTURE"] = [-0.75, 0]
        translate_dic["NEG"]["POSSIBLE"]["FUTURE"] = [-0.75, 0]
        translate_dic["POS"]["PROBABLE"]["NON_FUTURE"] = [1.5, 0]
        translate_dic["POS"]["PROBABLE"]["FUTURE"] = [1.5, 0]
        translate_dic["NEG"]["PROBABLE"]["NON_FUTURE"] = [-1.5, 0]
        translate_dic["NEG"]["PROBABLE"]["FUTURE"] = [-1.5, 0]

        return translate_dic

    def calculate_numerical_fact(self, feats):
        """
        Convert Meantime's several axes into a single numerical fact.
        """
        polarity = feats["polarity"]
        certainty = feats["certainty"]
        time = feats["time"]
        if any([feat == "_" for feat in [polarity,
                                         certainty,
                                         time]]):
            return "_"
        ent = self.translate_dic[polarity]\
              [certainty]\
              [time]

        ent[1] += 1
        return ent[0]

    def __str__(self):
        return self.conll_txt

    def convert(self, fn):
        """
        Returns a sentence split and tokenized version of meanttime's data, in a simple conll like form.
        Output format is a list of tab-delimited strings, each representing a single token in the input.
        Sentences are delimited by an empty line
        """
        self.soup = BeautifulSoup(open(fn), "lxml")
        self.tokens = dict([(int(tok["t_id"]),
                             Word(t_id = tok["t_id"],
                                  surface_form = tok.text,
                                  sent_id = tok["sentence"],
                                  evaluate_func = lambda feats: self.calculate_numerical_fact(feats)))
                            for tok in self.soup.find_all("token")])

        # Associate each event with a token
        # Find all events with a "pred" attribute
        ## TODO: Here I ignore those without a pred attribute - is it possible that these
        ## actually encode the nested semantics? (which is actually what we need)
        self.events = self.soup.find_all("event_mention", attrs={"pred":lambda s: s})

        for event in self.events:
            for anchor in event.find_all("token_anchor"):
                # "" -> "_" for conll
                self.tokens[int(anchor["t_id"])].feats.update([(k, v if v else "_")
                                                               for (k, v) in event.attrs.iteritems()])

        self.sents = []
        cur_sent = []
        word_ind = -1     # Store the index of this word in the sentence
        for t_id, tok in self.tokens.iteritems():
            word_ind += 1
            if not (cur_sent):
                cur_sent.append(tok)
                tok.word_ind = word_ind
                continue

            if tok.sent_id != cur_sent[-1].sent_id:
                # This indicates a new sentence
                self.sents.append(cur_sent)
                cur_sent = [tok]
                word_ind = 0

            else:
                cur_sent.append(tok)

            tok.word_ind = word_ind

        # Store the last sentence
        self.sents.append(cur_sent)

        # Remove sentences without any factuality annotations
        ## TODO: not sure why, but it seems like some
        ## files in Meantime just stop annotating sentences at some point
        ## certain sentences - I remove these here
        for sent in reversed(self.sents):
            if any([feat not in ["", "_"] for word in sent
                    for feat in word.feats]):
                # Found the last annotated sentence
                break
            self.sents.remove(sent)

        # A more conservative approach:
        # self.sents = filter(lambda sent: any([feat not in ["", "_"] for word in sent
        #                                       for feat in word.feats]),
        #                     self.sents)

        # Construct conll

        self.conll_txt = ""
        for sent in self.sents:
            toks = nlp(unicode(" ".join([w.surface_form for w in sent])))
            dep_feats = self.get_dep_feats(toks, sent)

            self.conll_txt += '\n'.join(['\t'.join(word.conll() + dep_feat)
                                         for word, dep_feat in zip(sent, dep_feats)])+ "\n\n"

    def get_dep_feats(self, toks, sent):
        """
        Return the required features to complete the conll format:
        1. POS
        2. Head index
        3. Head relations
        4. Lemma
        """
        self.align(toks, sent)
        assert(len(toks) == len(sent))  # After alignment there should be the of equal lengths
        return [[tok.tag_,
                 str(tok.head.i),
                 tok.dep_,
                 unidecode(tok.lemma_)] for tok in toks]

    def align(self, toks, sent):
        """
        Match between the spacy tokens in toks to the words in sent
        and return the required features to complete the conll format:
        1. POS
        2. Head index
        3. Head relations
        4. Lemma
        """
        toks_ind = 0
        sent_ind = 0
        ret = []
        while sent_ind < len(sent):
            cur_tok = str(toks[toks_ind]).decode("ascii", errors = 'ignore')
            cur_word = unidecode(sent[sent_ind].surface_form)

            if (cur_tok == cur_word) or \
               cur_tok.endswith(cur_word) or cur_word.endswith(cur_tok):
                toks_ind += 1
                sent_ind += 1

            elif cur_tok in cur_word:
                toks[toks_ind : toks_ind + 2].merge()

            else:
                raise Exception("Unknown case: {}".format((toks,
                                                           cur_tok,
                                                           cur_word)))
        assert(toks_ind == len(toks))
        return ret

class UW:
    """
    Reads a UW directory, producing (as class members):
    - CONLL string represeting parse and factuality annotations.
    - Doc_with_factuality encoding a spacy parse with the factuality annotations.
    """
    def __init__(self, txt_file, ann_file):
        self.txt_file = txt_file
        self.ann_file = ann_file
        self.factuality = Doc_with_factuality()
        self.conll_txt = self.alternative_convert(self.txt_file, self.ann_file)

    def __str__(self):
        """
        Return a textual conll represenation of this UW format file
        """
        return '\n'.join(self.conll_txt)

    @staticmethod
    def read_ann_file(ann_file):
        # Read gold labels
        dic = dict([(line.split('\t')[0], '\t'.join(line.strip().split('\t')[1:]))
                    for line in open(ann_file)])
        starts = {}
        ends = {}
        for key, val in [(k, v) for (k, v) in dic.iteritems() if k.startswith('T')]:
            span, word = val.split('\t')
            start, end = map(int, span.split(' ')[1:])
            ind = int(key[1:])
            data = dic['A{}'.format(ind)].split(' ')
            assert(data[0] == 'Factuality')
            score = float(data[2])
            # Because tokenization is different between our code and uw unavailable (?) tokenization, I use only the start of the span as index
            # TODO: ask Kenton for the tokenized version of their data? The paper says that they highlighted tokens for annotators,
            #       so there should be some tokenized version of the data
            starts[start] = (score, word)
            ends[end] = start
        return starts, ends

    def get_opts(self, word, word_to_ret_index):
        """
        Get best matching options for word in word_to_ret_index
        """
        ret = word_to_ret_index[word]
        if ret:
            return ret

        for word_opt, val in word_to_ret_index.iteritems():
            if ((word_opt in word) or (word in word_opt)) and (len(word_opt) > 0.2*(len(word))):
                ret.extend(val)

        return ret

    def get_conll_format_per_token(self, tok, sent_start):
        """
        Return the conll format for this token (list of values)
        Format: index, word, factuality value (place holder - always blank),
        pos, dep head index, dep relation, lemma
        """
        return map(str, [tok.i - sent_start, tok, "_", tok.tag_, tok.head.i - sent_start, tok.dep_, tok.lemma_])

    def alternative_convert(self, txt_file, ann_file):
        """
        Hopefully with no SP shananigans.
        Returns a sentence split and tokenized version of uw's data, in a simple conll like form.
        Output format is a list of tab-delimited strings, each representing a single token in the input.
        Sentences are delimited by an empty line
        """
        gold_dic, gold_ends = UW.read_ann_file(ann_file)
        ret = []
        word_to_ret_index = defaultdict(lambda: [])
        global_index = 0
        last_val = '\n'

        for line in open(txt_file).readlines():
            line = line.strip()
            if not line:
                if ret and (ret[-1] != []):
                    ret.append([])
                global_index += 1
                continue
            line = " ".join([word for word in line.split(" ") if word])

            toks = nlp(unicode(line))

            for sent in toks.sents:
                sent_start = sent[0].i
                for cur_tok in sent:
                    word_to_ret_index[str(cur_tok)].append((len(ret), global_index))
                    global_index += len(cur_tok) + 1
                    ret.append(self.get_conll_format_per_token(cur_tok, sent_start))
                ret.append([])

        for start, (score, word) in gold_dic.iteritems():
            opts = self.get_opts(word, word_to_ret_index)
            assert len(opts) > 0
            best = min(opts, key = lambda (ret_index, global_ind): abs(global_ind - start))
            ret_index, global_ind = best
            ret[ret_index][2] = str(score)

        return ['\t'.join(x) for x in ret]

def ddict_app(d, val, args):
    """
    Append (to a set) the value 'val' to an arbitrary nesting in dictionary 'd'
    """
    cur = d
    for k in args[:-1]:
        cur[k] = cur.get(k, {})
        cur = cur[k]
    last_k = args[-1]
    cur[last_k] = cur.get(last_k, set())
    cur[last_k] = cur[last_k].union([val])

def ddict_get(d, keys):
    """
    Return a value from an arbitrary nesting level in dictionary 'd'
    """
    cur = d
    for k in keys:
        cur = cur[k]
    return cur

if __name__ == '__main__':
    from docopt import docopt
    args = docopt(__doc__)
    out = args["--out"]

    if args["--uw"] is not None:
        logging.debug("Parsing UW")
        inp_ = args["--uw"]
        conll = UW(inp_ + '.txt',
                   inp_ + '.ann')

        with open(out, 'w') as fout:
            fout.write(str(uw))

    if args["--mt"] is not None:
        logging.info("Parsing Meantime")
        inp_ = args["--mt"]
        mt = Meantime(inp_, Meantime.get_translate_dic())

        with open(out, 'w') as fout:
            fout.write(str(mt))

    if args["--fb_path"] is not None:
        logging.debug("Parsing Factbank")
        inp_ = args["--fb_path"]
        fb = Factbank(os.path.join(inp_, "fb_factValue.txt"),
                      os.path.join(inp_, "tokens_tml.txt"))
        with open(out, 'w') as fout:
            fout.write(str(fb))
