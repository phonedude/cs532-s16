import requests
import csv

# get set of unique urls
def unique():
    s = set()
    with open("urls.dat","r") as o:
        for line in o:
            url = line.rstrip("\n")
            s.add(url)
    with open("urls.dat","w+") as write:
        for url in sorted(s):
            write.write("%s\n"%url)

# get the real urls for shortened ones
def uniqueShortened():
    useragent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:44.0) Gecko/20100101 Firefox/44.01'
    session = requests.Session()
    session.headers.update({'User-Agent': useragent})
    s = set()
    c = 0

    with open("shortenedURLS.txt", "r") as o:
        for line in o:
            url = line.rstrip("\n")
            try:
                r = session.get(url)
                """:type : requests.Response """
		# if status code is 200 then we have a good link
                if r.status_code == 200:
		    # add it our set of urls
                    s.add(r.url)
                    c += 1
                    print(c)
            except:
                continue

    print(len(s))
    print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

    session.close()
    with open("urls2.dat", "w+") as write:
        for url in sorted(s):
            print(url)
            write.write("%s\n" % url)


# method to write out the zero and non-zero memento count urls
def zeroNoneZero():
    # count()
    zero = []
    nonZero = []

    with open("counted.csv", "r") as csvFile:
        reader = csv.DictReader(csvFile)
        for row in reader:
            print(row)
            print(row["site"], row["count"])
            if int(row["count"]) > 0:
                nonZero.append(row["site"])
            else:
                zero.append(row["site"])

    with open("nonZero.txt", "w+") as onz:
        for site in nonZero:
            onz.write("%s\n" % site)

    with open("zero.txt", "w+") as zo:
        for site in zero:
            zo.write("%s\n" % site)
