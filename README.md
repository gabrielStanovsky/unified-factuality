
Code and data for testing different factuality models across different testsets.
This is the code and dataset reported in [Integrating Deep Linguistic Features in Factuality Prediction over Unified Datasets](https://gabrielstanovsky.github.io/assets/papers/acl17/paper.pdf), Gabriel Stanovsky, Judith Eckle-Kohler, Yevgeniy Puzikov, Ido Dagan and Iryna Gurevych, ACL 2017.

If you use this data set or provided tools, make sure to cite the following paper:

```
@InProceedings{stanovsky2017fact,
author    = {Stanovsky, Gabriel and Eckle-Kohler, Judith and Puzikov, Yevgeniy and Dagan, Ido and Gurevych, Iryna},
title     = {Integrating Deep Linguistic Features in Factuality Prediction over Unified Datasets},
booktitle = {Proceedings of the 55th Annual Meeting of the Association for Computational Linguistics (ACL 2017)},
month     = {August},
year      = {2017},
address   = {Vancouver, Canada}
}
```

## Getting started:

From ```src``` run:

```
./scripts/install.sh
```

This will perform the following steps (each of which can also be run separately):

1. [Install required packages](./src/scripts/install_requirements.sh).
2. [Download external resources](./src/scripts/download_external.sh).
3. [Convert to unified factuality](./src/scripts/convert.sh)

The converted unified corpus should be created in the [unified directory](data/unified).
There's also a static aggregated version of the corpus in the [snapshot folder](data/unified/snapshot).

## Format

TODO


## Running the automatic annotator

## OLD:

### TODO:


#### Unified corpus:
   1. Download external script to get all of the datasets
   2. Requirements pip file to download all needed python dependencies

#### Practical factuality annotator:
   1. End-to-end pipeline: Raw text -> annotation (will apply dependency parsing)
   2. Dep trees -> factuality. Will provide the ability to experiment with other dep parsers.
   3. Client - server architecture. Will load all heavy models once (Spacy, Truthteller, etc.)
   4. Using the previous module - create an online demo.


### Converting the Data to CoNLL Format

#### UW
Run the conversion script:

        src> ./convert_uw.sh
This will create the UW [dev](data/uw/factuality-data/dev.conll), [train](data/uw/factuality-data/train.conll), and [test](data/uw/factuality-data/test.conll) CoNLL files with factuality annotations.

#### MEANTIME
Run the conversion script:

        src> ./convert_meantime.sh
This will create the [Meantime](data/meantime/meantime_cross_filtered.conll) CoNLL file with factuality annotations.

Splitting the corpus:

        src> ./split_meantime.sh

This will create the MEANTIME [train](data/meantime/train.conll), [dev](data/meantime/dev.conll) and [test](data/meantime/test.conll) files.

#### Factbank
Run the conversion script:

        src> ./convert_factbank.sh
This will create the [Factbank ](data/factbank_v1/factbank_filtered.conll) CoNLL file with factuality annotations.

Splitting the corpus:

        src> ./split_factbank.sh

This will create the factbank [train](data/factbank_v1/train.conll), [dev](data/factbank_v1/dev.conll) and [test](data/factbank_v1/test.conll) files.


### Running TruthTeller on the Test Set

1. Run the spaCy server:


        src>  python ./parsers/spacy_server.py

2. In a new terminal, run:

        src> ./run_TT_on_UW_test.sh
    This will take some time (20 minutes on my machine) and will create a [TruthTeller annotated file](src/test.tt.conll)

    **Note**: where Truthteller doesn't annotate a value, this will produce a "DEFAULT" label instead of a number in [-3, 3].

### Evaluate Against the Gold Standard

Run:

    src> python  ./evaluate.py  --pred=./test.tt.conll  --gold=../data/uw/factuality-data/test.conll --default=3

### Other Evaluations

#### Label Distribution Histogram

For example, for the development set, run:

    src> python ./plot_histogram.py --in=../data/uw/factuality-data/dev.conll --out=../figures/Dev_gold_histogram.svg --default=3 --title="Dev TT Gold Histogram"

This will create the [dev histogram figure](figures/Dev_gold_histogram.svg).


















