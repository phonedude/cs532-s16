#!/usr/bin/env python3
import argparse
import re
from collections import deque

import requests
from urllib.parse import urljoin

from bs4 import BeautifulSoup

reg_s = "((([A-Za-z]{3,9}:(?:\/\/)?)(?:[\-;:&=\+\$,\w]+@)?[A-Za-z0-9\.\-]+|" + \
        "(?:www\.|[\-;:&=\+\$,\w]+@)[A-Za-z0-9\.\-]+)((?:\/[\+~%\/\.\w\-]*)?" + \
        "\??(?:[\-\+=&;%@\.\w]*)#?(?:[\.\!\/\\\w]*))?)"

# my standard url regex found a while ago
url_re = re.compile(reg_s, re.IGNORECASE)

relative = re.compile("^(?!www\.|(?:http|ftp)s?://|[A-Za-z]:\\|//).*")

def print_headers(r):
    print("printing headers for url=", r.url)
    for headerk, headerv in r.headers.items():
        print(headerk + ":" + headerv)
    print("++++++++++++++++++++++++++++++")


def ispdf(rq):
    if rq.headers['Content-type'].lower() in 'application/pdf':
        return True
    else:
        return False


def strip_href(request, que, saw):
    try:
        s = BeautifulSoup(request.text, 'html5lib')
    except:
        # just because if this fails there are problems
        s = BeautifulSoup(request.text)
    all_a = s.find_all('a', href=True)

    for link in map(lambda a: a['href'], all_a):
        if link not in saw:
            if url_re.match(link):
                que.append(link)
            else:
                if relative.match(link):
                    link = urljoin(request.url,link)
                    que.append(link)
                else:
                 print("The input uri %s failed to pass my regex " % link, reg_s)
    return s


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("uri", type=str, help="the url to extract from")
    parser.add_argument("-v", help="verbose", action="store_true")
    parser.add_argument("-ph", help="print all headers", action="store_true")

    args = parser.parse_args()

    # your on Ubuntu and you will like it
    useragent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:44.0) Gecko/20100101 Firefox/44.01'
    session = requests.Session()
    session.headers.update({'User-Agent': useragent})
    seen = set()
    q = deque()
    q.append(args.uri)  # ("http://tinyurl.com/gv8jnso")
    uri = q.popleft()

    if re.match(url_re, uri):
        if args.v:
            print("it matches")
    else:
        print("The input uri %s failed to pass my regex " % uri, reg_s)

    request = session.get(uri)
    """:type : requests.Response """
    if ispdf(request):
        print("The link %s was a link to an actual pdf file " % uri,
              ("but it was misleading %s its length is " % request.url)
              if uri != request.url else "its length is",
              request.headers['Content-Length']
              )
        print("No other links are in a pdf have nice day")
        if request.is_redirect or request.is_permanent_redirect:
            print("It was dirty reditect ;)")
        exit()
    soup = strip_href(request, q, seen)
    if args.ph:
        print_headers(request)

    while True:
        try:
            uri = q.popleft()
        except IndexError:
            break
        if re.match(url_re, uri):
            if args.v:
                print("the uri %s was valid" % uri)
        else:
            print("Bad url %s" % uri)
            continue
        seen.add(uri)

        request = session.get(uri)
        """:type : requests.Response """

        if args.ph:
            print_headers(request)

        if ispdf(request):
            if request.ok:
                print("The link %s was a link to an actual pdf file " % uri,
                      ("\n\tbut it was misleading %s its length is " % request.url)
                      if uri != request.url else "its length is",
                      request.headers['Content-Length']
                      )
                continue

        if args.v:
            print("so far I have processed these uris: ", seen)
            print("I still have these to go", q)

        if request.ok:
            print("\nHey were are ok! %i" % request.status_code, "Done going down the rabit hole for %s\n" % uri)
        elif request.is_permanent_redirect or request.is_redirect:
            soup = strip_href(request, q, seen)

    session.close()
