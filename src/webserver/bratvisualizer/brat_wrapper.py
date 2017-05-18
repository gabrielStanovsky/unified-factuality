import logging
from brat_handler import Brat
from operator import itemgetter
from annotate_factuality import parse_sent
logging.basicConfig(level = logging.INFO)


class Brat_wrapper:
    """
    Simple wrapper for easier sentence level represenation
    """

    def __init__(self, sentence):
        """
        Initialize with a space separated sentence
        """
        self.sent = sentence
        self.annots = {}


    def add_fact(self, word_index, val):
        """
        Add annotation of factuality val for word at index word_index
        """
        self.annots[word_index] = val


    def get_html(self):
        """
        Return the html representation as string
        """
        return Brat.sent_to_html(self.sent,
                                 self.annots)

    def visualize(self, fn):
        """
        Visualize this structure into a brat html file
        """
        Brat.output_brat_html(self.sent,
                              self.annots,
                              fn)

def conll_to_brat(conll):
    """
    Convert conll factuality represnetation to brat html
    """
    split_lines = [line.strip().split('\t') for line in conll.split('\n')
                   if line.strip()]
    sent = ' '.join(map(itemgetter(1), split_lines))
    brat = Brat_wrapper(sent)
    for (word_index, val) in enumerate(map(itemgetter(2),
                                           split_lines)):
        if val != "_":
            brat.add_fact(word_index, float(val))

    return brat.get_html()

if __name__ == "__main__":
    ## Example usage
    from truth_teller_factuality_annotator import Truth_teller_factuality_annotator
    from truth_teller_wrapper import Truth_teller_wrapper

    # Initialize TruthTeller
    tt_annotator = Truth_teller_factuality_annotator(Truth_teller_wrapper('../truth_teller/'))

    # Write example to file
    with open("./webserver/bratvisualizer/visualizations/fact_example.html", 'w') as fout:
        fout.write(conll_to_brat(parse_sent(tt_annotator, "Don refused to pay his taxes .")))
    print("wrote to file")

