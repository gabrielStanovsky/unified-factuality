<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [Unified Factuality Representation - Corpus and Code](#unified-factuality-representation---corpus-and-code)
  - [Introduction](#introduction)
  - [Online Demo](#online-demo)
  - [Local Installation](#local-installation)
    - [Pre-requsities](#pre-requsities)
    - [Unified Dataset](#unified-dataset)
      - [Manual Download](#manual-download)
      - [Format](#format)
    - [Automatic Annotator](#automatic-annotator)
      - [Installation](#installation)
      - [Running the Automatic Annotator](#running-the-automatic-annotator)
      - [Usage Examples](#usage-examples)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# Unified Factuality Representation - Corpus and Code


## Introduction

Previous models for the assessment of commitment towards a predicate in a sentence (also known as factuality prediction) were trained and tested against a specific annotated dataset, subsequently limiting the generality of their results. In this work we propose an intuitive method for mapping three previously annotated corpora onto a single factuality scale, thereby enabling models to be tested across these corpora. In addition, we design a novel model for factuality prediction by first extending a previous rule-based factuality prediction system and applying it over an abstraction of dependency trees, and then using the output of this system in a supervised classifier.

In this repository you'll find both the converted corpus, as well as our factuality prediction model.

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

## Online Demo


Try a live demonstration by heading over to our [Online Demo Page](http://u.cs.biu.ac.il/~stanovg/factuality.html)


## Local Installation


### Pre-requsities

1. python 2.7
2. Java openjdk-8
```
Make sure that the JAVA_HOME variable is set accordingly.
E.g., JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64/
```
3. python-setuptools
4. easy_install
5. pip 9.x
6. libxml
7. libxslt
8. NLTK with the WordNet corpus<br>
```
pip install nltk
python -c "import nltk;nltk.download('wordnet')"
```
9. spaCy with English models<br>
```
pip install spacy
python -m spacy download en
```

### Unified Dataset


You can find a static aggregated version of the corpus in the [snapshot folder](data/unified/snapshot).

#### Manual Download


From ```src```:

1. Download external corpora: <br>
```
./scripts/download_external_corpora.sh
```

**NOTE**: FactBank should be downloaded separately. Please login to LDC, [download the corpus](https://catalog.ldc.upenn.edu/ldc2009t23), and place it in the directory ```factbank_v1``` under ```/data/external_annotations/```.

2. Install converter
```
./scripts/install_converter.sh
```

3. Convert to a unified representation:<br>
```
./scripts/convert_corpora.sh
```

The converted unified corpus should be created in the [unified corpus directory](data/unified).

#### Format


TODO

### Automatic Annotator


#### Installation


From ```src```, run: <br>
```
./scripts/install_annotator.sh
```
#### Running the Automatic Annotator


1. Start servers:

    1. Start the spaCy server:<br>
    Run ```./scripts/run_spacy_server.sh``` <br>
    This will open a server listening on port 8081 by default. <br>
    Wait for the ```ENGINE Bus STARTED``` message to appear, indicating that the server is up.
    

    2. In a new terminal, start the PropS server:<br>
    Run ```./scripts/run_props_server.sh```<br>
    This will open a server listening on port 10345. <br>
    Wait for the ```Listening on http://:8081/``` message to appear, indicating that the server is up.
  
2. Run client application:<br>
``` ./scripts/annotate_factuality.sh ``` <br>
This will wait for input on STDIN and will output sentences with CoNLL factuality annotations 
to STDOUT.

**NOTE**: You can also run these scripts using different hosts and ports. See the scripts above for instructions on how to do this.

#### Usage Examples


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


















