import os
import subprocess
pth = '/Users/mohamedshaaban/Desktop/Tarek_Fouda/'
text_files=[f for f in os.listdir(pth) if f.endswith('.txt')]
i= 0
while (i<len(text_files)-1):
	with open(text_files[i]) as fil:
		proc = subprocess.Popen(["lynx -dump -force_html "+ text_files[i] +"> " + text_files[i] + ".proccesed"], stdout=subprocess.PIPE, shell=True)

		(out, err) = proc.communicate()

	i=i+1