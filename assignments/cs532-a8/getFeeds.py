import json as jjson
import re
from operator import add
import os
import feedparser
import nltk
import requests
from bs4 import BeautifulSoup
from functional import seq
from nltk.corpus import stopwords

fmeasure = "http://f-measure.blogspot.com/feeds/posts/default?max-results=200"
fmeasure_next = "https://www.blogger.com/next-blog?navBar=true&blogID=3471633091411211117"
wsdl = "http://ws-dl.blogspot.com/feeds/posts/default?max-results=200"
bspot_feed = "/feeds/posts/default?max-results=200"

# nuke all none-alpha chars
removeExtra = re.compile('[^a-zA-Z]')

langs = ["dutch", "finnish", "german", "italian", "portuguese", "spanish", "turkish", "danish", "english",
         "french", "hungarian", "norwegian", "russian", "swedish"]
langStopWords = {}
for lang in langs:
    langStopWords[lang] = stopwords.words(lang)


def check_next(text):
    # check for the next button ie pagination of blog pages
    soup = BeautifulSoup(text, "lxml-xml")
    next_page = soup.find_all('link', attrs={'type': 'application/atom+xml', 'rel': 'next'})
    # if there is a next page our next_page list will always be 1 otherwise its 0
    # that means we have consumed all the pages for the blog
    if len(next_page) > 0:
        nl = next_page[0].attrs['href']
        return True, nl
    return False, None


def process_text(text):
    # clean text
    t = removeExtra.sub(' ', BeautifulSoup(text.summary, 'html5lib').text).lower()
    ret = []
    # tokenize according to word and emit word if it is not a stopword
    for word in nltk.word_tokenize(t):
        if word not in langStopWords['english']:
            ret.append(word)
    return ret


def consume_all(start, sesh):
    # the text of the entry titles
    text = []
    # the request for the first page of the blogs atom feed
    r = sesh.get(start)  # type: requests.Response
    # parse the feed
    feed = feedparser.parse(r.text)  # type: feedparser.FeedParserDict
    # some blogs do not have titles so I must check for them
    try:
        t = feed['feed']['title']
    except KeyError as e:
        # some blogs do not have a title so I will skip them
        print(e)
        r.close()
        return None
    # see if we have more feed pages
    good, nl = check_next(r.text)

    if len(feed.entries) < 25:
        return None
    # All these operations are very good for more of a functional approach
    # to much work otherwise
    '''
    flatmap:
        for entry <- feed, token <- process_text(entry): yeild token
    '''
    text.extend(seq(feed.entries).flat_map(process_text).to_list())
    while good:
        r = sesh.get(nl)
        feed = feedparser.parse(r.text)
        r.close()
        text.extend(seq(feed.entries).flat_map(process_text))
        good, nl = check_next(r.text)

    # since the number of words can become extremely large we need to do a
    # reduce before emitting the words
    text = seq(text).map(lambda word: (word, 1)) \
        .reduce_by_key(add) \
        .order_by(lambda x: x[1]).to_dict()

    return {'title': t, 'text': text}


def get98(sesh):
    the98 = {}
    counter = 0
    while counter < 98:
        r = sesh.get(fmeasure_next)  # type: requests.Response
        rurl = r.url[:r.url.rindex("/")]
        # I had the random button give the same blog 68 times before
        # so I will simply look for another one if I have seen it before
        if the98.get(rurl, None) is not None:
            r.close()
            print("Processed URL already %s" % rurl)
            continue
        else:
            print(r.url[:r.url.rindex("/")])
        got = consume_all(rurl + bspot_feed, sesh)
        # if the consuming of the feed was bad choose another
        if got is None:
            r.close()
            print("continuing on in get98")
            continue
        the98[rurl] = got
        counter += 1
        print(counter)
        r.close()
    return the98


def getData():
    data = {}
    # have a useragent so we do not look like a robot
    useragent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0'
    session = requests.Session()  # type: requests.Session
    session.headers.update({'User-Agent': useragent})
    try:
        # get the data
        wsdldata = consume_all(wsdl, session)
        data[wsdldata['title']] = wsdldata['text']
        fmeasuredata = consume_all(fmeasure, session)
        data[fmeasuredata['title']] = fmeasuredata['text']
        data98 = get98(session)
        # write out the uris used for the 98 other blogs
        with open("98bloguris.dat", "w+") as out:
            for url, d in data98.items():
                data[d['title']] = d['text']
                out.write("%s\n" % url)
        session.close()
        # write out our data to json
        with open("blogdata.json", "w+") as out:
            out.write(jjson.dumps(data, indent=1))

    except Exception as e:
        print(e)
        session.close()


if __name__ == "__main__":
    if not os.path.exists(os.getcwd()+"/datafiles"):
        os.makedirs(os.getcwd()+"/datafiles")
    getData()

