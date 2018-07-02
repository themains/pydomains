PyDomains: Classifying the Content of Domains
------------------------------------------------

.. image:: https://travis-ci.org/themains/pydomains.svg?branch=master
    :target: https://travis-ci.org/themains/pydomains
.. image:: https://ci.appveyor.com/api/projects/status/qfvbu8h99ymtw2ub?svg=true
    :target: https://ci.appveyor.com/project/themains/pydomains
.. image:: https://img.shields.io/pypi/v/pydomains.svg
    :target: https://pypi.python.org/pypi/pydomains
.. image:: https://readthedocs.org/projects/pydomains/badge/?version=latest
    :target: http://pydomains.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

The package provides two broad ways of learning about the kind of content hosted 
on a domain. First, it provides convenient access to curated lists of domain content
like the Shallalist, DMOZ, PhishTank, and such. Second, it exposes models built on top of 
these large labeled datasets; the models estimate the relationship between sequence of 
characters in the domain name and the kind of content hosted by the domain. 


Quick Start
------------

::

    import pandas as pd
    from pydomains import *

    # Get help
    help(dmoz_cat)

    # Load data
    df = pd.read_csv('./pydomains/examples/input-header.csv')

    #  df
    #       label                                url
    #   0   test1                        topshop.com
    #   1   test2                   beyondrelief.com

    # Get the Content Category from DMOZ, phishtank
    df_dmoz  = dmoz_cat(df, domain_names = 'url')
    df_phish = phish_cat(df, domain_names = 'url')

    # Predicted category from shallalist, toulouse
    df_shalla   = pred_shalla(df, domain_names = 'url')
    df_toulouse = pred_toulouse(df, domain_names = 'url')


Installation
--------------

Installation is as easy as typing in:

::

    pip install pydomains

API
~~~~~~~~~~

1. **dmoz\_cat**, **shalla\_cat**, and **phish\_cat**: When the domain
   is in the DMOZ, Shallalist, and Phishtank data, the functions give the
   category of the domain according to the respective list. (Phishtank just
   gives whether or not the domain has been implicated in phishing.) Otherwise,
   the function returns an empty string.

   -  **Arguments:**

      -  ``df``: pandas dataframe. No default.
      -  ``domain_names``: column with the domain names/URLs. 
         Default is ``domain_names``
      -  ``year``. Specify the year from which you want to use the data.
         Currently only DMOZ data from 2016, and Shallalist and Phishtank
         data from 2017 is available.
      -  ``latest``. Boolean. Default is ``False``. If ``True``, the
         function checks if a local file exists and if it exists, if the
         local file is the latest. If it isn't, it downloads the latest
         file from the GitHub link and overwrites the local file.

   -  **Functionality:**

      -  converts domain name to lower case, strips ``http://``.
      -  Looks for ``dmoz_YYYY.csv``, ``shalla_YYYY.csv``, or
         ``phish_YYYY.csv`` respectively in the local folder. If it
         doesn't find it, it downloads the latest DMOZ, Shallalist, or
         Phishtank file from
         `pydomains/data/dmoz_YYYY.csv.bz2 <pydomains/data/dmoz_YYYY.csv.bz2>`__,
         `pydomains/data/shalla_YYYY.csv.bz2 <pydomains/data/shalla_YYYY.csv.bz2>`__,
         or
         `pydomains/data/phish_YYYY.csv.bz2 <pydomains/data/phish_YYYY.csv.bz2>`__\ respectively.
      -  If the ``latest`` flag is planted, it checks if the
         local file is older than the remote file. If it is,
         it overwrites the local file with the newer remote file.

   -  **Output:**

      -  Appends the category to the CSV. By default it creates a column
         (dmoz\_year\_cat or shalla\_year\_cat or phish\_year\_cat).
      -  If no match is found, it returns nothing.
      -  DMOZ sometimes has multiple categories per domain. The
         categories are appended together with a semi-colon.

   -  **Examples:**

      ::
      
          import pandas as pd

          df = pd.DataFrame([{'domain_names': 'http://www.google.com'}])

          dmoz_cat(df)
          shalla_cat(df)
          phish_cat(df)

