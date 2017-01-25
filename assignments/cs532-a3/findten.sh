#!/bin/bash

#where are we
cwd=$(pwd)

#our processed dir should be near
cwd="$cwd/processed/"
echo $cwd

#output file
file="tfidftable.csv"

if [ -f $file ] 
then
   echo "File $file exists. Deleting and remaking"
   rm $file
fi

touch $file

#output first line of csv file
$(echo "tfidf,tf,idf,uri" >> $file)

#for each choosen hash 
for f in $(cat "tenForTFID.txt")
do
 #file location of choosen hash 
 p="$cwd$f"
 #get the word count for it. Only want the count
 wdCount=$(wc -w $p| awk '{print $1}')
 # redo the termCount
 termCount=$(grep -c -i "Bernie" $p)
 
#extract only the hash portion of the file (hash).html 
 hash=$(echo $f | sed -r "s/([a-z0-9]+)(.)([a-z]+)/\1/g")

# get the uri associated with it from the csv file in format hash.processed,uri
# the capture group grabs the uri in its entirity 
 uri=$(grep $hash "ulrToHash.csv" | sed -r "s/[a-z0-9]+,(.+)/\1/g")

# do the tf, idf, tfidf calculation
# use scale 5 for percision and send the calulation to An arbitrary precision calculator language
 tf=$(echo "scale=5; $termCount / $wdCount" | bc)
 idf=8.8662
 tfidf=$(echo "scale=5; $tf * $idf" | bc)
 echo "tf=$tf idf=$idf tfidf=$tfidf uri=$uri"
# append the tf, idf, tfidf and uri to the final file 
 $(echo $tf,$idf,$tfidf,$uri >> $file)
done


