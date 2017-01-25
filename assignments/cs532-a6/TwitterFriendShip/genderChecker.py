import csv
import json
from collections import Counter

import networkx as nx
import requests

edgeTGroup = {(0, 0): 0, (0, 1): 1, (0, 2): 2, (0, 3): 3, (1, 0): 4, (1, 1): 5, (1, 2): 6, (1, 3): 7,
              (2, 0): 8, (2, 1): 9, (2, 2): 10, (2, 3): 11,
              (3, 0): 12, (3, 1): 13, (3, 2): 14, (3, 3): 15}

wsdlTwitterHandles = ['machawk1', 'aalsum', 'justinfbrunelle', 'phonedude_mln', 'weiglemc', 'Galsondor',
                      'shawnmjones', 'ibnesayeed', 'LulwahMA', 'yasmina_anwar', 'kaylamarie0110',
                      'maturban1', 'CorrenMcCoy', 'acnwala', 'hanysalaheldeen', 'simplesimon2013', 'fmccown',
                      'mart1nkle1n', 'joansm1th', 'hvdsomp', 'johnaberlin', 'WebSciDL', 'DanMilanko']

digLibHandles = ['internetarchive', 'HistWebArchives', 'TPDL2016', 'UKWebArchive', "NetPreserve", "ijdl",
                 'JCDLConf', 'archiveitorg', "archiveis", "idjl", "webrecorder_io", "tpdl2016", "WOSP2014",
                 "WebArch_RT"]

userToGroup = {}


def getGroup(test):
    g = 0
    if test in wsdlTwitterHandles:
        # print("We have a wsdl person ", test)
        g = 1
    elif test in digLibHandles:
        # print("We have a diglib person",test)
        g = 2
    elif 'odu' in test.lower() or 'monarch' in test.lower() or 'MaceandCrown' in test.lower():
        # print("We have odu",test)
        g = 3
    userToGroup[test] = g
    return g


def getGenders(names):
    '''
    Thanks https://github.com/block8437/gender.py
    The MIT License (MIT)

    Copyright (c) 2013 block8437

    Permission is hereby granted, free of charge, to any person obtaining a copy of
    this software and associated documentation files (the "Software"), to deal in
    the Software without restriction, including without limitation the rights to
    use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
    the Software, and to permit persons to whom the Software is furnished to do so,
    subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
    FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
    COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
    IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
    CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
    '''
    url = ""
    cnt = 0
    for name in names:
        if url == "":
            url = "name[0]=" + name
        else:
            cnt += 1
            url = url + "&name[" + str(cnt) + "]=" + name

    req = requests.get("http://api.genderize.io?" + url)
    results = json.loads(req.text)

    retrn = []
    for result in results:
        if result["gender"] is not None:
            retrn.append((result["gender"], result["probability"], result["count"]))
        else:
            retrn.append((u'None', u'0.0', 0.0))
    return retrn


def splitOrWhole(s):
    # gender only works on first names so split the name
    splitted = s['name'].split(' ')
    # there was a first name
    if len(splitted) > 0:
        return splitted[0]
    else:  # otherwise just give back the original
        return s


class GNode:
    def __init__(self, row, g):
        # name,screenName,imurl
        self.name = row['name']
        self.imurl = row['imurl']
        self.screenName = row['screenname']
        self.indegree = 0
        self.outdegree = 0
        self.gender = g
        self.group = 0

    def to_jdic(self):
        out = {'name': self.name, 'screenName': self.screenName, 'gender': self.gender,
               'indegree': self.indegree, 'outdegree': self.outdegree, "group":self.group}
        return out

    def __str__(self):
        return self.screenName


class GEdge:
    def __init__(self, source, sIndex, target, tIndex, edgeToGroup, sg, tg,cross):
        self.source = source
        self.sIndex = sIndex
        self.target = target
        self.tIndex = tIndex
        self.sGender = sg
        self.tGender = tg
        self.edgeToGroup = edgeToGroup
        self.isCross = cross

    def to_jdic(self):
        out = {'source': self.sIndex, 'sname': self.source, 'target': self.tIndex, 'tname': self.target,
               'egroup': self.edgeToGroup, "cross":self.isCross}
        return out


