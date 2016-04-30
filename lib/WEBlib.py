import os
import requests
import urllib3
import socket
import re
import json
from datetime import datetime
from io import StringIO

__author__ = 'Plinio H. Vargas'
__date__ = 'Thu,  Feb 04, 2016 at 08:58:56'
__email__ = 'pvargas@cs.odu.edu'
__modified__ = 'hu,  Feb 04, 2016 at 09:20:22'


def AddURI(uriList, uri):
    """
    :param uriList: List containing links for ultimate location of any
                    given URI.
    :param uri: URI which ultimate location wants be found.
    :return: Update List containing location of any redirected URI

    Given an URI this function finds final location of any given URI, regardless
    if it is redirected. If URI is not found, then list of valid URIs is not updated.
    """
    try:
        r = requests.get(uri, timeout=2.0)
        if r.status_code == 200:
            if r.history:
                final_link = r.history[len(r.history) - 1].headers['location']
                print(final_link)

            else:
                final_link = uri
                print(uri)

            uriList.add(final_link)
        else:
            print(r.status_code, uri)

    except requests.exceptions.SSLError:
        print('Couldn\'t open: %s. URL requires authentication.' % uri)
    except requests.exceptions.ConnectionError:
        print('Couldn\'t open: %s. Connection refused.' % uri)
    except requests.exceptions.TooManyRedirects:
        print('Unable to locate: %s. Exceeded 30 redirects.' % uri)
    except urllib3.exceptions.LocationParseError:
        print('Failed to parse: %s' % uri)
    except requests.exceptions.Timeout:
        print('Have no time for: %s. It\'s taking too long.' % uri)
    except socket.timeout:
        print('Socket Connection with %s timeout.' % uri)

    return


def MementoCount(directory, output, sample_size):
    """
    :param directory:  Relative path where memento files are located
    :param output: Path were histogram data will be written
    :param sample_size: Number of URIs that were sampled
    :return: void. Function data is written to output file

    Given a directory where all memento files are located, opens each
    file and counts number of mementos. Keeps a dictionary to create
    a histogram data of mementos per file. Dictionary is written into output
     file.
    """
    data = {0: sample_size}

    for dirpath, dirname, filenames in  os.walk(directory):
        print(filenames )

    for mementofile in filenames:
        counter = GetNumberMementos(directory + '/' + mementofile)

        data[0] -= 1
        if counter in data:
            data[counter] += 1
        else:
            data[counter] = 1

        # for debugging
        # print(counter)

    with open(output, 'w') as out:
        out.write('No-URI\tcount\n')
        for counter in data:
            out.write('%d\t%d\n' % (data[counter], counter))

    return


def GetNumberMementos(filename):
    """
    :param filename: Name of file to count number of mementos
    :return: number of mementos
    """
    with open(filename, 'r') as file:
        text = file.read()

    return len(re.findall(r'rel=\"memento\"', text))


def GetURIage(json_data):
    """
    :param json_data: JSON object containing URI estimated creation date
    :return: number of days from creation. If Null there is not an estimated
    creation date.


    """

    if json_data['Estimated Creation Date']:
        # data['Estimated Creation Date'] format  is 2016-02-06T03:36:33

        my_date= datetime.strptime(json_data['Estimated Creation Date'], "%Y-%m-%dT%H:%M:%S")
        return (datetime.now()-my_date).days

    return None


def Text2Json(text):
    """
    :param text: text to be converted into JSON object
    :return: JSON object

    """
    text = text.replace("\n", "")    # remove all new line characters
    result = re.search("(?=\{)(.*)\}", text)

    if not result:
        return None

    io = StringIO(result.group())   # convert string into json format

    return json.load(io)            # python dictionary containing JSON object
