#! /usr/bin/env python

import pickle
import json

def build_matrix(raw, n):
	"""Builds a matrix from a list of strings where each string
	is a space-separated row of the matrix"""
	matrix = [[0 for y in range(n)] for x in range(n)]
	for idx, line in enumerate(raw):
		for idy, val in enumerate(line.split()):
			matrix[idx][idy] = int(val)
	return matrix

def build_nodes(clubs, names):
	"""Builds a list of nodes represented as a python dict"""
	return [{"id": i, "club": c, "name": names[i]} for i, c in enumerate(clubs)]

def build_links(egraph, cgraph):
	"""Builds a list of links represented as a python dict"""
	links = []
	for idx, line in enumerate(egraph):
		for idy, val in enumerate(line):
			if val == 1:
				links.append({"source": idx, "target": idy, "value": cgraph[idx][idy]})
	return links

if __name__ == '__main__':
	data = pickle.loads(open('karate.pickle').read())['karate']
	clubs = data.vs['Faction']
	names = data.vs['name']

	# Read lines from input data file
	lines = [line.strip() for line in open('karate.txt').readlines()]

	# parse size of nxn matrix
	n = int(lines[1].split()[0].replace('N=', ''))

	# build matrices using input data
	egraph = build_matrix(lines[7:41], n)
	cgraph = build_matrix(lines[41:], n)

	m = {}
	m['nodes'] = build_nodes(clubs, names)
	m['links'] = build_links(egraph, cgraph)
	with open('out.json', 'w') as output:
		output.write(json.dumps(m, indent=1, separators=(',', ': ')))
