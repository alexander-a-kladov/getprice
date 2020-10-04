#!/usr/bin/python
# coding: utf8

import sys,datetime
import sqlite3
from sqlite3 import Error

print(sys.stdin.encoding)
conn = ""
mtgset = ""

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn

def select_card_name_for_lang(mtgset, number, lang):
    global conn
    count_r=0
    cur = conn.cursor()
    cur.execute("SELECT * FROM cards_names WHERE set_id=? and number=? and lang=?", (mtgset,number,lang))

    rows = cur.fetchall()
    if len(rows):
        return rows[0][3]
    return None

def insert_card_name_for_lang(mtgset, number, lang, name):
    global conn
    sql = ''' INSERT INTO cards_names(set_id,number,lang, name)
              VALUES(?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, (mtgset, number, lang, name))
    conn.commit()
    return cur.lastrowid

def update_card_name_for_lang(mtgset, number, lang, name):
    global conn
    sql = ''' UPDATE cards_names
              SET name = ?,
              WHERE set_id = ? and number = ? and lang = ?'''
    cur = conn.cursor()
    cur.execute(sql, (name,mtgset,number,date_today))
    conn.commit()

def load_names(filename):
    global mtgset
    f=open(filename,'r')
    line_num=1
    for line in f:
        name=line.split("\n")[0]
        print(mtgset+" "+str(line_num)+" "+name)
        insert_card_name_for_lang(mtgset,line_num,"ru",name)
        line_num+=1
    test_name=select_card_name_for_lang("znr",70,"ru")
    print("test_name="+str(test_name))
if __name__ == '__main__':
    count_args = 0
    total_cards = 0
    total_price = 0
    if len(sys.argv)<2:
        print("usage: load_cards_names.py set_file.txt")
        exit
    else:
        filename = sys.argv[1]
        mtgset=filename.split(".")[0]
        conn = create_connection(r"mycards.db")
        print(mtgset)
    load_names(filename)
    