2. **pred\_shalla**: We use data from Shallalist to train a 
   `LSTM model <pydomains/models/shalla_pred_2017_others.ipynb>`__. The function
   uses the trained model to predict the category of the domain based on 
   the domain name.

   -  **Arguments:**

      -  ``df``: pandas dataframe. No default.
      -  ``domain_names``: column with the domain names/URLs. 
         Default is ``domain_names``
      -  ``year``. Year of the model. Default is 2017. Currently only
         a model based on data from 2017 is available.
      -  ``latest``. Boolean. Default is ``False``. If ``True``, the
         function checks if a local model file exists and if it exists, is it
         older than what is on the website. If it isn't, it downloads the latest
         file from the GitHub link and overwrites the local file.

   -  **Functionality:**

      -  converts domain name to lower case, strips ``http://``.
      -  Uses the model to predict the probability of content being from
         various categories.

   -  **Output**

      -  Appends a column carrying the label of the category with the 
         highest probability (``pred_shalla_year_lab``) and a series of 
         columns with probabilities for each category 
         (``pred_shalla_year_prob_catname``).

   -  **Examples:**

      ::

          pred_shalla(df)

3. **pred\_toulouse**: We use data from http://dsi.ut-capitole.fr/blacklists/ to 
   train a `LSTM model <pydomains/models/toulouse_pred_2017_others.ipynb>`__ that predicts
   the category of content hosted by the domain. The function uses the trained 
   model to predict the category of the domain based on the domain name.

   -  **Arguments:**

      -  ``df``: pandas dataframe. No default.
      -  ``domain_names``: column with the domain names/URLs. 
         Default is ``domain_names``
      -  ``year``. Year of the model. Default is 2017. Currently only
         a model based on data from 2017 is available.
      -  ``latest``. Boolean. Default is ``False``. If ``True``, the
         function checks if a local model file exists and if it exists, is it
         older than what is on the website. If it isn't, it downloads the latest
         file from the GitHub link and overwrites the local file.

   -  **Functionality:**

      -  converts domain name to lower case, strips ``http://``.
      -  Uses the model to predict the probability of it being a domain
         implicated in distributing malware.

   -  **Output:**

      -  Appends a column carrying the label of the category with the 
         highest probability (``pred_toulouse_year_lab``) and a series of 
         columns with probabilities for each category 
         (``pred_toulouse_year_prob_catname``).

   - **Examples:**

      ::

          pred_malware(df)

