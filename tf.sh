#!/bin/bash

for file in ./selection/*.processed
do
    oc="$(grep -o 'constitution' "${file}" | wc -l)"
    count="$(wc -w "${file}" | awk '{print $1}')" 
    tf=$(echo "scale=4; $oc/$count" | bc) 
    echo "${tf}" >> tf.txt
    head -1 "${file}" >> tf.txt
done
