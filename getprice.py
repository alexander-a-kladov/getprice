#!/usr/bin/python3
# coding: utf8

# topdeck_tmpl.txt topdeck_pioner_tmpl.txt topdeck_modern.txt topdeck_cmdr_tmpl.txt topdeck_foil.txt topdeck_piles.txt
import sys, requests, json, time, datetime;
import re;
import sqlite3
from sqlite3 import Error
from price_dict import price_dict

# reload(sys)
# sys.setdefaultencoding('utf-8')
print(sys.stdin.encoding)
conn = ""
date_today = ""
fw = ""
fhtml = ""

total_cards = 0
total_price = 0
foil = 0
promo = 0
test_set = ""
lang = ""
test = False
html = False
inTopic = False
rarity_dict = dict()

result_fn = 'topdeck.txt'
result_html = 'topdeck.html'
scryfall_url = 'https://api.scryfall.com'


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


def select_card_price_for_date(mtgset, number, date_today):
    global conn
    count_r = 0
    cur = conn.cursor()
    cur.execute("SELECT * FROM cards_prices WHERE set_id=? and number=? and date=?", (mtgset, number, date_today))

    rows = cur.fetchall()
    for row in rows:
        count_r += 1
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
    cur.execute(sql, (price, quantity, mtgset, number, date_today))
    conn.commit()


def select_total_data(date_today):
    global conn
    count_r = 0
    cur = conn.cursor()
    cur.execute("SELECT * FROM total_data WHERE date=?", (date_today,))

    rows = cur.fetchall()
    for row in rows:
        count_r += 1
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
    cur.execute(sql, (price, quantity, date_today))
    conn.commit()


def add_price_for_card(mtgset, number, date_today, price, quantity):
    if select_card_price_for_date(mtgset, number, date_today):
        update_card_price_for_date(mtgset, number, date_today, price, quantity)
    else:
        insert_card_price_for_date(mtgset, number, date_today, price, quantity)


def add_total_data():
    global date_today, total_price, total_cards
    if select_total_data(date_today):
        update_total_data(date_today, total_price, total_cards)
    else:
        insert_total_data(date_today, total_price, total_cards)


def get_number_of_cards(line):
    parser = re.search('[0-9]x ', line);
    if (parser):
        return int(line[0:(parser.end() - 2)])
    else:
        return 1


def get_set_present(line):
    str0 = line.split('(')
    if (len(str0) > 1):
        str1 = str0[1].split(')')
        if (len(str1) > 1):
            parser = re.search('[A-Za-z0-9][A-Za-z0-9][A-Za-z0-9]', str1[0])
            if (parser):
                return str1[0]
    return None


def select_card_name_for_lang(mtgset, number, lang):
    global conn
    count_r = 0
    cur = conn.cursor()
    cur.execute("SELECT * FROM cards_names WHERE set_id=? and number=? and lang=?", (mtgset, number, lang))

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
    cur.execute(sql, (name, mtgset, number, date_today))
    conn.commit()


def get_price_from_txt(price_str):
    price = None
    pos = 0
    price_str_tokens = price_str.split()
    for token in price_str_tokens:
        try:
            price = float(token)
            break
        except ValueError:
            price = None
        pos += 1
    if price:
        del price_str_tokens[pos]
        price_str = " ".join(price_str_tokens)
        try:
            price = int(token)
        except ValueError:
            pass
    return price, price_str


def get_card_name(lang, mtgset, number):
    global scryfall_url
    if lang:
        name = select_card_name_for_lang(mtgset, number, lang)
        if name is None:
            url = scryfall_url + '/cards/' + mtgset + '/' + str(number) + '/' + lang
            r = requests.get(url)
            if r.status_code != 404:
                token = json.loads(r.text)
                token1 = token.get('card_faces')
                if token1:
                    token = token1[0]
                if (lang == 'en'):
                    insert_card_name_for_lang(mtgset, number, lang, token.get('name'))
                    return token.get('name')
                else:
                    insert_card_name_for_lang(mtgset, number, lang, token.get('printed_name'))
                    return token.get('printed_name')
            else:
                print('error rest api code=', r.status_code)
        else:
            return name
    return None


