import xml.etree.ElementTree as ET
import re

if __name__ == "__main__":
	tree = ET.parse('updated_mln.graphml')
	root = tree.getroot()

	graphml = {
	"graph": "{http://graphml.graphdrawing.org/xmlns}graph",
	"node": "{http://graphml.graphdrawing.org/xmlns}node",
	"data": "{http://graphml.graphdrawing.org/xmlns}data",
	"friend_count": "{http://graphml.graphdrawing.org/xmlns}data[@key='friend_count"
	}

	graph = tree.find(graphml.get("graph"))
	nodes = graph.findall(graphml.get("node"))

	friend_counts = []

	for node in nodes:
		attribs = {}
		for data in node.findall(graphml.get('data')):
			attribs[data.get('key="friend_count"')] = data.text

		friend_counts.append(map(int, re.findall('\d+', attribs[data.get('key="friend_count')])))

	print friend_counts