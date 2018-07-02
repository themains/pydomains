#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Predict the Phishtank categories
"""

import os

import numpy as np
import pandas as pd

from keras.models import load_model
from keras.preprocessing import sequence

from .utils import (url2domain, get_app_file_path, download_file, find_ngrams,
                    MODELS_BASE_URL)

NGRAMS = 2
FEATURE_LEN = 128


def load_model_data(year, latest=False):
    model_fn = 'phish_cat_lstm_{0:d}.h5'.format(year)
    model_path = get_app_file_path('pydomains', model_fn)
    if not os.path.exists(model_path) or latest:
        print("Downloading Phishtank model data from the server ({0!s})..."
              .format(model_fn))
        if not download_file(MODELS_BASE_URL + model_fn, model_path):
            print("ERROR: Cannot download Phishtank model data file")
            return None, None
    else:
        print("Using cached Phishtank model data from local ({0!s})...".format(model_path))
    vocab_fn = 'phish_cat_vocab_{0:d}.csv'.format(year)
    vocab_path = get_app_file_path('pydomains', vocab_fn)
    if not os.path.exists(vocab_path) or latest:
        print("Downloading Phishtank vocab data from the server ({0!s})..."
              .format(vocab_fn))
        if not download_file(MODELS_BASE_URL + vocab_fn, vocab_path):
            print("ERROR: Cannot download Phishtank vocab data file")
            return None, None
    else:
        print("Using the cached Phishtank vocab data from local ({0!s})...".format(vocab_path))
    print("Loading the Phishtank model and vocab data file...")
    #  sort n-gram by freq (highest -> lowest)
    vdf = pd.read_csv(vocab_path)
    vocab = vdf.vocab.tolist()
    model = load_model(model_path)

    return (model, vocab)


def pred_phish(df, domain_names="domain_names", year=2016, latest=False):
    """Predict whether domain is implicated in phishing
       using a model based on the PhishTank data.

    Args:
        df (:obj:`DataFrame`): Pandas DataFrame. No default value.
        domain_names (str): Column name of the domain in DataFrame. 
            Default in `domain_names`.
        year (int): PhishTank model year. Only 2016 is available.
            Default is `2016`.
        latest (Boolean): Whether or not to download latest 
            model available from GitHub. Default is `False`.

    Returns:
        DataFrame: Pandas DataFrame with additional columns:
            - `pred_phish_year_domain`: domain name
            - `pred_phish_year_lab`: most probable category
            - `pred_phish_year_prob`: probability of the domain being
              implicated in phishing.
    """

    if domain_names not in df.columns:
        print("No column `{0!s}` in the DataFrame".format(column))
        return None

    model, vocab = load_model_data(year, latest)

    if model is None or vocab is None:
        print("ERROR: Couldn't load model data.")
        return None

    col_domain = 'pred_phish_{0:04d}_domain'.format(year)
    col_lab =  'pred_phish_{0:04d}_lab'.format(year)
    col_prob =  'pred_phish_{0:04d}_prob'.format(year)
    df[col_domain] = df[domain_names].apply(lambda c: url2domain(c, exclude_subdomains=['www']))

    # build X from index of n-gram sequence
    X = np.array(df[col_domain].apply(lambda c: find_ngrams(vocab, c, NGRAMS)))
    X = sequence.pad_sequences(X, maxlen=FEATURE_LEN)

    df[col_lab] = model.predict_classes(X, verbose=2)

    df[col_prob] = model.predict_proba(X, verbose=2)[:, 1]

    return df


if __name__ == "__main__":
    pass
