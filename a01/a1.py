import locale
import sys
import requests
import validators
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from time import strftime, localtime, time

"""
This Python program
  1. takes as a command line argument a web page
  2. extracts all the links from the page
  3. lists all the links that result in PDF files, and prints out
     the bytes for each of the links.  (note: be sure to follow
     all the redirects until the link terminates with a "200 OK".)
"""
__author__ = 'Plinio H. Vargas'
__date__ = 'Thu,  Jan 21, 2016 at 22:22:11'
__email__ = 'pvargas@cs.odu.edu'


def main(url):
    locale.setlocale(locale.LC_ALL, 'en_US.utf8')
    # record running time
    start = time()
    print('Starting Time: %s' % strftime("%a,  %b %d, %Y at %H:%M:%S", localtime()))
    print('Extracting pdf links from: %s\n' % url)

    # get uri status
    if requests.get(url).status_code != 200:
        print('\n\nURI is not available from SERVER. Verify URI.\n')
        return

    # get source from URI
    page = requests.get(url).text

    # get parse hostname from URI
    url = 'http://' + urlparse(url).netloc

    # create BeautifulSoup Object
    soup = BeautifulSoup(page, 'html.parser')

    # place source link into list
    all_links = []
    for link in soup.find_all('a'):
        uri = link.get('href')
        # include hostname if url is provided by reference
        if ((len(uri) > 6 and uri[:7].lower() != 'http://') or len(uri) < 7) and uri[:8].lower() != 'https://':
            if uri[:2] == '//':    # if url has double backslash then url is not provided by reference
                uri = 'http:' + uri
            elif uri[0] != '/':    # include backslash if it was not include by reference
                uri = url + '/' + uri
            else:
                uri = url + uri

        # for debugging
        # print(uri)

        try:
            r = requests.get(uri)
            if 'Content-Type' in r.headers and r.headers['Content-Type'] == 'application/pdf':
                if r.status_code == 200:
                    # ensure server provides Content-Length
                    try:
                        all_links.append((uri, r.headers['Content-Length']))
                    except KeyError:
                        # make Content-Length unknown
                        r.headers['Content-Length'] = '???'
                        all_links.append((uri, r.headers['Content-Length']))
        except requests.exceptions.SSLError:
            print('Couldn\'t open: %s. URL requires authentication.' % uri)
        except requests.exceptions.ConnectionError:
            print('Couldn\'t open: %s. Connection refused.' % uri)

    print('\n\nList of all PDFs Links:')
    print('-' * len('List of all PDFs Links'))

    pdf_links = set(all_links)
    all_links = list(pdf_links)
    if len(all_links) > 0:
        for i in range(len(pdf_links)):
            if all_links[i][1] == '???':
                # don't format Content-Lenght
                print('%s, File Size: %s bytes' % (all_links[i][0], all_links[i][1]))
            else:
                print('%s, File Size: %s bytes' % (all_links[i][0],
                                                  locale.format("%d", int(all_links[i][1]), grouping=True)))
    else:
        print('No PDFs links for above URI.')

    print('\nEnd Time:  %s' % strftime("%a,  %b %d, %Y at %H:%M:%S", localtime()))
    print('Execution Time: %.2f seconds' % (time()-start))
    return

if __name__ == '__main__':
    # checks for argument
    if len(sys.argv) != 2:
        print('Please, provide url\nUsage: python3 a1.py [url]')
        sys.exit(-1)
    if not validators.url(sys.argv[1]):
        print('URL is invalid, please correct url and try again')
        sys.exit(1)

    # call main
    main(sys.argv[1])

    sys.exit(0)
