Unified Factuality Representation - Corpus and code
===================================================

Introduction
============

Code and data for testing different factuality models across different testsets.<br>
If you use this resource, please cite the  following [paper](https://gabrielstanovsky.github.io/assets/papers/acl17/paper.pdf):

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

Online Demo
===========

Local Installation
==================

This repository provides:

1. A unified factuality dataset

2. Automatic factuality annotator

The following describes the installtion and format of both of these.


Unified dataset
---------------

You can find a static aggregated version of the corpus in the [snapshot folder](data/unified/snapshot).

Manual Download
---------------

From ```src```:

1. Download external corpora: <br>
```
./scripts/download_external_corpora.sh
```

**NOTE**: FactBank should be downloaded separately. Please login to LDC, [download the corpus](https://catalog.ldc.upenn.edu/ldc2009t23), and place it in the directory ```factbank_v1``` under ```/data/external_annotations/```.


2. Convert to a unified representation:<br>
```
./scripts/convert_corpora.sh
```

The converted unified corpus should be created in the [unified corpus directory](data/unified).

Format
------

TODO

Automatic annotator
-------------------

Installation
------------

From ```src```, run: <br>
```
sudo -E ./scripts/install_annotator.sh
```
Running the automatic annotator
-------------------------------

1. Start servers:

    1. Start the spaCy server:<br>
    Run ```./scripts/run_spacy_server.sh``` <br>
    Wait for the the ```ENGINE Bus STARTED``` message to appear, indicating that the server is up.

    2. In a new terminal, start the PropS server:<br>
    Run ```./scripts/run_props_server.sh```<br>
    Wait for the ```Listening on http://:8081/``` message to appear, indicating that the server is up.

2. Run client application:<br>
``` ./scripts/annotate_factuality.sh ``` <br>
This will wait for output on STDIN and will output sentences with CoNLL factuality annotations 
to STDOUT.

Usage examples
--------------

``` echo "John refused to go" | ./scripts/annotate_factuality.sh ```

``` ./scripts/annotate_factuality.sh < input_file > output_file ```


<!-- ## OLD: -->

<!-- ### TODO: -->


<!-- #### Unified corpus: -->
<!--    1. Download external script to get all of the datasets -->
<!--    2. Requirements pip file to download all needed python dependencies -->

<!-- #### Practical factuality annotator: -->
<!--    1. End-to-end pipeline: Raw text -> annotation (will apply dependency parsing) -->
<!--    2. Dep trees -> factuality. Will provide the ability to experiment with other dep parsers. -->
<!--    3. Client - server architecture. Will load all heavy models once (Spacy, Truthteller, etc.) -->
<!--    4. Using the previous module - create an online demo. -->


<!-- ### Converting the Data to CoNLL Format -->

<!-- #### UW -->
<!-- Run the conversion script: -->

<!--         src> ./convert_uw.sh -->
<!-- This will create the UW [dev](data/uw/factuality-data/dev.conll), [train](data/uw/factuality-data/train.conll), and [test](data/uw/factuality-data/test.conll) CoNLL files with factuality annotations. -->

<!-- #### MEANTIME -->
<!-- Run the conversion script: -->

<!--         src> ./convert_meantime.sh -->
<!-- This will create the [Meantime](data/meantime/meantime_cross_filtered.conll) CoNLL file with factuality annotations. -->

<!-- Splitting the corpus: -->

<!--         src> ./split_meantime.sh -->

<!-- This will create the MEANTIME [train](data/meantime/train.conll), [dev](data/meantime/dev.conll) and [test](data/meantime/test.conll) files. -->

<!-- #### Factbank -->
<!-- Run the conversion script: -->

<!--         src> ./convert_factbank.sh -->
<!-- This will create the [Factbank ](data/factbank_v1/factbank_filtered.conll) CoNLL file with factuality annotations. -->

<!-- Splitting the corpus: -->

<!--         src> ./split_factbank.sh -->

<!-- This will create the factbank [train](data/factbank_v1/train.conll), [dev](data/factbank_v1/dev.conll) and [test](data/factbank_v1/test.conll) files. -->


<!-- ### Running TruthTeller on the Test Set -->

<!-- 1. Run the spaCy server: -->


<!--         src>  python ./parsers/spacy_server.py -->

<!-- 2. In a new terminal, run: -->

<!--         src> ./run_TT_on_UW_test.sh -->
<!--     This will take some time (20 minutes on my machine) and will create a [TruthTeller annotated file](src/test.tt.conll) -->

<!--     **Note**: where Truthteller doesn't annotate a value, this will produce a "DEFAULT" label instead of a number in [-3, 3]. -->

<!-- ### Evaluate Against the Gold Standard -->

<!-- Run: -->

<!--     src> python  ./evaluate.py  --pred=./test.tt.conll  --gold=../data/uw/factuality-data/test.conll --default=3 -->

<!-- ### Other Evaluations -->

<!-- #### Label Distribution Histogram -->

<!-- For example, for the development set, run: -->

<!--     src> python ./plot_histogram.py --in=../data/uw/factuality-data/dev.conll --out=../figures/Dev_gold_histogram.svg --default=3 --title="Dev TT Gold Histogram" -->

<!-- This will create the [dev histogram figure](figures/Dev_gold_histogram.svg). -->


















