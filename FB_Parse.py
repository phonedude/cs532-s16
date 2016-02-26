from xml.dom import minidom 
import os
dir = r'F:\Web_Science\cs532-s16\A4'
os.chdir(dir)
xmlDoc = minidom.parse("mln.graphml")
graph = xmlDoc.getElementsByTagName("graph")[0] #returns list
nodes = graph.getElementsByTagName("node")
friends = open("friends.csv","a")
noFriends = open("noFriends.txt","a")
friends.write("Friend_Count\n")
noFriends.write("Has No Friends!\n")
for node in nodes:
    data = node.getElementsByTagName("data")
    if len(data) == 4:
        attrib = node.attributes["id"]
        attrName = attrib.value
        noFriends.write("%s\n"%attrName)
    for d in data:
        a = d.attributes["key"]
        val = a.value
        if val == "friend_count":
            friends.write("%s\n"%d.firstChild.data)
            