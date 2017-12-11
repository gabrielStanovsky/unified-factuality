""" Usage:
   train --train=TRAIN_FILE --test=TEST_FILE
"""

from evaluate import Factuality_annotation
from docopt import docopt
import os
import logging
logging.basicConfig(level = logging.DEBUG)
from sklearn import linear_model
import pandas as pd
import numpy as np
from one_hot import One_hot, Dense_encoder
from sklearn.metrics import mean_absolute_error
from sklearn.svm import SVR


EMBEDDING_DIM = 300

class Regression:
    """
    Perform training and store resulting model
    """
    def __init__(self):
        self.regr = SVR()
        logging.debug("Regression model: {}".format(self.regr))


    def create_encoders(self, df):
        """
        Create one hot encoders based on training data (pd format).
        These will later be used to encode both train as well as test data.
        """
        #TODO: replace hard-coding of embedding dimension
        dense_encoder = Dense_encoder(EMBEDDING_DIM)  # singelton dense encoder
        # Create data encoders
        self.oh_encoders = [One_hot(list(df[col]), allow_oov = True) if (not Dense_encoder.is_dense(list(df[col])))
                            else dense_encoder    # Distinguish between one hot and dense encoding
                            for col in [col for col in df][1:]]
        logging.debug("Total number of features: {}".format(sum([enc.len_vocab for enc
                                                                 in self.oh_encoders])))

    def encode_data(self, df):
        """
        Encode the given train data (pd format) to one hot representations,
        and extract labels
        """
        # Extract labels
        labels = list(df.ix[:, 0])

        # Encode data
        encoded_data = [[oh_encoder.encode(val) for val, oh_encoder in
                         equal_zip(row[1:], self.oh_encoders)]
                        for row_index, row in df.iterrows()]

        # Merge the one hot vectors to a single sparse vector and return
        return [[val for ls in enc for val in ls] for enc in encoded_data], labels

    def train(self, train_fn):
        """
        Train a regression model from a given train file (csv)
        """
        # Parse data
        df= pd.read_csv(train_fn, sep='\t', header = None)

        # Encode data and get labels
        logging.debug("Encoding data...")
        self.create_encoders(df)         # Create one data encoders
        x, y = self.encode_data(df)

        # Fit the training data
        logging.debug("Fitting training data...")
        self.regr.fit(x, y)

    def test(self, test_fn):
        """
        Apply this model on a test file.
        """
        # Parse data
        df= pd.read_csv(test_fn, sep='\t', header = None)

        # Encode data and get labels
        logging.debug("Encoding data...")
        x, self.y_gold = self.encode_data(df)

        # Predict
        self.y_predicted = [max(min(3, y_label), -3)
                            for y_label in self.regr.predict(x)]   # cap the predictions to [-3, 3]

        logging.info("MAE: {}".format(mean_absolute_error(self.y_gold,
                                                          self.y_predicted)))


# Helper functions

def equal_zip(*args):
    """
    Zip which also verifies that all input lists are of the same length
    """
    # make sure that all lists are of the same length
    assert len(set(map(len, args))) == 1, "lists are of different lengths {}".format(args)
    return zip(*args)


if __name__ == "__main__":
    args = docopt(__doc__)
    reg = Regression()
    train_fn = args["--train"]
    test_fn = args["--test"]
    reg.train(train_fn)
    reg.test(test_fn)
