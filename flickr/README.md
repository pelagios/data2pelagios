# Pelagios Flickr Photostream Conversions

This Python script converts a Flickr photostream tagged with Pleiades machine tags to Pelagios annotations.

## Setup

* Install the [flickrapi](http://stuvel.eu/flickrapi) module. Use *easy_install flickrapi* if you have [SetupTools](http://pypi.python.org/pypi/setuptools).
  (Note: you can install SetupTools on Linux via _sudo apt-get install python-setuptools_.)
* You need to have a Flickr API key - put the key into a file named 'api-key.txt', so the script can pick it up from there.
* Tweak the user_id in the script - and run
