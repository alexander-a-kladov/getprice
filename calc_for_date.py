#!/usr/bin/python
# coding: utf8

import sys,datetime
import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn

def select_cards_total_for_date(date_today):
    global conn
    count_r=0
    cur = conn.cursor()
    cur.execute("SELECT * FROM cards_prices WHERE date=?", (date_today,))

    rows = cur.fetchall()
    return rows

if __name__ == '__main__':
    count_args = 0
    total_cards = 0
    total_price = 0
    if len(sys.argv)<2:
	date_calc = str(datetime.date.today())
    else:
	date_calc = sys.argv[1]
    print('На дату: '+date_calc)
    conn = create_connection(r"mycards.db")
    rows = select_cards_total_for_date(date_calc)
    for row in rows:
	if (row[3] and row[4]):
	    total_cards += row[4]
	    total_price += row[4]*row[3]
    print("Всего карт: "+str(total_cards))
    print("Стоимость: "+str(total_price))