4. **pred\_phish**: Given the importance, we devote special care to try
   to predict domains involved in phishing well. To do that, we use data
   from `PhishTank <https://www.phishtank.com/>`__ and combine it with
   data from http://s3.amazonaws.com/alexa-static/top-1m.csv.zip, and train a `LSTM
   model <pydomains/models/phish_pred_2017.ipynb>`__. The function gives the 
   predicted probability based on the LSTM model.

   -  **Arguments:**

      -  ``df``: pandas dataframe. No default.
      -  ``domain_names``: column with the domain names/URLs. 
         Default is ``domain_names``
      -  ``year``. Year of the model. Default is 2017. Currently only
         a model based on data from 2017 is available.
      -  ``latest``. Boolean. Default is ``False``. If ``True``, the
         function checks if a local model file exists and if it exists, is it
         older than what is on the website. If it isn't, it downloads the latest
         file from the GitHub link and overwrites the local file.

   -  **Functionality:**

      -  converts domain name to lower case, strips ``http://``.
      -  Uses the model to predict the probability of it being a domain
         implicated in phishing.

   -  **Output:**

      -  Appends column `pred_phish_year_lab` which contains the most probable
         label, and a column indicating the probability that the domain 
         is involved in distributing malware (`pred_phish_year_prob`).

   -  **Examples:**

      ::

          pred_phish(df)

5. **pred\_malware**: Once again, given the importance of flagging domains
   that carry malware, we again devote extra care to try to predict domains 
   involved in distributing malware well. We combine data on malware 
   domains http://mirror1.malwaredomains.com/ with data from 
   http://s3.amazonaws.com/alexa-static/top-1m.csv.zip, and train a 
   `LSTM model <pydomains/models/malware_pred_2017.ipynb>`__. The function gives 
   the predicted probability based on the LSTM model.

   -  **Arguments:**

      -  ``df``: pandas dataframe. No default.
      -  ``domain_names``: column with the domain names/URLs. 
         Default is ``domain_names``
      -  ``year``. Year of the model. Default is 2017. Currently only
         a model based on data from 2017 is available.
      -  ``latest``. Boolean. Default is ``False``. If ``True``, the
         function checks if a local model file exists and if it exists, is it
         older than what is on the website. If it isn't, it downloads the latest
         file from the GitHub link and overwrites the local file.

   -  **Functionality:**

      -  converts domain name to lower case, strips ``http://``.
      -  Uses the model to predict the probability of it being a domain
         implicated in distributing malware.

   -  **Output:**

      -  Appends column `pred_malware_year_lab` and a column indicating the 
         probability that the domain is involved in distributing malware 
         (`pred_malware_year_prob`).

   - **Examples:**

      ::

          pred_malware(df)

Using pydomains
~~~~~~~~~~~~~~~~

::

    >>> import pandas as pd
    >>> from pydomains import *
    Using TensorFlow backend.

    >>> # Get help of the function
    ... help(dmoz_cat)
    Help on function dmoz_cat in module pydomains.dmoz_cat:

    dmoz_cat(df, domain_names='domain_names', year=2016, latest=False)
        Appends DMOZ domain categories to the DataFrame.

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


    >>> # Load an example input with columns header
    ... df = pd.read_csv('./pydomains/examples/input-header.csv')

    >>> df
        label                                url
    0   test1                        topshop.com
    1   test2                   beyondrelief.com
    2   test3                golf-tours.com/test
    3   test4                    thegayhotel.com
    4   test5  https://zonasequravlabcp.com/bcp/
    5   test6                http://privatix.xyz
    6   test7              adultfriendfinder.com
    7   test8            giftregistrylocator.com
    8   test9                 bangbrosonline.com
    9  test10                scotland-info.co.uk

    >>> # Get the Content Category from DMOZ
    ... df = dmoz_cat(df, domain_names='url')
    Loading DMOZ data file...

    >>> df
        label                                url         dmoz_2016_domain  \
    0   test1                        topshop.com              topshop.com
    1   test2                   beyondrelief.com         beyondrelief.com
    2   test3                golf-tours.com/test           golf-tours.com
    3   test4                    thegayhotel.com          thegayhotel.com
    4   test5  https://zonasequravlabcp.com/bcp/     zonasequravlabcp.com
    5   test6                http://privatix.xyz             privatix.xyz
    6   test7              adultfriendfinder.com    adultfriendfinder.com
    7   test8            giftregistrylocator.com  giftregistrylocator.com
    8   test9                 bangbrosonline.com       bangbrosonline.com
    9  test10                scotland-info.co.uk      scotland-info.co.uk

                                        dmoz_2016_cat
    0  Top/Regional/Europe/United_Kingdom/Business_an...
    1                                                NaN
    2                                                NaN
    3                                                NaN
    4                                                NaN
    5                                                NaN
    6                                                NaN
    7                                                NaN
    8                                                NaN
    9  Top/Regional/Europe/United_Kingdom/Scotland/Tr...
    >>> # Predict Content Category Using the Toulouse Model
    ... df = pred_toulouse(df, domain_names='url')
    Loading Toulouse model, vocab and names data file...

    >>> df
        label                                url         dmoz_2016_domain  \
    0   test1                        topshop.com              topshop.com
    1   test2                   beyondrelief.com         beyondrelief.com
    2   test3                golf-tours.com/test           golf-tours.com
    3   test4                    thegayhotel.com          thegayhotel.com
    4   test5  https://zonasequravlabcp.com/bcp/     zonasequravlabcp.com
    5   test6                http://privatix.xyz             privatix.xyz
    6   test7              adultfriendfinder.com    adultfriendfinder.com
    7   test8            giftregistrylocator.com  giftregistrylocator.com
    8   test9                 bangbrosonline.com       bangbrosonline.com
    9  test10                scotland-info.co.uk      scotland-info.co.uk

                                        dmoz_2016_cat  \
    0  Top/Regional/Europe/United_Kingdom/Business_an...
    1                                                NaN
    2                                                NaN
    3                                                NaN
    4                                                NaN
    5                                                NaN
    6                                                NaN
    7                                                NaN
    8                                                NaN
    9  Top/Regional/Europe/United_Kingdom/Scotland/Tr...

    pred_toulouse_2017_domain pred_toulouse_2017_lab  \
    0               topshop.com               shopping
    1          beyondrelief.com                  adult
    2            golf-tours.com               shopping
    3           thegayhotel.com                  adult
    4      zonasequravlabcp.com               phishing
    5              privatix.xyz                  adult
    6     adultfriendfinder.com                  adult
    7   giftregistrylocator.com               shopping
    8        bangbrosonline.com                  adult
    9       scotland-info.co.uk               shopping

    pred_toulouse_2017_prob_adult  pred_toulouse_2017_prob_audio-video  \
    0                       0.133953                             0.003793
    1                       0.521590                             0.016359
    2                       0.186083                             0.008208
    3                       0.971451                             0.001080
    4                       0.065503                             0.001063
    5                       0.986328                             0.002241
    6                       0.939441                             0.000211
    7                       0.014645                             0.000570
    8                       0.945490                             0.004017
    9                       0.256270                             0.003745

    pred_toulouse_2017_prob_bank  pred_toulouse_2017_prob_gambling  \
    0                  1.161209e-04                      2.911613e-04
    1                  3.912278e-03                      6.484169e-03
    2                  1.783388e-03                      8.022175e-04
    3                  8.920387e-05                      6.256429e-05
    4                  6.226773e-04                      1.073759e-04
    5                  6.823016e-07                      1.969112e-06
    6                  1.742063e-07                      6.485808e-08
    7                  3.973934e-04                      1.019526e-05
    8                  9.122109e-05                      1.142884e-04
    9                  3.962536e-04                      4.977396e-04

    pred_toulouse_2017_prob_games  pred_toulouse_2017_prob_malware  \
    0                       0.002073                         0.003976
    1                       0.022408                         0.018371
    2                       0.013352                         0.006392
    3                       0.000713                         0.000934
    4                       0.012431                         0.077391
    5                       0.001021                         0.004949
    6                       0.000044                         0.000059
    7                       0.004112                         0.016339
    8                       0.002216                         0.000422
    9                       0.014452                         0.006615

    pred_toulouse_2017_prob_others  pred_toulouse_2017_prob_phishing  \
    0                        0.014862                          0.112132
    1                        0.046011                          0.172208
    2                        0.021287                          0.060633
    3                        0.005018                          0.017201
    4                        0.031691                          0.416989
    5                        0.003069                          0.002094
    6                        0.001674                          0.058497
    7                        0.015631                          0.131174
    8                        0.017964                          0.012574
    9                        0.057622                          0.111698

    pred_toulouse_2017_prob_press  pred_toulouse_2017_prob_publicite  \
    0                   8.404775e-04                           0.000761
    1                   2.525988e-02                           0.002821
    2                   1.853482e-02                           0.000990
    3                   2.208834e-04                           0.000135
    4                   2.796387e-03                           0.000284
    5                   4.559151e-06                           0.000252
    6                   1.133891e-07                           0.000007
    7                   1.115335e-02                           0.000436
    8                   5.098383e-04                           0.000785
    9                   7.331154e-04                           0.000168

    pred_toulouse_2017_prob_shopping
    0                          0.727203
    1                          0.164577
    2                          0.681934
    3                          0.003094
    4                          0.391121
    5                          0.000038
    6                          0.000066
    7                          0.805531
    8                          0.015817
    9                          0.547802

Models
~~~~~~~~~~~~~~~~

For more information about the models, including the decisions we made around
curtailing the number of categories, see `here <./pydomains/models/>`__

Underlying Data
~~~~~~~~~~~~~~~~

We use data from DMOZ, Shallalist, PhishTank, and a prominent Blacklist aggregator.
For more details about how the underlying data, see `here <./pydomains/data/>`__

Validation
~~~~~~~~~~~~~~~~~

We compare content categories according to the `TrustedSource API <https://www.trustedsource.org>`__ 
with content category from Shallalist and the Shallalist model for all the unique domains in the 
comScore 2004 data: 

