"""Usage:
  evaluate --gold=GOLD_FILE (--pred=PRED_FILE | --allfactual) --default=DEFAULT_VALUE

Prints the Mean Squared Error between a predicated and gold factuality file, using a specified default value.
Assumes that both gold and predicated agree on the events to annotate. """

from docopt import docopt
from operator import itemgetter
from scipy.stats import pearsonr
from sklearn.metrics import mean_absolute_error
from collections import defaultdict
from annotate_factulity import is_annot
import numpy as np
import matplotlib.pyplot as plt
import string
import math
import logging
logging.basicConfig(level = logging.DEBUG)

class Factuality:
    """
    Container for factuality functions, and main driver through the constructor function.
    Stores metrics as class variables.
    """
    def __init__(self, gold_fn, pred_fn, default_value):
        """
        Calculate metrics for gold against predicted.
        The predicted file may contain entries marked as DEFAULT --
        to indicate the predictor didn't assign a value to this entry.
        Evaluate will replace such entries with default_value (Float).
        """
        self.default_value = default_value
        self.evaluate(gold_fn, pred_fn)

    def evaluate(self, gold_fn, pred_fn):
        """
        Driver for evaluating gold vs. predicted factuality.
        if pred_fn is None, will evaluate the factual baseline
        """
        self.load_values(gold_fn, pred_fn)
        self.compute_agreement()

    def extract_word_and_vals(self, fn):
        """
        Extract only indices, words and factuality values
        from an annotation file
        """
        self.original_lines = list(enumerate(open(fn).readlines()))
        return filter(lambda (line_ind, (ind, word, val)): val != "_",
                      [(line_ind, line.strip().split('\t')[:3])
                       for line_ind, line in self.original_lines
                       if line.strip()])

    def load_values(self, gold_fn, pred_fn):
        """
        Stores gold and predicted values into class memebers
        """
        self.gold_vals = self.extract_word_and_vals(gold_fn)

        if pred_fn is not None:
            self.pred_vals = self.extract_word_and_vals(pred_fn)

            # Sanity check -- Make sure that gold and pred agree on the input
            self.gold_vals, self.pred_vals = self.validate_gold_pred(self.gold_vals, self.pred_vals)

            # Extract only numerical factuality values
            self.pred_vals = map(lambda (ind, val): (ind, float(val) if val != "DEFAULT" else self.default_value),
                                 [(ind, val) for (ind, (_, word, val)) in self.pred_vals])

        else:
            logging.info("Evaluating All-factual baseline")
            # Factual baseline
            self.pred_vals = self.generate_factual_baseline(self.gold_vals)

        # Extract only numerical factuality values
        self.gold_vals = map(lambda (ind, val): (ind, float(val) if val != "DEFAULT" else self.default_value),
                                 [(ind, val) for (ind, (_, word, val)) in self.gold_vals])
        # self.gold_vals = map(float,
        #                      map(itemgetter(2), self.gold_vals))

    def compute_agreement(self):
        """
        Compute agreement values after loading them into member variables
        """
        golds = map(itemgetter(1),
                    self.gold_vals)
        preds = map(itemgetter(1),
                    self.pred_vals)
        self.mse = self._mse(golds, preds)
        self.mae = mean_absolute_error(golds, preds)
        self.normalized_mae = self.mae / 6.0
        self.pearson = pearsonr(golds, preds)

    def generate_factual_baseline(self, gold_vals):
        """
        Generate a baseline which always assigns 3.0
        """
        return [3.0] * len(gold_vals)

    def validate_gold_pred(self, gold, pred):
        """
        Returns true iff gold and pred agree on index and word
        """
        #assert len(gold) == len(pred), "Lists are of different lenghts ({}, {})!".format(len(gold), len(pred))
        d = defaultdict(lambda: defaultdict (lambda: []))

        for i, x in gold:
            ind, word = x[:2]
            d[ind][word] = [(i, x)]

        for i, y in pred:
            ind, word = y[:2]
            d[ind][word].append((i, y))

        ret_gold = []
        ret_pred = []
        for ind, words in d.iteritems():
            for word in words:
                if len(d[ind][word]) == 2:
                    ret_gold.append(d[ind][word][0])
                    ret_pred.append(d[ind][word][1])


        logging.debug("{} factuality annotations".format(len(ret_gold)))
        return ret_gold, ret_pred