def set_foil_promo(line):
    global foil, promo, lang
    if line.find('<foil>') != -1:
        foil = 1
        line = line.replace('<foil>', '')
    if not line.find('/promo/') == -1:
        promo = 1
        line = line.replace('/promo/', '')
    if line.find('<nonfoil>') != -1:
        foil = 0
        line = line.replace('<nonfoil>', '')
    if line.find('/nonpromo/') != -1:
        promo = 0
        line = line.replace('/nonpromo/', '')
    if line.find('[ru]') != -1:
        lang = 'ru'
    elif line.find('[en]') != -1:
        lang = 'en'
    else:
        lang = ''
    return line


def get_price_modifier(mtg_set, lang):
    global price_dict
    price_modifier = 2.0
    if mtg_set in price_dict:
        if not isinstance(price_dict[mtg_set], dict):
            price_modifier = price_dict[mtg_set]
        else:
            price_modifier = price_dict[mtg_set][lang]
    # print("price_modifier"+str(price_modifier))
    return price_modifier


def write_html_headers():
    fhtml.write('<html>')
    style_f = open('html/style.html', 'r')
    fhtml.write(style_f.read())
    fhtml.write('<body>')
    contacts_f = open('html/contacts.html', 'r')
    fhtml.write(contacts_f.read())
    topdeck_search_f = open('html/topdeck_search.js', 'r')
    fhtml.write('<script>')
    fhtml.write(topdeck_search_f.read())
    fhtml.write('</script>\n')


def calc_price(token, mtgset, lang, promo, foil, line):
    price1 = price2 = 0
    price3 = 0
    if token.get('prices').get('usd'):
        price1 = int(50.0 * float(token.get('prices').get('usd'))) # 50
    if token.get('prices').get('eur'):
        price2 = 0#int(50.0 * float(token.get('prices').get('eur')))
    if token.get('prices').get('usd_foil'):
        price3 = int(30.0 * float(token.get('prices').get('usd_foil'))) # 30
        if get_set_present(line) == "FMB1":
            price3 = int(price3 / 5.0)
        if lang == 'ru':
            price3 = int(1.5 * price3)
        if promo:
            price3 = int(0.5 * price3)
    if price1 > price2:
        price = price1
    else:
        price = price2
    if price1 > 1.0 and price2 > 1.0:
        price = int((price1 + price2) / 2.0)
    if foil or promo:
        price = price3
        price = price + 4  # add perfect's price
                    # if price>=0 and price<4:
                    #    price = 4;
    price *= get_price_modifier(mtgset, "ru" if (~line.find("русский")) else lang)
    #price *= (-1.0 * (price * 150.0) ** 0.6 + 9000.0) / 8000.0
    price = int(price)
    return price


def add_to_rarity_dict(rarity_count, rarity, quantity, price):
    if rarity not in rarity_count:
        rarity_count[rarity] = [quantity, price]
    else:
        q = rarity_count[rarity][0]
        p = rarity_count[rarity][1]
        rarity_count[rarity] = [q+quantity, p+price]


