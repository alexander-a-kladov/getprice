#!/usr/bin/python
# coding: utf8

import sys,requests,json,time;
f=open('topdeck_tmpl.txt','r')
for line in f:
    str0=line.split("{")
    if (len(str0)>1):
	str1=str0[1].split("}")
	if (len(str1)>1):
	    url="https://api.scryfall.com/cards/"
	    url=url+str1[0];
	    #print(url)
	    r = requests.get(url);
	    if r.status_code != 404:
		#print(r.text)
		#raise Exception("Ошибка запроса с сервера")
		token = json.loads(r.text)
		price1 = price2 = 0
		if token.get('prices').get('usd'):
		    price1 = int(50.0*float(token.get('prices').get('usd')))
		if token.get('prices').get('eur'):
		    price2 = int(60.0*float(token.get('prices').get('eur')))
		if (price1>price2):
		    price = price1
		else:
		    price = price2
		if price>0 and price<4:
		    price = 4;
		if (price==0):
		    price=""
		time.sleep(0.1) # scryfall recomendation
	    else:
		price="";
	    print(str0[0]+str(price)+' р'+str1[1])
    elif (len(line)>1):
	print(line)
