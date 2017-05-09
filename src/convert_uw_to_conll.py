""" Usage:
    convert_uw_to_conll --in=PATH_TO_UW --out=OUTPUT_FILE

Converts a UW style factuality annotation folder to a single CONLL-style file.
"""
from docopt import docopt
from glob import glob
from readers import UW
import os
import logging


if __name__ == "__main__":
    args = docopt(__doc__)
    path = args['--in']
    output_file = args['--out']
    docs_with_fact = []

    logging.basicConfig(level = logging.DEBUG)

    # Get unique Filename -- there is an .ann and .txt file per each entry
    files = set([f.replace('.txt','.ann').split('.ann')[0]
                 for f in glob(os.path.join(path, '*'))
                 if f.endswith('.txt') or f.endswith('.ann')])

    cnt = 0

    with open(output_file, 'w') as fout:
        for fn in files:
            uw = UW('{}.txt'.format(fn),
                    '{}.ann'.format(fn))
            docs_with_fact.append(uw.factuality)
            fout.write(str(uw))
            # Just in case, add an extra empty line
            fout.write('\n')
            cnt += 1

    logging.info("Converted {} UW files into {}".format(cnt, output_file))