def get_prices(filename):
    global total_cards, total_price, foil, promo, lang, test, test_set, fhtml, inTopic, rarity_dict
    album_names = {"Стандарт:": "Standard.png", "Пионер:": "Pioneer.png", "Модерн:": "Modern.png",
                  "Коммандер:": "Commander.jpg", "Фойл:": "Foil.jpg", "Пайло:": "Piles.jpg"}
    mana_symbols = {":w::w::w:": "w.html", ":u::u::u:": "u.html", ":b::b::b:": "b.html", ":r::r::r:": "r.html",
                   ":g::g::g:": "g.html", ":c:": "colorless.html", ":mc:": "multicolor.html"}
    album_spoilers_f = open('html/album_spoilers.html', 'r')
    album_spoilers = album_spoilers_f.read()
    album_spoilers_f.close()

    line_num = 1
    f = open(filename, 'r')
    print(filename)
    print(test_set)
    foil = promo = 0
    for line in f:
        if html and line.strip() in album_names:
            if inTopic:
                fhtml.write("</details></p>")
            fhtml.write(album_spoilers.replace('Topic_Name', '<img src=images/' + album_names[
                line.strip()] + ' alt=' + line.strip() + ' width=360px height=80px>'))
            inTopic = True
        reserve = False
        if line[0] == '-':
            reserve = True
            line = line[1:]
        line = set_foil_promo(line)
        str0 = line.split("{")
        if len(str0) > 1:
            str1 = str0[1].split("}")
            quantity = 0
            if len(str1) > 1:
                mtgset = str1[0].split("/")[0]
                number = str1[0].split("/")[1]
                if test and mtgset != test_set:
                    if test_set != "all" and test_set[0] != '>' and test_set[0] != '<':
                        continue
                # if mtgset=="znr":
                #    continue;
                url = "https://api.scryfall.com/cards/"
                url = url + str1[0]
                print(url)
                r = requests.get(url)
                if r.status_code != 404:
                    # print(r.text)
                    # raise Exception("Ошибка запроса с сервера")
                    token = json.loads(r.text)
                    if html:
                        image_uris = token.get('image_uris')
                        if image_uris:
                            image_url = image_uris.get('small')
                        else:
                            image_url = token.get('card_faces')[0].get('image_uris').get('small')
                    price, str1[1] = get_price_from_txt(str1[1])
                    frame_effect = token.get('frame_effects')
                    if frame_effect:
                        frame_effect = frame_effect[0].replace("extendedart", "Extended")
                        if not frame_effect == "Extended":
                            frame_effect = ""
                    else:
                        frame_effect = ""
                        
                    if not price or isinstance(price, float):
                        topdeck_multiplier = price
                        price = calc_price(token, mtgset, lang, promo, foil, line)
                        if isinstance(topdeck_multiplier, float):
                            price = int(price*topdeck_multiplier)
                    
                    if test and test_set[0] == '>':
                        if price < int(test_set.split('>')[1]):
                            #print("price="+str(price)+" too small")
                            continue
                    if test and test_set[0] == '<':
                        if price > int(test_set.split('<')[1]):
                            continue
                    if price > 0:
                        price = int(0.7*price)
                        if price < 10:
                            price = 10
                        quantity = get_number_of_cards(line)
                        if quantity > 4:
                            quantity = 4
                        total_cards += quantity
                        total_price += quantity * price
                        add_to_rarity_dict(rarity_dict, token.get("rarity"), quantity, quantity*price)
                        if not test:
                            add_price_for_card(mtgset, number, date_today, price, quantity)
                    if price == 0:
                        price = ""
                    time.sleep(0.3)  # scryfall recomendation
                else:
                    price = ""
                    print("error:" + str(r.status_code) + " " + str(line_num) + " " + line)
                    continue
                if reserve:
                    continue
                en_name = get_card_name('en', mtgset, number)
                if len(line.split('[ru]')) > 1:
                    card_name = get_card_name('ru', mtgset, number)
                elif len(line.split('[en]')) > 1:
                    card_name = get_card_name('en', mtgset, number)
                else:
                    card_name = None
                if card_name:
                    if quantity > 1:
                        str0[0] = str(quantity) + 'x '
                    else:
                        str0[0] = ''
                    str0[0] = str0[0] + card_name + ' - '
                if get_set_present(line):
                    fw.write(str0[0] + str1[1].strip() + ' ' + str(price))
                else:
                    fw.write(str0[0] + ' (' + mtgset.swapcase() + '/'+str(number)+ ')' + str1[
                        1].strip() + ' '+ str(price))
                if foil:
                    fw.write(' FOIL')
                if promo:
                    fw.write(' promo')
                if len(frame_effect):
                    fw.write(f' {frame_effect}')
                if html:
                    fhtml.write('<div id="container">')
                    # fhtml.write('<p>'+str(price)+' р </p>')
                    fhtml.write('<input style="width:100px" type="number" />')
                    fhtml.write(' <img src=')
                    fhtml.write(image_url)
                    fhtml.write(' alt=')
                    fhtml.write('"' + str0[0].replace(" - ", "") + '"')
                    fhtml.write(' height="230px"')
                    fhtml.write(' onclick=comparePrice("')
                    if card_name:
                        compare_card_name = card_name.replace(' ', '+')
                    else:
                        parser = re.search('[0-9]x ', line)
                        if parser:
                            compare_card_name = str0[0][parser.end():].split('(')[0].strip().strip('-').strip().replace(
                                ' ', '+')
                        else:
                            compare_card_name = str0[0].split('(')[0].strip().strip('-').strip().replace(' ', '+')
                    fhtml.write(compare_card_name)
                    fhtml.write('",')
                    fhtml.write('"' + en_name.replace(' ', '+') if en_name else '')
                    fhtml.write('")')
                    fhtml.write('>')
                    fhtml.write('<h2><span>')
                    if quantity > 1:
                        fhtml.write(str(quantity)+"x  "+str(price) + ' р')
                    else:
                        fhtml.write("    " + str(price) + ' р')
                    fhtml.write('</span></h2><p>')
                    if get_set_present(line):
                        fhtml.write(str0[0] + '<wbr>' + str1[1].strip() + '<wbr>')
                    else:
                        fhtml.write(
                            str0[0] + '<wbr>' + '(' + mtgset.swapcase() + '/' + str(number) + ')' + '<wbr>' + str1[
                                1].strip() + '<wbr>')
                    if foil:
                        fhtml.write(' FOIL')
                    if promo:
                        fhtml.write(' promo')
                    fhtml.write('</p>')
                    fhtml.write('</div>')
                    fhtml.write('\n')

                fw.write('\n\n')
        elif len(line) > 1:
            fw.write(line)
            if html:
                # fhtml.write('<div id="line">')
                if len(line.strip().split()) > 1 and line.strip().split()[1] in mana_symbols:
                    print(line.strip().split()[1])
                    file_mana_f = open("html/" + mana_symbols[line.strip().split()[1]])
                    line = line.replace(line.strip().split()[1], file_mana_f.read())
                    file_mana_f.close()
                fhtml.write('<p id="line">' + line + '</p>')
                # fhtml.write('</div>')
                fhtml.write('\n')
        line_num += 1
    print(rarity_dict)


