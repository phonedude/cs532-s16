#!/usr/bin/env python3
from pygraphml import GraphMLParser

if __name__ == "__main__":

    # well that was easy look what have here a parser!
    # create a new graph parser
    parser = GraphMLParser()
    # get the graph
    g = parser.parse("mln.graphml")

    # set up how we keep track of everything
    friendCounter = {}
    mlnFCount = 0

    # extract the data by simply looping through the data
    for node in g.nodes():
        try:
            print(node['name'], node['friend_count'])
            name = node['name']
            fcount = node['friend_count']
            friendCounter[name] = fcount
            # glorious leader has one more friend
            mlnFCount += 1
        except KeyError:
            print("bad key", node['name'])

    # add out glorious leader
    friendCounter["mln"] = str(mlnFCount)
    print(mlnFCount)

    # write out findings to a file
    with open("mlnfbcount.csv", "w+") as out:
        out.write("friend,fcount\n")
        for fc in friendCounter.items():
            out.write("%s,%s\n" % fc)
