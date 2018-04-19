# DrupalVersionChecker
A program designed to automatically check for the drupal version of a site or list of sites.

It is written in python3, and therefore requires that python3 be installed in order to run.

[Python3 downloads page](https://www.python.org/downloads/)
## Usage

This program can be used in one of two ways.

`python3 DrupalVersionChecker.py YOURURL.com`  
This will return the Drupal version of YOURURL.com (Or let you know that it is not a Drupal Site)

`python3 DrupalVersionChecker.py -f FILENAME.txt`  
This will run through FILENAME.txt and check for the Drupal version of sites included therein. It assumes that there will be one URL per line.
*Important: Make sure your input file has only one URL per line*

## How it works

Firstly we attempt to pull the sites CHANGELOG.txt file, as this is usually the most accurate way of determining a sites Drupal version.

If this failes, we attempt to aproximate the Drupal version of the site based off of the md5 hash of the drupal.js file. (/misc/drupal.js or /core/misc/drupal.js).
While this doesn't always give us an exact version, it will still definitely determine if a site is a Drupal site, and give a general idea of how up to date it is.