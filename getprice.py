#!/usr/bin/python
# coding: utf8

import sys,requests,json,time,datetime;
import sqlite3
from sqlite3 import Error

conn = ""
date_today = ""
fw = ""

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn

def select_card_price_for_date(mtgset, number,date_today):
    count_r=0
    cur = conn.cursor()
    cur.execute("SELECT * FROM cards_prices WHERE set_id=? and number=? and date=?", (mtgset,number,date_today))

    rows = cur.fetchall()
    for row in rows:
	count_r+=1
    return count_r

def insert_card_price_for_date(mtgset, number, date_today, price):
    sql = ''' INSERT INTO cards_prices(set_id,number,date,price)
              VALUES(?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, (mtgset, number, date_today, price))
    conn.commit()
    return cur.lastrowid

def update_card_price_for_date(mtgset, number, date_today, price):
    sql = ''' UPDATE cards_prices
              SET price = ?
              WHERE set_id = ? and number = ? and date = ?'''
    cur = conn.cursor()
    cur.execute(sql, (price,mtgset,number,date_today))
    conn.commit()

def add_price_for_card(mtgset, number, date_today, price):
    if select_card_price_for_date(mtgset, number, date_today):
	update_card_price_for_date(mtgset, number, date_today, price)
    else:
	insert_card_price_for_date(mtgset, number, date_today, price)


def get_prices(filename):
    line_num = 1;
    f=open(filename,'r')
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
		    if price>0:
			add_price_for_card(str1[0].split("/")[0],int(str1[0].split("/")[1]),date_today,price)
		    if (price==0):
			price=""
		    time.sleep(0.1) # scryfall recomendation
		else:
		    price="";
		    print("error:"+str(r.status_code)+" "+str(line_num)+" "+line)
		fw.write(str0[0]+str(price)+' р'+str1[1]+"\n")
	elif (len(line)>1):
	    fw.write(line)
	line_num+=1

if __name__ == '__main__':
    count_args = 0
    if len(sys.argv)<2:
	print("usage: getprice.py file_tmpl.txt file_tmpl1.txt")
    else:
	date_today = str(datetime.date.today())
	conn = create_connection(r"mycards.db")
	fw=open('topdeck.txt','w')
	for filename in sys.argv:
		if count_args:
		    get_prices(filename)
		count_args+=1
	fw.close()