1. `comScore 2004 Trusted API results <http://dx.doi.org/10.7910/DVN/BPS1OK>`__

2. `comScore 2004 categories from pydomains <./pydomains/app/comscore-2004.ipynb>`__

3. `comparison between TrustedSource and Shallalist and shallalist model <./pydomains/app/comscore-2004-eval.ipynb>`__

Learning Browsing Behavior Using pydomains
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To make it easier to learn browsing behavior of people, we obtained the type of content
hosted by a domain using all the functions in pydomains for all the unique domains in all 
the comScore data from 2002 to 2016 (there are some missing years). We have posted the data
`here <https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/DXSNFA>`__  

Notes and Caveats
~~~~~~~~~~~~~~~~~~~

-  The DMOZ categorization system at tier 1 is bad. The category names
   are vague. They have a lot of subcategories that could easily belong
   to other tier 1 categories. That means a) it would likely be hard to
   classify well at tier 1 and b) not very valuable. So we choose not to
   predict tier 1 DMOZ categories.

-  The association between patterns in domain names and the kind of
   content they host may change over time. It may change as new domains
   come online and as older domains are repurposed. All this likely
   happens slowly. But, to be careful, we add a ``year`` variable in our
   functions. Each list and each model is for a particular year.

-  Imputing the kind of content hosted by a domain may suggest to some
   that domains carry only one kind of content. Many domains don't. And
   even when they do, the quality varies immensely. (See more `here 
   <https://themains.github.io/index.html#domain_classifier>`__.) There is 
   much less heterogeneity at the URL level. And we plan to look into 
   predicting at URL level. See `TODO <TODO>`__ for our plans.

-  There are a lot of categories where we do not expect domain names to
   have any systematic patterns. Rather than make noisy predictions
   using just the domain names (the data that our current set of 
   classifiers use), we plan to tackle this prediction task with 
   some additional data. See `TODO <TODO>`__ for our plans.

Documentation
-------------

For more information, please see `project documentation <http://pydomains.readthedocs.io/en/latest/>`__.

Authors
~~~~~~~~

Suriyan Laohaprapanon and Gaurav Sood

Contributor Code of Conduct
~~~~~~~~~~~~~~~~~~~~~~~~~~~

The project welcomes contributions from everyone! In fact, it depends on
it. To maintain this welcoming atmosphere, and to collaborate in a fun
and productive way, we expect contributors to the project to abide by
the `Contributor Code of
Conduct <http://contributor-covenant.org/version/1/0/0/>`__

License
~~~~~~~

The package is released under the `MIT
License <https://opensource.org/licenses/MIT>`__.