if __name__ == '__main__':
    count_args = 0
    html = True
    prefix_fn = ""
    if len(sys.argv) < 2:
        print("usage: getprice.py file_tmpl.txt file_tmpl1.txt")
    else:
        print(sys.argv[1])
        if sys.argv[1] == "test":
            test_set = sys.argv[2]
            test = True
            prefix_fn = "test_"
            if test_set[0] != '>' and test_set[0] != '<':
                print("test_set=" + test_set)
            else:
                print("test_price=" + test_set)

        date_today = str(datetime.date.today())
        conn = create_connection(r"mycards.db")
        fw = open(prefix_fn+result_fn, 'w')
        fheader = open('header.txt', 'r')
        fw.write(fheader.read())
        if html:
            fhtml = open(prefix_fn+result_html, 'w')
            write_html_headers()
        for filename in sys.argv:
            if count_args and filename != prefix_fn+result_fn:
                if (test and count_args > 2) or test == False:
                    print("Обработка файла: " + filename)
                    get_prices(filename)
                    print("Карт обработано:" + str(total_cards) + " Стоимость: " + str(total_price) + " р")
                    time.sleep(5.0)
            count_args += 1
        print("Всего карт: " + str(total_cards))
        print("Стоимость: " + str(total_price) + " р")
        if (test == False):
            add_total_data()
            print("add_total")
        fw.close()
        if html:
            fhtml.close()
