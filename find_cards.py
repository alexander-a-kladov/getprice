#!/usr/bin/python
# coding: utf8

import sys,datetime
import sqlite3
from sqlite3 import Error

total_cards = 0
total_price = 0

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn

def select_card_by_name(name,quantity):
    global conn
    count_r=0
    cur = conn.cursor()
    cur.execute("""select cp.quantity,cn.name,cp.price,max(date) from cards_names as cn join cards_prices as cp on cp.set_id=cn.set_id
		    and cp.number=cn.number where cn.name=? and cp.quantity>=? and date>=(select max(date) from total_data)""",(name,quantity,))
    rows = cur.fetchall()
    return rows

def read_mtg_file(filename):
    global total_cards,total_price
    f=open(filename,'r')
    for line in f:
	if len(line)>3:
	    quantity=line.split(' ',1)[0]
	    name=line.split(' ',1)[1][0:-2]
	    rows=select_card_by_name(name,1)
            quantity_my=rows[0][0]
	    if quantity_my>int(quantity):
		quantity_my=int(quantity)
	    if quantity_my:
		print(str(quantity_my)+"/"+quantity+" "+str(rows[0][1])+" "+str(rows[0][2]))
		total_cards+=quantity_my
		total_price+=quantity_my*rows[0][2]
	    else:
		print("-"+str(quantity)+" "+name)

if __name__ == '__main__':
    
    if len(sys.argv)<2:
	print("usage: find_cards.py <file_name_deck_mtggoldfish>")
	sys.exit(1)
    else:
	file_name = sys.argv[1]
    conn = create_connection(r"mycards.db")
    read_mtg_file(file_name)
    print("Всего карт: "+str(total_cards))
    print("Стоимость: "+str(total_price))
