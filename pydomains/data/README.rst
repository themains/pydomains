Pre-processed data files
========================

DMOZ

    We use the DMOZ data from http://www.dmoz.org/. Unfortunately, it's no longer updated.
    DMOZ only has a static mirror site `here <http://dmoztools.net/>`_.
    Hence, we use the data from `dmoz_csv <https://github.com/themains/dmoz_csv/tree/master/data>`_ instead.

Shalla

    Shallalist data can be downloaded from http://www.shallalist.de/ and converted to CSV using the `following script <shalla2csv.py>`__::

        python shalla2csv.py shalla_2017.csv.bz2

PhishTank

    PhishTank data can be downloaded from https://www.phishtank.com/developer_info.php.
    and converted to CSV file using the `following script <phishtank2csv.py>`__ ::

        python phishtank2csv.py phish_2017.csv.bz2
