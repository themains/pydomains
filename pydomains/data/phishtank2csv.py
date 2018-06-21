#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Download PhishTank and pre-processed to CSV format
"""

import os
import sys

import pandas as pd

from pydomains.utils import url2domain, download_file

PHISHTANK_DOWNLOAD_URL = 'http://data.phishtank.com/data/online-valid.csv.bz2'
PHISHTANK_CSV_BZ2 = 'phishtank-online-valid.csv.bz2'

if __name__ == "__main__":
    print("Downloading online-valid.csv.bz2 from www.phishtank.com...")
    download_file(PHISHTANK_DOWNLOAD_URL, PHISHTANK_CSV_BZ2)
    df = pd.read_csv(PHISHTANK_CSV_BZ2)
    df['domain'] = df.url.apply(lambda c: url2domain(c))
    os.unlink(PHISHTANK_CSV_BZ2)
    print("Saving the output to CSV file")
    if len(sys.argv) > 1:
        outfn = sys.argv[1]
    else:
        outfn = 'phishtank.csv.bz2'
    df.to_csv(outfn, index=False, compression='bz2')
    print('Done')
