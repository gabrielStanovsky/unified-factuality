from truth_teller_wrapper import Truth_teller_wrapper

class Truth_teller_factuality_annotator:
    """
    Functions which receive a single sentence, runs Truthteller on it and makes factuality assessments.
    """

    # The default factuality value
    DEFAULT = "DEFAULT"

    def __init__(self, truth_teller):
        """
        Init with backend truth teller instance
        """
        self.truth_teller = truth_teller

    def tt_annot_to_fact(self, sig, nu, ct, pt):
        """
        Convert a truth_teller annotation: (sig, nu, ct, pt)
        to a UW style annotation in [-3, 3]
        """
        ret = Truth_teller_factuality_annotator.DEFAULT
        if pt == 'N':
            ret = -3.0
        if pt == 'P':
            ret = 3.0
        if (nu == 'N') and (ret != Truth_teller_factuality_annotator.DEFAULT):
            #TODO: Can experiment with changing the factuality if nu is 'N' and we're currently on default -
            #      for instance, by changing factuality to -1.0
            ret *= 0.5
        return ret

    def annotate_sentence(self, sent, predicate_indexes):
        """
        Given a sentence and a list of indexes, returns a list of
        (word index, word, factuality value)
        """
        return [(ind,
                 word,
                 self.tt_annot_to_fact(*tt_output) if (ind in predicate_indexes) else '_') +
                tt_output # add TT annotations as features
                for ind, (word, tt_output) in
                enumerate(self.truth_teller.annotate(sent))]


if __name__ == '__main__':
    tt = Truth_teller_factuality_annotator(Truth_teller_wrapper('../truth_teller'))
    print tt.annotate_sentence("Gal refused to go home", [1, 3])
