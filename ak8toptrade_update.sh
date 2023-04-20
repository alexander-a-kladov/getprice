#!/bin/bash

md1=`md5sum topdeck.html | awk '{print $1 }'`
md2=`md5sum ak8toptrade/index.html | awk '{print $1}'`
if [ $md1 != $md2 ]; then
cp -f topdeck.html ak8toptrade/index.html
cd ak8toptrade
git add -u .
git commit -m "Update "`date +%d%m%y`
git push
fi