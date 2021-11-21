#!/bin/bash
IFS=$'\n'
TCOST=0
NUM=0

if [ "$1"x == "x" ]; then
echo "usage: $0 SET"
exit 1
fi
price=""
function getPrice()
{
    price=`echo $1 | gawk -F" - " '{print $2}' | gawk -F" р " '{print $1}'`
}

for a in `cat topdeck.txt`; do
line=`echo $a | grep $1`
if [ $? -eq 0 ];then
echo $line
getPrice $line
number=`echo $line | cut -d" " -f 1`
echo $number | grep x > /dev/null
if [ $? -eq 0 ]; then
number=`echo $number | sed -e 's/x//'`
else
number="1"
fi
NUM=$(( NUM + number ))
TCOST=$(( TCOST + price * number ))
fi
done;
echo "Number of cards:"$NUM
echo "Total cost:"$TCOST
