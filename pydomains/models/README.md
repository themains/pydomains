## PyDomains: Classifying the Content of Domains

We use LSTM to estimate the relationship between the characters in the domain name and the category of content it hosts. We first break down the domain name into common bi-chars and then learn patterns in sequences of common bi-chars.

### Performance

For model performance and comparison to Random Forest and SVC models, see the relevant notebooks and `eps images of the ROC <./pydomains/models/roc>`__.

### Calibration

We also checked if the probabilities were calibrated. We find LSTM to be pretty well calibrated. The notebooks are posted `here <./pydomains/models/calibration/>`__

### Shallalist

In shallalist, a few domains are assigned to multiple categories. We ignore those. We only look at domain names that have been assigned to one category. The other issue with shallalist is that some of the categories don't have many domains. To learn models that have high accuracy and recall, we subset on categories that have more than a 1,000 unique domain names. We also take out categories where the recall is < .3 --- suggesting there is little systematic pattern to the domain names (at least based on the kinds of patterns our model can detect). This leaves us with 30 categories. We consign rest of the domains to the 'other' category.

### Toulouse

* We estimate the model using UT 1 data from http://dsi.ut-capitole.fr/blacklists/index_en.php. We limit our data to categories that make sense:
  1. adult    1870741
  2. audio-video 2977
  3. bank  1689
  4. gambling  1012
  5. games 9357
  6. malware 4463
  7. others  17373 --- placeholder for all other domains
  8. phishing  62712
  9. press 4410
  10. publicite 1091
  11. shopping  36331

### Phish

Phishing URLs are crafted in a way to mimic URLs of popular sites. For instance, there are bunch that have the word 'paypal' in them. So rather than use Common Crawl, we use Alexa top 1M domains as the source of 'legitimate domains.' In particular, we use 50,000 unique domains from PhishTank year 2016-2017, and pair it with the top 50,000 most visited domains from the 1M Alexa domain list.

### Malware

We add 50k samples from Alexa top 1M domains to the roughly 15k Malware domains.

### Using the Models

Before applying the models to data that looks different from what the models were trained on, we recommend getting getting some new 'training' data to get an estimate of the measurement error. The training data can also be used to choose appropriate cut-offs for classification. For instance, phishing URLs are not common in browsing data. And precision/recall tradeoff can be crucial.
