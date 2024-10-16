#!/usr/bin/python3
# coding: utf8

# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import sys, re
foil = promo = lang = ''

def set_foil_promo(line):
    global foil, promo, lang
    if line.find('<foil>') != -1:
        foil = 'FOIL'
        line = line.replace('<foil>', '')
    if not line.find('/promo/') == -1:
        promo = 'promo'
        line = line.replace('/promo/', '')
    if line.find('<nonfoil>') != -1:
        foil = ''
        line = line.replace('<nonfoil>', '')
    if line.find('/nonpromo/') != -1:
        promo = ''
        line = line.replace('/nonpromo/', '')
    if line.find('[ru]') != -1:
        lang = 'ru'
    elif line.find('[en]') != -1:
        lang = 'en'
    else:
        lang = ''
    return line


def get_number_of_cards(line):
    parser = re.search('[0-9]x ', line)
    if (parser):
        return line[0:parser.end()], line[parser.end():]
    else:
        return '1', line


def get_mtgset_number(line):
    mtgset_number = None
    str0 = line.split("{")
    if len(str0) > 1:
        str1 = str0[1].split("}")
        if len(str1) > 1:
            mtgset_number = str1[0].split("/")
    return mtgset_number


def get_number_of_cards_search(line):
    parser = re.search('[0-9]x ', line)
    if (parser):
        return int(line[0:(parser.end() - 2)]), line[parser.end():]
    else:
        return 1, line


def get_mtgset_number_search(line):
    mtgset_number = None
    str0 = line.split("(")
    if len(str0) > 1:
        str1 = str0[1].split(")")
        if len(str1) > 1:
            mtgset_number = str1[0].split("/")
    return mtgset_number


def read_albums(album_names : list) -> dict:
    global foil, promo
    albums = dict()
    for name in album_names:
        album_name = name
        albums[album_name] = list()
        foil= ''
        promo=''
        f = open(name,'r')
        if f:
            for line in f:
                if len(line) > 2 and line[0] != '-':
                    line = line.strip()
                    line = set_foil_promo(line)
                    mtgset_number = get_mtgset_number(line)
                    if mtgset_number:
                        quantity, line = get_number_of_cards_search(line)
                        albums[album_name].append((quantity, mtgset_number, line, foil, promo))
                    else:
                        albums[album_name].append(line)
                else:
                    albums[album_name].append(line[0:len(line)-1])
            f.close()
    return albums


def print_albums(albums : dict):
    for album in albums.values():
        for line in album:
            print(line)


def update_albums(albums: dict, mtgset_number: list, quantity: int, foil: str, promo: str) -> int:
    number_of_cards = 0
    for album in albums.values():
        for i in range(len(album)):
            el = album[i]
            if type(el) is not str:
                quan, mtgset_n, line, fo, pr  = el
                if quan > 0 and mtgset_n[0].lower() == mtgset_number[0].lower() and mtgset_n[1] == mtgset_number[1]:
                    if foil == fo and promo == pr:
                        if quan>=quantity:
                            album[i] = (quan-quantity, mtgset_n, line, foil, promo)
                            #print(album[i])
                            number_of_cards += quantity
                            return number_of_cards
                        else:
                            album[i] = (0, mtgset_n, line, foil, promo)
                            #print(album[i])
                            quantity -= quan
                            number_of_cards += quan
    return number_of_cards

def make_foil_promo_str(foil_c, promo_c, foil, promo):
    foil_promo_str = ''
    if foil != foil_c:
        if foil == 'FOIL':
            foil_promo_str += " <foil>"
        else:
            foil_promo_str += " <nonfoil>"
        foil_c = foil
    if promo != promo_c:
        if promo == 'promo':
            foil_promo_str += " /promo/"
        else:
            foil_promo_str += " /nonpromo/"
        promo_c = promo
    return foil_promo_str, foil_c, promo_c


