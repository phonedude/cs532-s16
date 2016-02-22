i = 0;
while read line; do
	echo $line
	curl $line > "$i";
	lynx -dump -force_html "$i" > "$i.processed"
	((i+=1));
done < 1000_unique_links.txt
