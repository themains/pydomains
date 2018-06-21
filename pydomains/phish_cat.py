#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Get the domain category from the PhishTank database
"""

import os

import pandas as pd

from .utils import (url2domain, get_app_file_path, download_file,
                    DATA_BASE_URL)


def load_phish_data(year, latest=False):
    data_fn = 'phish_{0:d}.csv.bz2'.format(year)
    data_path = get_app_file_path('pydomains', data_fn)
    if not os.path.exists(data_path) or latest:
        print("Downloading PhishTank data from the server ({0!s})..."
              .format(data_fn))
        if not download_file(DATA_BASE_URL + data_fn, data_path):
            print("ERROR: Cannot download PhishTank data file")
            return None
    else:
        print("Using cached PhishTank data from local ({0!s})...".format(data_path))
    print("Loading PhishTank data file...")
    df = pd.read_csv(data_path, usecols=['domain', 'verified'])
    df.drop_duplicates('domain', inplace=True)
    df.columns = ['phish_{0:04d}_cat'.format(year), '__domain']
    return df


def phish_cat(df, domain_names="domain_names", year=2017, latest=False):
    """Appends PhishTank data to the DataFrame
    
    The function extracts the domain name along with the subdomain 
    from the specified column and appends the category (phish_cat)
    to the DataFrame. If Phishtank file is not available locally or 
    latest is set to True, it downloads the file. The function 
    looks for category of the domain name in the Phishtank file 
    for each domain. When no match is found, it returns an 
    empty string.

    Args:
        df (:obj:`DataFrame`): Pandas DataFrame. No default value.
        domain_names (str): Column name of the domain in DataFrame. 
            Default in `domain_names`.
        year (int): PhishTank data year. Only 2017 data is available.
            Default is 2017.
        latest (Boolean): Whether or not to download latest 
            data available from GitHub. Default is `False`.

    Returns:
        DataFrame: Pandas DataFrame with two additional columns:
            'phish_year_domain' and 'phish_year_cat'
    """

    phish_df = load_phish_data(year, latest)
    if phish_df is not None:
        try:
            col_domain = "phish_{0:04d}_domain".format(year)
            df[col_domain] = df[domain_names].apply(lambda c:
                                                    url2domain(c))
            odf = pd.merge(df, phish_df, how='left',
                           left_on=col_domain, right_on='__domain')
            del odf['__domain']
            return odf
        except KeyError as e:
            print("ERROR: Column {0!s} not found in the input file".format(e))
        except Exception as e:
            print("ERROR: {0!s}".format(e))

    return None


if __name__ == "__main__":
    pass
