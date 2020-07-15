#!/usr/bin/python
# coding: utf8

import sys,requests,json,time,datetime;
import re;
import sqlite3
from sqlite3 import Error

reload(sys)
sys.setdefaultencoding('utf-8')
conn = ""
date_today = ""
fw = ""

total_cards = 0
total_price = 0
foil = 0
promo = 0
lang = ""

result_fn = 'topdeck.txt'
scryfall_url = 'https://api.scryfall.com'

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

def select_total_data(date_today):
    global conn
    count_r=0
    cur = conn.cursor()
    cur.execute("SELECT * FROM total_data WHERE date=?", (date_today,))

    rows = cur.fetchall()
    for row in rows:
	count_r+=1
    return count_r

def insert_total_data(date_today, price, quantity):
    global conn
    sql = ''' INSERT INTO total_data(date,price,quantity)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, (date_today, price, quantity))
    conn.commit()
    return cur.lastrowid

def update_total_data(date_today, price, quantity):
    global conn
    sql = ''' UPDATE total_data
              SET price = ?, quantity = ?
              WHERE date = ?'''
    cur = conn.cursor()
    cur.execute(sql, (price,quantity,date_today))
    conn.commit()


def add_price_for_card(mtgset, number, date_today, price, quantity):
    if select_card_price_for_date(mtgset, number, date_today):
	update_card_price_for_date(mtgset, number, date_today, price, quantity)
    else:
	insert_card_price_for_date(mtgset, number, date_today, price, quantity)

def add_total_data():
    global date_today,total_price,total_cards
    if select_total_data(date_today):
	update_total_data(date_today,total_price,total_cards)
    else:
	insert_total_data(date_today,total_price,total_cards)

def get_number_of_cards(line):
    parser = re.search('[1-9]x',line);
    if (parser):
	return int(line[0:(parser.end()-1)])
    else:
	return 1

def get_set_present(line):
    str0 = line.split('(');
    if (len(str0)>1):
	str1 = str0[1].split(')');
	if (len(str1)>1):
	    parser = re.search('[A-Z][A-Za-z0-9][A-Za-z0-9]',str1[0])
	    if (parser):
		return str1[0]
    return None

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

def get_card_name(line, mtgset, number):
    global scryfall_url
    lang=None
    if (len(line.split('[ru]'))>1):
	lang='ru'
    elif (len(line.split('[en]'))>1):
	lang='en'
    if lang:
	name = select_card_name_for_lang(mtgset, number, lang)
	if name is None:
	    url=scryfall_url+'/cards/'+mtgset+'/'+str(number)+'/'+lang
	    r = requests.get(url)
	    if r.status_code != 404:
		token = json.loads(r.text)
		token1= token.get('card_faces')
		if token1:
		    token = token1[0]
		if (lang=='en'):
		    insert_card_name_for_lang(mtgset, number, lang, token.get('name'))
		    return token.get('name')
		else:
		    insert_card_name_for_lang(mtgset, number, lang, token.get('printed_name'))
		    return token.get('printed_name')
	    else:
		print('error rest api code=',r.status_code)
	else:
	    return name
    return None

def set_foil_promo(line):
    global foil,promo,lang
    if line.find('<foil>')!=-1:
	foil=1
	line = line.replace('<foil>','')
    if line.find('/promo/')!=-1:
	promo=1
	line = line.replace('/promo/','')
    if line.find('<nonfoil>')!=-1:
	foil=0
	line = line.replace('<nonfoil>','')
    if line.find('/nonpromo/')!=-1:
	promo=0
	line = line.replace('/nonpromo/','')
    if line.find('[ru]')!=-1:
	lang='ru'
    elif line.find('[en]')!=-1:
	lang='en'
    else:
	lang=''
    return line

def get_prices(filename):
    global total_cards, total_price, foil, promo, lang
    line_num = 1
    f=open(filename,'r')
    foil=promo=0
    for line in f:
	reserv = False
	if line[0]=='-':
	    reserv = True
	    line=line[1:]
	line = set_foil_promo(line)
	str0=line.split("{")
	if (len(str0)>1):
	    str1=str0[1].split("}")
	    if (len(str1)>1):
		url="https://api.scryfall.com/cards/"
		url=url+str1[0];
		print(url)
		r = requests.get(url);
		if r.status_code != 404:
		    #print(r.text)
		    #raise Exception("Ошибка запроса с сервера")
		    token = json.loads(r.text)
		    price1 = price2 = 0
		    price3 = 0
		    if token.get('prices').get('usd'):
			price1 = int(50.0*float(token.get('prices').get('usd')))
		    if token.get('prices').get('eur'):
			price2 = int(60.0*float(token.get('prices').get('eur')))
		    if token.get('prices').get('usd_foil'):
			price3 = int(50.0*float(token.get('prices').get('usd_foil')))
			if (get_set_present(line)=="FMB1"):
			    price3 = int(price3/5.0)
			if lang=='ru':
			    price3 = int(3.0*price3)
			if promo:
			    price3 = int(0.5*price3)
		    if (price1>price2):
			price = price1
		    else:
			price = price2
		    if foil or promo:
			price=price3
		    if price>0 and price<4:
			price = 4;
		    if price>0:
			quantity = get_number_of_cards(line)
			total_cards += quantity
			total_price += quantity*price
			mtgset = str1[0].split("/")[0]
			number = int(str1[0].split("/")[1])
			if foil==0 and promo==0:
			    add_price_for_card(mtgset,number,date_today,price,quantity)
		    if (price==0):
			price=""
		    time.sleep(0.3) # scryfall recomendation
		else:
		    price="";
		    print("error:"+str(r.status_code)+" "+str(line_num)+" "+line)
		if reserv:
		    continue
		card_name=get_card_name(line,mtgset,number)
		if card_name:
		    if quantity>1:
			str0[0]=str(quantity)+'x '
		    else:
			str0[0]=''
		    str0[0]=str0[0]+card_name+' - '
		if get_set_present(line):
		    fw.write(str0[0]+str(price)+' р '+str1[1].strip())
		else:
		    fw.write(str0[0]+str(price)+' р'+' ('+ mtgset.swapcase()+')'+str1[1].strip())
		if foil:
		    fw.write(' FOIL')
		if promo:
		    fw.write(' promo')
		fw.write('\n\n')
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
	fw=open(result_fn,'w')
	for filename in sys.argv:
		if count_args and filename != result_fn:
		    print("Обработка файла: "+filename)
		    get_prices(filename)
		    print("Карт обработано:"+str(total_cards)+" Стоимость: " + str(total_price) + " р")
		    time.sleep(5.0)
		count_args+=1
	print("Всего карт: "+str(total_cards))
	print("Стоимость: "+str(total_price)+" р")
	add_total_data()
	fw.close()
