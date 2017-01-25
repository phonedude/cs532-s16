#!/bin/bash

# test-echo-urls.sh

while read -r full_url
do 
    echo $full_url
    wget -O temp.txt "${full_url}"    
    temp=`echo -n $full_url | md5sum| awk '{ print $1 }'`
    cp temp.txt ./outFiles/"${temp}.raw"
    echo "${full_url}" >> ./outFiles/"${temp}.raw"
    echo "${full_url}" > ./outFiles/"${temp}.processed"
    lynx -dump -force_html temp.txt >> ./outFiles/"${temp}.processed"
done < links.txt
