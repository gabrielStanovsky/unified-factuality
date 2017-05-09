""" Usage:
   split_corpus --in=CORPUS_FN --out=OUT_FOLDER --train=TRAIN_PART --dev=DEV_PART

Split a conll corpus file into train dev and test partitions. These all should sum to 1.
train partition size is assumed from the two others.
The resulting files will be named OUT_FOLDER/{train, dev, test}.conll
"""

from docopt import docopt
import numpy as np
import os
import logging
logging.basicConfig(level = logging.DEBUG)

# set seed for random for replicability
np.random.seed(42)

# UW partitions: (0.6855998114541598, 0.24982323827480557, 0.06457695027103465)
def split_corpus(sents, train_size, dev_size):
    """
    Return a random sampling of sents according to the different sizes
    Changes sents in-place.
    return (dev, train, test)
    """

    num_of_sents = len(sents)
    dev_ind, train_ind = [int(np.round(part_size * num_of_sents))
                          for part_size in (dev_size, train_size)]
    np.random.shuffle(sents)

    return (sents[: train_ind],
            sents[train_ind : (train_ind + dev_ind)],
            sents[(train_ind + dev_ind): ])

def load_corpus(conll_fn):
    """
    Returns a list of sentences encoded in conll format
    """
    ret = []
    cur_sent = []
    for line in open(conll_fn):
        line = line.strip()
        if not line:
            if cur_sent:
                ret.append(cur_sent)
            cur_sent = []
        else:
            cur_sent.append(line)
    return ret


def print_sents_to_file(sents, fn):
    """
    Print conll sentences to file, will be separated by empty lines
    """
    with open(fn, 'w') as fout:
        fout.write('\n\n'.join(['\n'.join([line for line in sent])
                              for sent in sents]) + '\n\n')

def hash_sents(sents):
    """
    Return a hashable format of a list of conll sentences
    """
    return map(str, sents)

if __name__ == "__main__":
    args = docopt(__doc__)
    corpus_fn = args["--in"]
    out_folder = args["--out"]
    train_part = float(args["--train"])
    dev_part = float(args["--dev"])

    # Load corpus and split
    sents = load_corpus(corpus_fn)

    logging.debug("Read {} sentences from {}".format(len(sents),
                                                     corpus_fn))

    train, dev, test = split_corpus(sents, train_part, dev_part)
    assert set(hash_sents(train) + hash_sents(dev) + hash_sents(test)) == set(hash_sents(sents)) # Sanity check
    logging.debug("partitioned to: {}".format(map(len, (train, dev, test))))

    # Write to files
    logging.debug("Writing to {}".format(out_folder))
    print_sents_to_file(train, os.path.join(out_folder, "train.conll"))
    print_sents_to_file(dev, os.path.join(out_folder, "dev.conll"))
    print_sents_to_file(test, os.path.join(out_folder, "test.conll"))

    logging.info("Done!")
