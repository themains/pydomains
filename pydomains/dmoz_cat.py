#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Get the category of content hosted by the domain according to the DMOZ database
"""

import os

import pandas as pd

from .utils import (url2domain, get_app_file_path, download_file,
                    DATA_BASE_URL)


def load_dmoz_data(year, latest=False):
    data_fn = 'dmoz_{0:d}.csv.bz2'.format(year)
    data_path = get_app_file_path('pydomains', data_fn)
    if not os.path.exists(data_path) or latest:
        print("Downloading DMOZ data from the server ({0!s})..."
              .format(data_fn))
        if not download_file(DATA_BASE_URL + data_fn, data_path):
            print("ERROR: Cannot download DMOZ data file")
            return None
    else:
        print("Using cached DMOZ data from local ({0!s})...".format(data_path))
    print("Loading DMOZ data file...")
    df = pd.read_csv(data_path, usecols=['domain', 'cat_labels_en', 'rdomain'])
    df.columns = ['__domain', 'dmoz_{0:04d}_cat'.format(year), '__rdomain']
    return df


def dmoz_cat(df, domain_names="domain_names", year=2016, latest=False):
    """Appends DMOZ domain categories to the DataFrame.
    
    The function extracts the domain name along with the subdomain 
    from the specified column and appends the category (dmoz_cat) 
    to the DataFrame. If DMOZ file is not available locally or 
    latest is set to True, it downloads the file. The function 
    looks for category of the domain name in the DMOZ file 
    for each domain. When no match is found, it returns an 
    empty string.

    Args:
        df (:obj:`DataFrame`): Pandas DataFrame. No default value.
        domain_names (str): Column name of the domain in DataFrame. 
            Default in `domain_names`.
        year (int): DMOZ data year. Only 2016 data is available.
            Default is 2016.
        latest (Boolean): Whether or not to download latest 
            data available from GitHub. Default is False.

    Returns:
        DataFrame: Pandas DataFrame with two additional columns:
            'dmoz_year_domain' and 'dmoz_year_cat'
    """

    dmoz_df = load_dmoz_data(year, latest)
    if dmoz_df is not None:
        try:
            col_domain = "dmoz_{0:04d}_domain".format(year)
            col_cat = "dmoz_{0:04d}_cat".format(year)
            df[col_domain] = df[domain_names].apply(lambda c:
                                                    url2domain(c))
            dmoz_cols = ['__domain', col_cat]
            odf = pd.merge(df, dmoz_df[dmoz_cols], how='left',
                           left_on=col_domain, right_on='__domain')
            del odf['__domain']
            dmoz_df.drop_duplicates('__rdomain', inplace=True)
            dmoz_cols = ['__rdomain', col_cat]
            odf = pd.merge(odf, dmoz_df[dmoz_cols], how='left',
                           left_on=col_domain, right_on='__rdomain')
            del odf['__rdomain']
            cat_xy = [col_cat + '_x', col_cat + '_y']
            odf[col_cat] = odf[cat_xy].apply(lambda r: r[0]
                                             if pd.isnull(r[1]) else r[1],
                                             axis=1)
            odf.drop(cat_xy, axis=1, inplace=True)
            return odf
        except KeyError as e:
            print("ERROR: Column {0!s} not found in the dataframe".format(e))
        except Exception as e:
            print("ERROR: {0!s}".format(e))

    return df


if __name__ == "__main__":
    pass
