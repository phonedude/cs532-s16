import sys
import requests
import validators
import locale
from urllib.parse import urlparse
from bs4 import BeautifulSoup


def main(url):

    print('\nExtracting all pdf links from: %s' % url)

    if requests.get(url).status_code != 200:
        print('\nURL not Found!\n')
        return
    page = requests.get(url).text
    url = 'http://' + urlparse(url).netloc
	
    soup = BeautifulSoup(page, 'html.parser')
    all_links = []
    for link in soup.find_all('a'):
        urls = link.get('href')
        if ((len(urls) > 6 and urls[:7].lower() != 'http://') or len(urls) < 7) and urls[:8].lower() != 'https://':
            if urls[:2] == '//':
                urls = 'http:' + urls
            elif urls[0] != '/':    
                urls = url + '/' + urls
            else:
                urls = url + urls

        try:
            r = requests.get(urls)
            if 'Content-Type' in r.headers and r.headers['Content-Type'] == 'application/pdf':
                if r.status_code == 200:
                    try:
                        all_links.append((urls, r.headers['Content-Length']))
                    except KeyError:
                        r.headers['Content-Length'] = '???'
                        all_links.append((urls, r.headers['Content-Length']))
        except requests.exceptions.SSLError:
            print('Couldn\'t open: %s. URL requires authentication.' % urls)
        except requests.exceptions.ConnectionError:
            print('Couldn\'t open: %s. Connection refused.' % urls)

    print('\nList of all PDFs Links:')

    pdf_links = set(all_links)
    all_links = list(pdf_links)
    if len(all_links) > 0:
        for i in range(len(pdf_links)):
            if all_links[i][1] == '???':
                print('%s, File Size: %s bytes \n' % (all_links[i][0], all_links[i][1]))
            else:
                print('%s, File Size: %s bytes \n' % (all_links[i][0],
                                                  locale.format("%d", int(all_links[i][1]), grouping=True)))
    else:
        print('\nNo PDFs links for above URL.')

    return

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('\nUsage: python q2.py [url]')
        sys.exit(-1)
    if not validators.url(sys.argv[1]):
        print('URL is Invalid, Please try again')
        sys.exit(1)
    main(sys.argv[1])
    sys.exit(0)