def save_albums(albums: dict):
    foil_c = ''
    promo_c = ''
    for album_name in albums:
        f = open(album_name, 'w')
        if f:
            album = albums[album_name]
            for el in album:
                if type(el) is str:
                    f.write(el+'\n')
                else:
                    quantity, mtgset_number, line, foil, promo = el
                    qunt_str = ''
                    if quantity<=0:
                        continue
                    if quantity > 1:
                        qunt_str = str(quantity)+'x '
                    foil_promo_str, foil_c, promo_c = make_foil_promo_str(foil_c, promo_c, foil, promo)
                    f.write(qunt_str + strip(line) + foil_promo_str + "\n")
            f.close()


def read_search_file(search_file: str)->list:
    search_data = list()
    print(search_file)
    f = open(search_file, 'r')
    if f:
        for line in f:
            line = line.strip()
            if len(line):
                mtgset_number = get_mtgset_number_search(line)
                if mtgset_number and len(mtgset_number) > 1:
                    quantity, line = get_number_of_cards_search(line)
                    search_data.append((quantity, mtgset_number, line))
        f.close()
    return search_data


def print_search_data(search_data: list):
    for el in search_data:
        print(el)


def read_request_file(request_file: str):
    number_of_cards = 0
    request_data = list()
    f = open(request_file, 'r')
    if f:
        for line in f:
            line = line.strip()
            if len(line):
                args = line.split('  ')
                tail = ''
                if len(args)>1:
                    quantity = args[-1].strip()
                else:
                    quantity = '1'
                args1 = line.split(' - ')
                if len(args1)>1:
                    name = args1[0].strip()
                    try:
                        tokens = name.split(' ')
                        int(tokens[0])
                        quantity = tokens[0]
                        name = " ".join(tokens[1:])
                    except:
                        pass
                    tail = args1[1].strip()
                else:
                    name = args[0]
                try:
                	number_of_cards += int(quantity)
                except:
                	number_of_cards += 1
                	quantity = "1"
                request_data.append((int(quantity), name, tail))
        f.close()
    return request_data, number_of_cards


def print_request_data(request_data: list):
    for el in request_data:
        print(el)


def process_request_data(albums: dict, search_data: list, request_data: list):
    number_of_cards = 0
    not_found = list()
    for el in request_data:
        found = number_of_cards
        quantity, name, tail = el
        print(el)
        if len(tail.split('FOIL'))>1:
            foil = 'FOIL'
        else:
            foil = ''
        if len(tail.split('promo'))>1:
            promo = 'promo'
        else:
            promo = ''
        for s in search_data:
            quan, mtgset_number, line = s
            if len(line.lower().split(name.lower()))>1:
                if foil == 'FOIL' and len(line.split(foil))>1 or foil == '' and len(line.split('FOIL'))<=1:
                    if promo == 'promo' and len(line.split(promo))>1 or promo == '' and len(line.split('promo'))<=1:
                        if quan >= quantity:
                            number_of_cards += update_albums(albums, mtgset_number, quantity, foil, promo)
                            break
                        else:
                            number_of_cards += update_albums(albums, mtgset_number, quan, foil, promo)
                            quantity-=quan
        if found == number_of_cards:
            not_found.append(el)
    return number_of_cards, not_found


def print_not_found(not_found):
    print('Не найдены')
    for el in not_found:
        print(el)


# findandremove.py topdeck_*.txt topdeck.txt

if __name__ == '__main__':
    album_names = ['topdeck_tmpl.txt', 'topdeck_pioner_tmpl.txt', 'topdeck_modern.txt', 'topdeck_cmdr_tmpl.txt', 'topdeck_foil.txt', 'topdeck_piles.txt']
    search_file = "topdeck.txt"
    request_file = ""
    if len(sys.argv) > 1:
        request_file = sys.argv[1]
    else:
        print("usage: ./findandremove.py request_file")
        exit(1)
    albums = read_albums(album_names)
   # print_albums(albums)
    search_data = read_search_file(search_file)
   # print_search_data(search_data)
    request_data, nc_req = read_request_file(request_file)
    nc, not_found = process_request_data(albums, search_data, request_data)
    print('Найдено '+str(nc)+' карт из '+str(nc_req))
    print_not_found(not_found)
    ans = input("Save albums (y,n)?");
    #print_albums(albums)
    if ans == "y":
        save_albums(albums)
        print("albums saved")
    else:
        print("not saved")
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
