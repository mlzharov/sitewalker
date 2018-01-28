import os
import logging
import time
import json
import argparse
from urllib.parse import urlparse, urlunparse
import requests
from bs4 import BeautifulSoup as Soup
from requests.exceptions import RequestException

from urlutils import get_domain, norm, join_parts, remove_params, belongs_to_domain

__author__ = 'Sergey Krushinsky'
__copyright__ = "Copyright 2018"
__license__ = "MIT"
__version__ = "1.0.0"
__email__ = "krushinsky@gmail.com"

ALLOW_SCHEMES = ('http', 'https')
DEFAULT_TIMEOUT = 15.0
DEFAULT_USERAGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:28.0) Gecko/20100101 Firefox/28.0'
DEFAULT_HEADERS = {
    'User-Agent'     : DEFAULT_USERAGENT,
    'Accept'         : 'text/html',
    'Accept-Encoding': 'gzip',
    'Connection'     : 'Keep-Alive',
}
DELAY = 1.0

# Disable HTTP logging
urllib3_logger = logging.getLogger('urllib3')
urllib3_logger.setLevel(logging.CRITICAL)

def make_request(url, session=None):
    '''
    Make GET request. Return requests.response object.
    Raise exception on a network error, bad status code or empty content.
    '''
    logging.debug('Requesting %s...', url)
    resp = session.get(url, timeout=DEFAULT_TIMEOUT, allow_redirects=True)
    logging.info('%s: %s - %s', resp.url, resp.status_code, resp.reason)
    resp.raise_for_status()
    assert hasattr(resp, 'text'), 'Empty content!'
    return resp



def iter_links(soup, domain, filter=None):
    '''Set of normalized links found inside the page.'''
    for a in soup.find_all('a', href=True):
        try:
            # remove parameters and query: we don't need them for site map
            url_parts = remove_params(norm(a['href'], domain))
            if not url_parts[0] in ALLOW_SCHEMES:
                continue
            if filter and not filter(url_parts):
                continue
            yield join_parts(url_parts)
        except Exception as ex:
            logging.warn(ex)


def traverse_function(start_url, depth=None):
    '''
    Return a function, which recursively traverses a site starting
    from given seed URL.
    '''
    session = requests.Session()
    session.headers.update(DEFAULT_HEADERS)
    passed = set()
    domain = norm(start_url)[1]

    def f(url, callback=None, level=0, parent=None):
        if level == depth:
            return
        logging.debug('Visiting %s...', url)
        try:
            resp = make_request(url, session)
            soup = Soup(resp.text, 'lxml')
        except (RequestException, AssertionError) as ex:
            logging.warning(ex)
        else:
            if level > 0:
                callback(parent, url)

            for link in iter_links(soup, domain, filter=lambda x: belongs_to_domain(x, domain)):
                if link in passed or link == url:
                    continue
                f(link, callback, level+1, parent=url)
                passed.add(url)
            time.sleep(DELAY)

    return f


def update_sitemap(map, src_url, dst_url):
    '''Update site map, given parent and child nodes
    '''
    # extract paths
    if not src_url:
        if dst_url:
            map[urlparse(dst_url)[2]] = []
    elif not dst_url:
        if src_url:
            map[urlparse(src_url)[2]] = []
    else:
        src = urlparse(src_url)[2]
        dst = urlparse(dst_url)[2]
        map.setdefault(src, []).append(dst)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Traverse a site')
    parser.add_argument('url', metavar='U', type=str, help='start URL')
    parser.add_argument('-d', '--depth', type=int, default=1, help='depth of traversal')
    parser.add_argument('-o', '--output', type=str, default='sitemap.json', help='output file name')

    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if 'DEBUG_SCRAPER' in os.environ else logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S',
        format='%(asctime)s - %(levelname)-8s - %(message)s',)
    try:
        map = {}
        start = join_parts(remove_params(norm(args.url)))
        traverse = traverse_function(start, args.depth)
        traverse(start, lambda *args: update_sitemap(map, *args) )
        # save result to json file
        with open(args.output, 'w') as f:
            json.dump(map, f, indent=4, sort_keys=True, ensure_ascii=False)
    except KeyboardInterrupt:
        logging.warn('Interrupted.')
    except Exception as ex:
        logging.error(ex, exc_info=True)
    else:
        logging.info('Result saved to %s', args.output)
