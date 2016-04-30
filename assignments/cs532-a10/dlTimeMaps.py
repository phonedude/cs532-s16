import requests
import urllib
import urllib.parse
from urllib.parse import urlparse

# download the timemaps from A2 Q2 and log the non 200 reponses
if __name__ == "__main__":
    useragent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:44.0) Gecko/20100101 Firefox/44.01'

    with requests.session() as session:
        session.headers.update({'User-Agent': useragent})
        with open("datafiles/thousand.dat", "r+") as ruri:
            with open("datafiles/non200.csv","w+") as n200:
                n200.write("urir,status_code\n")
                for uri in map(lambda l: l.rstrip("\n"), ruri):
                    print(uri)
                    response = session.get("http://mementoproxy.cs.odu.edu/aggr/timemap/link/1/%s" % uri) # type: requests.Response
                    print(response.status_code)
                    response.close()
                    parsed = urlparse(uri)
                    if response.status_code == 200:
                        with open("timemaps/%s.timemap"%parsed.netloc,"w+") as tout:
                            tout.write(response.text)
                    else:
                        n200.write("%s,%d\n"%(uri,response.status_code))
