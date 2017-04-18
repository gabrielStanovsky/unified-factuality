""" Usage:
    annotate_factuality --truthteller=PATH_TO_TT --input=INPUT_FILE --output=OUTPUT_DIR [--start=START_INDEX] [--end=END_INDEX]

Annotate a given conll file with factulity and print to a given output file.
"""
from docopt import docopt
from truth_teller_factuality_annotator import Truth_teller_factuality_annotator
from truth_teller_wrapper import Truth_teller_wrapper
import os
import logging
logging.basicConfig(level = logging.DEBUG)


def read_conll(input_conll_file):
    """
    Return a list of (sentence, predicate indexes) from a given conll file
    """
    ret = []
    curSent = ""
    curPreds = []
    for line in open(input_conll_file):
        line = line.strip()
        if not line:
            if curSent:
                ret.append((curSent.lstrip(), curPreds)) # Remove unneeded starting space
            curSent = ""
            curPreds = []
        else:
            # Some spacy characters mess up the conll format -- ignore these lines and carry on
            try:
                ind, word, fact = line.split()[:3]
                curSent += " " + word
                if is_annot(fact):
                    curPreds.append(int(ind))
            except:
                logging.warn("Couldn't parse line: {}".format(line))
                logging.debug("adding SP")
                # Not really sure what's better to insert here
                # SP messes up the parser's output
                curSent += " ,"
#                curSent += " SP"

                print curSent
    return ret

def is_annot(val):
    """
    Return True iff val is a factuality annotation
    http://stackoverflow.com/questions/354038/how-do-i-check-if-a-string-is-a-number-float-in-python
    """
    if val == "DEFAULT":
        return True
    try:
        float(val)
        return True
    except:
        return False


def annotate_conll(sentence_annotator, input_conll_file, output_dir, start_index = None, end_index = None):
    """
    Given an sentence_annotator and an input conll file - run the annotator on
    all the sentences in the file and return a string representing all of the sentences'
    output.
    """
    ret = []
    sents = read_conll(input_conll_file)
    logging.debug("Total number of sentences in input file: {}".format(len(sents)))
    if not start_index:
        start_index = 0
    if not end_index:
        end_index = len(sents)

    toAnnotate = sents[start_index : end_index]
    total = len(toAnnotate)

    for i, (sent, predicate_indexes) in enumerate(toAnnotate):
        logging.debug("{}/{} -- {}".format(i, total, sent))
        sent_index = i + start_index
        try:
            cur_parse = sentence_annotator.annotate_sentence(sent, predicate_indexes)
        except:
            logging.error("Couldn't produce output for sentence {}".format(sent_index))
            continue
        ret.append(cur_parse)
        with open(os.path.join(output_dir, "{0:04d}.conll".format(sent_index)), 'w') as fout:
            fout.write('\n'.join(['\t'.join(map(str,ent)) for
                                  ent in cur_parse]))
            fout.write('\n\n')
    return ret

if __name__ == '__main__':
    args = docopt(__doc__)
    logging.debug(args)
    tt_path = args["--truthteller"]
    input_fn = args["--input"]
    output_dir = args["--output"]
    start = args['--start']
    end = args['--end']
    tt_annotator = Truth_teller_factuality_annotator(Truth_teller_wrapper(tt_path))
    ret = annotate_conll(tt_annotator, input_fn, output_dir,
                         start_index = int(start) if start else start,
                         end_index = int(end) if end else end)
    print '\n\n'.join('\n'.join(['\t'.join(map(str,ent)) for ent in line]) for line in ret)
