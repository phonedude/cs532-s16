import csv
import json
from datetime import date

from dateutil.parser import parse

import timemaps


# method to count the number of timemaps for a uri
def count():
    counted = {}
    # for each url in the 1000 urls
    with open("urls.dat", "r") as o:
        for line in o:
	    # remove the newline character
            url = line.rstrip("\n")
            try:
		# get the time map 
                tm = timemaps.TimeMap(url)
		# the number of mementos is the number of keys
                counted[url] = len(tm.mementos.keys())
                print("%s, %i\n" % (url, len(tm.mementos.keys())))
            except:
		# if an exception is raised it means no mementos
                counted[url] = 0
    # write the counts to file
    with open("counted.csv", "w+") as oo:
        oo.write("site,count\n")
        for url, count in counted.items():
            print("%s, %i\n" % (url, count))
            oo.write("%s, %i\n" % (url, count))

# method to count and carbon date the uri mementos
def countAndDate():
    count()
    zero = []
    nonZero = []
    all = {}
    # get todays date
    now = date.today()

    with open("counted.csv", "r") as csvFile:
	# read the count file
        reader = csv.DictReader(csvFile)
        for row in reader:
            print(row)
            print(row["site"], row["count"])
	    # get two collections the nonZero and the zero counts
            if int(row["count"]) > 0:
                nonZero.append(row["site"])
            else:
                zero.append(row["site"])
            all[row["site"]] = row["count"]
    
    # open the json data from carbondate
    jdata = open("dated.json", "r")
    data = json.load(jdata)
    jdata.close()
    cds = {}

    for jd in data:
	# create mapping for the uri to date
        cds[jd['URI']] = parse(jd['Estimated Creation Date'])
        print(jd, type(parse(jd['Estimated Creation Date'])))

    with open("dated.csv", "w+") as out:
        out.write("age,mementos\n")
	# for all nonZero memento write the estimated age in days
        for it in nonZero:
	    # python dates have substraction for dates
	    # to mean the days between two daes
            age = now - date(cds[it].year, cds[it].month, cds[it].day)
            """ :type datetime.timedelta """
            out.write("%s,%s\n" % (age.days, all[it]))
            print(it, age.days, all[it])





if __name__ == "__main__":
    countAndDate()
