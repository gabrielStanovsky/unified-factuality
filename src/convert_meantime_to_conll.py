""" Usage:
    convert_meantime_to_conll --in=PATH_TO_UW --out=OUTPUT_FILE

Converts a MEANTIME style factuality annotation folder to a single CONLL-style file.
"""
from docopt import docopt
from glob import glob
from readers import Meantime
import os
import logging
from pprint import pprint
logging.basicConfig(level = logging.INFO)


def pprint_nested_ddict(d):
    """
    pprint a nested default dict
    """
    def dictify(d):
        if not isinstance(d, dict):
            return d
        return dict([(k, dictify(v)) for k, v in d.iteritems()])
    pprint(dictify(d))


if __name__ == "__main__":
    args = docopt(__doc__)
    path = args['--in']
    output_file = args['--out']

    logging.basicConfig(level = logging.DEBUG)

    # Get unique Filename -- there is an .ann and .txt file per each entry
    files = glob(os.path.join(path, "*/*.xml"))

    cnt = 0
    cnt_sents = 0
    translate_dic = Meantime.get_translate_dic()

    with open(output_file, 'w') as fout:
        for fn in files:
            logging.info(fn)
            mt = Meantime(fn, translate_dic)
            cnt_sents += len(mt.sents)
            fout.write(str(mt))
            # Just in case, add an extra empty line
            fout.write('\n')
            cnt += 1

    pprint_nested_ddict(mt.translate_dic)

    logging.info("Converted {} Meantime sentences in {} files into {}".format(cnt_sents,
                                                                              cnt,
                                                                              output_file))