def getGender():
    with open('wsdltwitterfollwers.csv', "r") as o:
        reader = csv.DictReader(o)
        rrList = []
        rList = []
        for row in reader:
            rList.append(row)
            # be nice to the api so we only send 9 at a time as max is 10
            if len(rList) == 9:
                rrList.append(list(rList))
                rList.clear()
        with(open("wsdlGenderResults2.csv", "w+")) as out:
            out.write("name,screenname,gender,prob\n")
            for rl in rrList:
                result = getGenders(list(map(lambda r: splitOrWhole(r), rl)))
                for gdr, rrl in zip(result, rl):
                    print(gdr)
                    out.write("%s,%s,%s,%f\n" % (rrl['name'], rrl['screenName'], gdr[0], float(gdr[1])))


def check_gender_homophily():
    with open("wsdlfollwerFriends.json", "r+") as r:
        it = json.load(r)

    it = it['followers']

    nlist = []
    ng = {}
    graph = nx.DiGraph()
    genderCounter = Counter()

    with open('wsdlGenderResults2.csv', "r") as o:
        reader = csv.DictReader(o)
        for row in reader:
            if 'None' not in row['gender']:
                nlist.append(row['screenname'])
                n = GNode(row, row['gender'])
                ng[row['screenname']] = row['gender']
                genderCounter[row['gender']] += 1
                genderCounter['peeps'] += 1
                sname = row['screenname']
                n.group = getGroup(sname)
                graph.add_node(row['screenname'], attr_dict={'nclass': n})

    nlist = sorted(nlist)

    for ff in it:
        fflist = []
        screanname = ff['screenname']
        if graph.has_node(screanname):
            for ffFriend in ff['friends']:
                if graph.has_node(ffFriend):
                    fflist.append(ffFriend)
                    cross = 0
                    if  ng[screanname] != ng[ffFriend]:
                        cross = 1
                    graph.add_edge(screanname, ffFriend, attr_dict={'sg': ng[screanname], 'tg': ng[ffFriend], 'cross':cross})

    nGenders = genderCounter['peeps']
    nMale = genderCounter['male']
    nFemale = genderCounter['female']

    p = nMale / nGenders
    q = nFemale / nGenders
    twopq = 2 * p * q
    r= "Total Members of Gender graph: %d\nNumber of males in graph: %d\nNumber of Females in graph: %d"%(nGenders, nMale, nFemale)
    r2= "P value of: %.2f\nQ value of: %.2f\n2pq value of %2f" % (p, q, twopq)


    print("Checking cross edges")
    numCrossGenderEdges = 0
    nEdges = 0
    for source, target, gender in graph.edges(data=True):
        nEdges += 1
        if gender['sg'] != gender['tg']:
            numCrossGenderEdges += 1


    print(r)
    print(r2)
    crossPercent = numCrossGenderEdges/nEdges
    print("Number of edges: %d, Number of cross-gender edges: %d, Percent: %.2f "%(nEdges,numCrossGenderEdges,crossPercent))
    win="Yes"
    if crossPercent == twopq:
        print("2pq(%.2f) == cross edge precentage(%.2f)"%(twopq,crossPercent))
        print("There is no homophily")
        win="No"
    else:
        print("2pq(%.2f) != cross edge precentage(%.2f)"%(twopq,crossPercent))
        print("There is homophily")

    with open("homophillyTest.csv","w+") as out:
        out.write("males,females,nodes,edges,p,q,2pq,crossEdges,crossEdgesP,homophily\n")
        out.write("%d,%d,%d,%d,%d,%.2f,%.2f,%.2f,%d,%.2f,%s"%(nGenders, nMale, nFemale,nGenders,nEdges,p,q,twopq,numCrossGenderEdges,crossPercent,win))

    nodeList = []
    edgeList = []
    for node, ndata in sorted(graph.nodes(data=True), key=lambda x: x[0]):
        # print(node, ndata['nclass'])
        nodeClass = ndata['nclass']
        # print(nodeClass.screenName)
        nodeClass.indegree = graph.in_degree(node)
        nodeClass.outdegree = graph.out_degree(node)
        nodeList.append(nodeClass)
        for source, target,data in graph.edges(node,data=True):
            e = GEdge(source,nlist.index(source),target,nlist.index(target),edgeTGroup[(userToGroup[source],userToGroup[target])],data['sg'],data['tg'],data['cross'])
            edgeList.append(e)


    g = {}
    g['nodes'] = nodeList
    g['links'] = edgeList
    with open("wsdlgraphGender.json","w+") as out:
        out.write(json.dumps(g,default=lambda c:c.to_jdic(),  indent=1))

if __name__ == "__main__":
    check_gender_homophily()
