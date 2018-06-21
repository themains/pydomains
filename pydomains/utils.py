#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Utility functions
"""

import sys
import os
from os import path

import tldextract
from tqdm import tqdm
import requests

DATA_BASE_URL = (os.environ.get('PYDOMAINS_DATA_URL') or
                 'https://raw.githubusercontent.com/themains/pydomains/master/pydomains/data/')

MODELS_BASE_URL = (os.environ.get('PYDOMAINS_MODELS_URL') or
                  'https://raw.githubusercontent.com/themains/pydomains/master/pydomains/models/')


def isstring(s):
    # if we use Python 3
    if (sys.version_info[0] >= 3):
        return isinstance(s, str)
    # we use Python 2
    return isinstance(s, basestring)


def find_ngrams(vocab, text, n):
    """Find and return list of the index of n-grams in the vocabulary list.

    Generate the n-grams of the specific text, find them in the vocabulary list
    and return the list of index have been found.

    Args:
        vocab (:obj:`list`): Vocabulary list.
        text (str): Input text
        n (int): N-grams

    Returns:
        list: List of the index of n-grams in the vocabulary list.

    """

    wi = []

    if not isstring(text):
        return wi

    a = zip(*[text[i:] for i in range(n)])
    for i in a:
        w = ''.join(i)
        try:
            idx = vocab.index(w)
        except Exception as e:
            idx = 0
        wi.append(idx)
    return wi


def url2domain(url, exclude_subdomains=False):
    """Extract the domain from URL.
    """
    tld = tldextract.extract(url)
    a = []
    if tld.subdomain != '':
        if isinstance(exclude_subdomains, list):
            if tld.subdomain not in exclude_subdomains:
                a.append(tld.subdomain)
        elif not exclude_subdomains :
            a.append(tld.subdomain)
    a.append(tld.domain)
    if tld.suffix != '':
        a.append(tld.suffix)
    domain = '.'.join(a)
    return domain


def get_app_file_path(app_name, filename):
    user_dir = path.expanduser('~')
    app_data_dir = path.join(user_dir, '.' + app_name)
    if not path.exists(app_data_dir):
        os.makedirs(app_data_dir)
    file_path = path.join(app_data_dir, filename)
    return file_path


def download_file(url, target):

    if 'PYDOMAINS_AUTH_TOKEN' in os.environ:
        auth_token = os.environ['PYDOMAINS_AUTH_TOKEN']
        headers = {'Authorization': 'token {0!s}'.format(auth_token)}
    else:
        headers = {}

    # Streaming, so we can iterate over the response.
    r = requests.get(url, stream=True, headers=headers)

    if r.status_code == 200:
        chunk_size = (64 * 1024)
        # Total size in bytes.
        total_size = int(r.headers.get('content-length', 0)) / chunk_size

        total_size += 1

        with open(target, 'wb') as f:
            for data in tqdm(r.iter_content(chunk_size), total=total_size, unit_scale=chunk_size/1024, unit='KB'):
                f.write(data)
        return True
    else:
        print("ERROR: status_code={0:d}".format(r.status_code))
        return False


if __name__ == "__main__":
    print(url2domain('http://test.hello.com/hello/test?hello=test&test=hello'))
    # PYDOMAINS_AUTH_TOKEN env. var. requires for private repo.
    # https://github.com/settings/tokens
    download_file('https://raw.githubusercontent.com/soodoku/pydomains/master/pydomains/data/dmoz_2016.csv.bz2', 'test.bz2')
    print(get_app_file_path('pydomains', 'dmoz_2016.csv.bz2'))