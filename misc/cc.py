#!/usr/bin/python
# coding: utf8

import sys,time,datetime,string;
import re;
import sqlite3
from sqlite3 import Error

reload(sys)
sys.setdefaultencoding('utf-8')
conn = ""

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn

def select_card_price_for_date(mtgset, number,date_today):
    global conn
    count_r=0
    cur = conn.cursor()
    cur.execute("SELECT * FROM cards_prices WHERE set_id=? and number=? and date=?", (mtgset,number,date_today))

    rows = cur.fetchall()
    for row in rows:
	count_r+=1
    return count_r

def insert_card_price_for_date(mtgset, number, date_today, price, quantity):
    global conn
    sql = ''' INSERT INTO cards_prices(set_id,number,date,price,quantity)
              VALUES(?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, (mtgset, number, date_today, price, quantity))
    conn.commit()
    return cur.lastrowid

def update_card_price_for_date(mtgset, number, date_today, price, quantity):
    global conn
    sql = ''' UPDATE cards_prices
              SET price = ?, quantity = ?
              WHERE set_id = ? and number = ? and date = ?'''
    cur = conn.cursor()
    cur.execute(sql, (price,quantity,mtgset,number,date_today))
    conn.commit()

def is_number_of_cards(line):
    parser = re.search('[1-9]',line[0:1]);
    if (parser):
	return True
    else:
	return False

def get_commands(filename):
    line_num = 1
    f=open(filename,'r')
    
    for line in f:
	action=""
	mtgset_number=""
	quantity=1
	lang=""
	promo=""
	line=line.strip()
	print(line)
	action=line[0]
	line=line[1:]
	str0=line.split(" ")
	if (len(str0)>1):
	    if is_number_of_cards(str0[0]):
		quantity=int(str0[0])
		mtgset_number=str0[1]
		lang=str0[2]
		if (len(str0)>3):
		    promo=str0[3]
	    else:
		mtgset_number=str0[0]
		lang=str0[1]
		if (len(str0)>2):
		    promo=str0[2]
	print(action+":"+str(quantity)+":"+mtgset_number+":"+lang+"-"+promo)
	line_num+=1


if __name__ == '__main__':
    count_args = 0
    if len(sys.argv)<2:
	print("usage: cc.py add.txt")
    else:
	conn = create_connection(r"mycards.db")
	for filename in sys.argv:
		if count_args:
		    print("Обработка файла: "+filename)
		    get_commands(filename)
		count_args+=1
