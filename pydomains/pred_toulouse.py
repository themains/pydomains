#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Predict the Toulouse list categories
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
    model_fn = 'toulouse_cat_lstm_others_{0:d}.h5'.format(year)
    model_path = get_app_file_path('pydomains', model_fn)
    if not os.path.exists(model_path) or latest:
        print("Downloading Toulouse model data from the server ({0!s})..."
              .format(model_fn))
        if not download_file(MODELS_BASE_URL + model_fn, model_path):
            print("ERROR: Cannot download Toulouse model data file")
            return None, None, None
    else:
        print("Using cached Toulouse model data from local ({0!s})...".format(model_path))
    vocab_fn = 'toulouse_cat_vocab_others_{0:d}.csv'.format(year)
    vocab_path = get_app_file_path('pydomains', vocab_fn)
    if not os.path.exists(vocab_path) or latest:
        print("Downloading Toulouse vocab data from the server ({0!s})..."
              .format(vocab_fn))
        if not download_file(MODELS_BASE_URL + vocab_fn, vocab_path):
            print("ERROR: Cannot download Toulouse vocab data file")
            return None, None, None
    else:
        print("Using cached Toulouse vocab data from local ({0!s})...".format(vocab_path))
    names_fn = 'toulouse_cat_names_others_{0:d}.csv'.format(year)
    names_path = get_app_file_path('pydomains', names_fn)
    if not os.path.exists(names_path) or latest:
        print("Downloading Toulouse names data from the server ({0!s})..."
              .format(names_fn))
        if not download_file(MODELS_BASE_URL + names_fn, names_path):
            print("ERROR: Cannot download Toulouse names data file")
            return None, None, None
    else:
        print("Using cached Toulouse names data from local ({0!s})...".format(names_path))
    print("Loading Toulouse model, vocab and names data file...")
    #  sort n-gram by freq (highest -> lowest)
    vdf = pd.read_csv(vocab_path)
    vocab = vdf.vocab.tolist()
    model = load_model(model_path)
    cdf = pd.read_csv(names_path)
    categories = cdf.toulouse_cat.tolist()
    return (model, vocab, categories)


def pred_toulouse(df, domain_names="domain_names", year=2017, latest=False):
    """Predict the category of content hosted by the domain
     using the Toulouse model

    Args:
        df (:obj:`DataFrame`): Pandas DataFrame. No default value.
        domain_names (str): Column name of the domain in DataFrame. 
            Default in `domain_names`.
        year (int): Toulouse model year. Only 2017 is available.
            Default is `2017`.
        latest (Boolean): Whether or not to download latest 
            model available from GitHub. Default is `False`.
    
    Returns:
        DataFrame: Pandas DataFrame with additional columns:
            - `pred_toulouse_year_domain`: domain name
            - `pred_toulouse_year_lab`: most probable category
            - `pred_toulouse_year_prob_catname`: probability that the 
              domain hosts content of category `catname`
    """

    if domain_names not in df.columns:
        print("No column `{0!s}` in the DataFrame".format(column))
        return None

    model, vocab, cats = load_model_data(year, latest)

    if model is None or vocab is None or cats is None:
        print("ERROR: Couldn't load model data.")
        return None

    col_domain = 'pred_toulouse_{0:04d}_domain'.format(year)
    col_lab =  'pred_toulouse_{0:04d}_lab'.format(year)
    col_probs =  ['pred_toulouse_{0:04d}_prob_{1:s}'.format(year, c)
                  for c in cats]

    df[col_domain] = df[domain_names].apply(lambda c: url2domain(c, exclude_subdomains=['www']))

    # build X from index of n-gram sequence
    X = np.array(df[col_domain].apply(lambda c: find_ngrams(vocab, c, NGRAMS)))
    X = sequence.pad_sequences(X, maxlen=FEATURE_LEN)

    df['toulouse_cat'] = model.predict_classes(X, verbose=2)

    df[col_lab] = df.toulouse_cat.apply(lambda c: cats[c])
    del df['toulouse_cat']

    proba = model.predict_proba(X, verbose=2)

    pdf = pd.DataFrame(proba, columns=col_probs)
    pdf.set_index(df.index, inplace=True)

    df = pd.concat([df, pdf], axis=1)

    return df


if __name__ == "__main__":
    pass
