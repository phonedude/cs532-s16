import urllib.request
import json

genders = {}

with open('real_names.txt') as f:
	for line in f:
		line = line.replace("(", "")
		line = line.replace(")", "")
		split = line.split(", ")
		username = split[0]
		username = username[1:-1]
		name = split[1]
		# Removing the "u" and " ' " and extra whitespace at end
		name = name[2:-2]
		# Getting only the first names
		name = name.split()[0]
		#print (username, name)
		string = "https://api.genderize.io/?name=" + name
		response = urllib.request.urlopen(string).read()
		#print (response)
		response = response.decode("utf-8")
		json_object = json.loads(response)
		gender = json_object['gender']
		genders[username] = gender

print (json.dumps(genders, indent=4, sort_keys=False))