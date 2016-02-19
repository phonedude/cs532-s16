#!/bin/bash

for file in $(grep -lr "constitution" ./outFiles/*.processed | tail -10)
do
    cp "${file}" ./selection
done
