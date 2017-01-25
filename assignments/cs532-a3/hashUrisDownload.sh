#!/bin/bash


#find where we are
wd=$(pwd)

#this is where we store out hash -> uri pairs
file="$wd/ulrToHash.csv"


#check for some house cleaning
if [ -f $file ] 
then
   echo "File $file exists. Deleting and remaking"
   rm $file
fi


htmlDir="$wd/html"
if [ -d $htmlDir ]
then
   echo "Directory $htmlDir exists. Deleting and remaking"
   rm -rf $htmlDir
fi

processedDir="$wd/processed"
if [ -d $processedDir ]
then
   echo "Directory $processedDir exists. Deleting and remaking. We will use it later ;)"
   rm -rf $processedDir
fi

# make everyting
touch $file
mkdir "html"
mkdir "processed"
echo "Parsing thousand.dat"

#for each uri in the thousand
for uri in $(cat thousand.dat)
do
   # create the md5 hash of the url
   # use awk to remove the trailing - 
   hash=$(echo $(md5sum <<< $uri) | awk '{print $1}')
   hashtml=$hash".html"
   $(echo "$hash,$uri" >> $file)
   $(curl -A "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:44.0) Gecko/20100101 Firefox/44.01" $uri > "$htmlDir/$hashtml")
   echo $uri | awk -F/ '{print $3}'
   echo $hashtml
   echo $hash 
done

#clean up after ourselves
for f in $(find $htmlDir/*.html -size 0c)
do
   echo "cleaning $f because it failed to download"
   rm $f
done
