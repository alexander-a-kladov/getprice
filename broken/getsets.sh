#!/bin/bash
for a in `cat topdeck.txt | grep '(' | gawk -F '(' '{print $2}' | gawk -F ')' '{print $1}' | gawk -F '/' '{print $1}' | grep -v " " | sort -u`;
do
echo $a
./get_set_data.sh $a
done
