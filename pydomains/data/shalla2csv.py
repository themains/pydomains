#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Convert Shallist to CSV format
"""

import os
import sys
import tarfile

import pandas as pd

from pydomains.utils import url2domain, download_file

SHALLALIST_DOWNLOAD_URL = 'http://www.shallalist.de/Downloads/shallalist.tar.gz'
SHALLALIST_TAR_GZ = 'shallalist.tar.gz'
if __name__ == "__main__":
    print("Downloading shallist.tar.gz from www.shallalist.de...")
    download_file(SHALLALIST_DOWNLOAD_URL, SHALLALIST_TAR_GZ)
    print("Processing the domain list...")
    shalla_cats = {}
    tar = tarfile.open(SHALLALIST_TAR_GZ, "r:gz")
    for tarinfo in tar:
        fn = tarinfo.name
        extracted = False
        if tarinfo.isreg():
            if fn.endswith('domains'):
                print("Extracting {0!s}, size = {1:d}...".format(fn, tarinfo.size))
                f = tar.extractfile(tarinfo)
                cat = '/'.join(fn.split('/')[1:-1])
                urls = f.read().split()
                for u in urls:
                    domain = url2domain(u)
                    if domain not in shalla_cats:
                        shalla_cats[domain] = cat
                    else:
                        shalla_cats[domain] += ('|' + cat)
                extracted = True
        elif tarinfo.isdir():
            pass
        else:
            pass
        if not extracted:
            print("Skipping {0!s}, size = {1:d}...".format(fn, tarinfo.size))
    tar.close()
    os.unlink(SHALLALIST_TAR_GZ)
    print("Saving the output to CSV file")
    sdf = pd.DataFrame.from_dict(shalla_cats, orient='index')
    sdf.columns = ['shalla_cat']
    if len(sys.argv) > 1:
        outfn = sys.argv[1]
    else:
        outfn = 'shallalist.csv.bz2'
    sdf.to_csv(outfn, index_label='domain', compression='bz2')
    print('Done')