#        return all([(x[0] == y[0]) and (x[1] == y[1]) for (x, y) in zip(gold, pred)])

    def _mse(self, gold, pred):
        """
        Compute the Mean Squared Error between two float lists
        """
        n = len(gold) * 1.0
        return sum([math.pow(x -y, 2) for (x, y) in zip(gold, pred)]) / n

    def _mae(self, gold, pred):
        """
        Compute the Mean Absolute Error between two float lists
        """
        n = len(gold) * 1.0
        return sum([abs(x -y) for (x, y) in zip(gold, pred)]) / n

    def find_first_diff(self, gold, pred):
        """
        Return the first index in which gold and pred differ in terms of word or index
        """
        g = f.read_factuality(gold_fn)
        p = f.read_factuality(pred_fn)
        for i, ((id1, w1, _), (id2, w2, _)) in enumerate(zip(g, p)):
            if (w1 != w2) or (id1 != id2):
                return i

class Factuality_annotation:
    """
    Load factuality annotations and calculate statistics about it
    """
    def __init__(self, fn, default_value):
        self.default_value = float(default_value)
        self.vals = self.read_factuality(fn)

    def hist(self, fn, title):
        """
        Plot an histagram of the values stored at in this annotation
        """
        hist, bin_edges =  np.histogram(map(itemgetter(2), self.vals), bins = np.arange(start = -3, stop = 3.5, step = 0.5))
        ind = np.arange(len(hist))
        plt.xlim([-0.5, len(ind)])
        plt.bar(ind, hist, width = 0.7)
        plt.xticks(ind, bin_edges[:-1])
        plt.xlabel('Label')
        plt.ylabel('#Instances')
        plt.title(title)
        plt.savefig(fn)
        return hist, bin_edges

    def read_factuality(self, fact_fn):
        """
        Reads factuality from file, assumes that each line is composed of tab separated token_id, word, factuality value
        Ignores any other tab separated fields that might appear in the file.
        Replaces "DEFAULT" labels with the default value.
        Returns a list of (token_id, word, factuality value).
        """
        ret = []
        self.vals_per_sent = {}
        cur_sent_fact = []
        cur_sent = ''
        for line in open(fact_fn):
            line = line.strip()
            if not line:
                if cur_sent:
                    self.vals_per_sent[cur_sent] = cur_sent_fact
                cur_sent = ''
                cur_sent_fact = []
            else:
                data = line.split('\t')
                token_id, word, fact_value, pos, head = data[:5]
                if len(data) > 5:
                    rel = data[5]
                else:
                    rel = 'punct'
                cur_sent += word.translate(None, string.punctuation)
                if is_annot(fact_value):
                    toAppend = [token_id, word, float(fact_value) if (fact_value != "DEFAULT") else self.default_value, pos, head, rel]
                    ret.append(toAppend)
                    cur_sent_fact.append(toAppend)

        # Make sure that we flushed the last buffer of annotations
        assert cur_sent == '', cur_sent
        return ret



## Constants
# An annotation value for inspection purposes, used to indicate that this value should be
# removed from both train and test
IGNORE_DEFAULT = 4

if __name__ == '__main__':
    logging.basicConfig(level = logging.DEBUG)
    args = docopt(__doc__)
    logging.error(args)
    gold_fn = args['--gold']
    pred_fn = args['--pred']

    default_value = float(args['--default'])
    f = Factuality(gold_fn, pred_fn, default_value)
    logging.info("MAE:\t{}".format(f.mae))
    logging.info("MSE:\t{}".format(f.mse))
    logging.info("r:\t{}".format(f.pearson))
