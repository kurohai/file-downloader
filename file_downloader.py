#!/bin/env python

import os
import sys
import requests
import logging
from pprint import pprint


# logging setup
# change log_level to increase or decrease log output
# logging.DEBUG, logging.ERROR, logging.WARN
log_level = logging.INFO

log = logging.getLogger(__name__)
streamHandler = logging.StreamHandler()
log.setLevel(log_level)
streamHandler.setLevel(log_level)
log.addHandler(streamHandler)


# usage printed out after error
usage = """
Small script to download a web page and replace words and phrases.
URL should be wrapped in double quotes if special characters are used.
Search and replace string can be single words, or phrases in double quotes.

usage: python file_downloader.py <url> <search string> <replace string>

example: python file_downloader.py lipsum.com "Lorem Ipsum" "stuff and things"
example: python file_downloader.py "http://lipsum.com/" "Lorem Ipsum" "stuff and things"
"""

def get_page(url):
    """
    Downloads the web page at url provided and returns full, unformatted html.
    Prepends HTTP if not provided.
    If HTTPS is required supply it in the command line in double quotes.
    Example: "https://encrypted.google.com"
    """

    # url formatting
    if not url.lower().startswith('http'):
        url = 'http://{u}'.format(u=url)

    log.info('Downloading source of {0}'.format(url))
    result = requests.get(url)

    if result.ok:
        log.info('Download elapsed time: {0}'.format(result.elapsed))
    else:
        log.error('Error during download.')
        log.error('Error: {0}'.format(result.status_code))
        log.error(result.content)
        log.error('URL requested: {0}'.format(result.url))
        sys.exit(1)

    return result.content


def process_page(page, search_str, replace_str):
    """
    Parses html, counts occurrences of search string,
    and replaces each occurrence with replace string.
    """

    log.info('Parsing...')

    log.info(
        'Found {c} occurrences of "{s}"'.\
        format(c=page.count(search_str), s=search_str)
    )

    new_page = page.replace(search_str, replace_str)

    log.info(
        'Replaced all occurrences of "{s}" with "{r}"'.\
        format(s=search_str, r=replace_str)
    )

    return new_page


def parse_inputs(args):
    """Parse positional inputs provided at command line."""

    try:
        url = args[1]
        file_name = get_file_name(url)
    except IndexError:
        log.error('No url supplied. Exiting.')
        log.warning(usage)
        sys.exit(1)

    try:
        search_str = args[2]
    except IndexError:
        log.error('No search string supplied. Exiting.')
        log.warning(usage)
        sys.exit(1)

    try:
        replace_str = args[3]
    except IndexError:
        log.error('No replace string supplied. Exiting.')
        log.warning(usage)
        sys.exit(1)

    return url, search_str, replace_str, file_name


def get_file_name(url):
    """
    Formats url into a friendly file name.
    """

    file_name = url.replace('http://', '')
    file_name = file_name.replace('https://', '')

    if '/' in file_name:
        temp_name = file_name.split('/')
        file_name = temp_name[0]

    file_name = '{0}.html'.format(file_name)
    pwd = os.path.abspath(os.curdir)
    file_name = os.path.join(pwd, file_name)

    return file_name
    

def main(args):
    """
    Small script to download a web page and replace words and phrases.
    URL should be wrapped in double quotes if special characters are used.
    Search and replace string can be single words, or phrases in double quotes.

    usage: python file_downloader.py <url> <search string> <replace string>

    example: python file_downloader.py lipsum.com "Lorem Ipsum" "stuff and things"
    example: python file_downloader.py "http://lipsum.com/" "Lorem Ipsum" "stuff and things"
    """

    url, search_str, replace_str, file_name = parse_inputs(args)

    log.debug('url: {0}'.format(url))
    log.debug('search string: {0}'.format(search_str))
    log.debug('replace string: {0}'.format(replace_str))

    page = get_page(url)

    log.debug('page html:\n{0}'.format(page))

    with open(file_name, 'w') as f:
        f.write(process_page(page, search_str, replace_str))

    log.info('Results written to {0}'.format(file_name))


if __name__ == '__main__':
    main(sys.argv)
