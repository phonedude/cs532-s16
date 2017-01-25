#!/bin/bash

for file in ./selection/*.processed
do
    head -1 "${file}" >>./URI.txt
done
