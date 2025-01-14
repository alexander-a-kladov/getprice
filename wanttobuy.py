#!/usr/bin/python3
# coding: utf8

import sys, requests, json, time, datetime
import re

foils = False
promo = False

def request_scryfall(name, set_name):
    url = "https://api.scryfall.com/cards/named?fuzzy="
    url += name.replace(' ', '+')
    print(url)
    if len(set_name)>0:
        url += "&set="+set_name
    r = requests.get(url)
    if r.status_code != 404:
        token = json.loads(r.text)
        return "["+token.get("lang")+"] {"+token.get("set")+"/"+token.get("collector_number")+"}", token.get("rarity")
    else:
        return None, None


def get_attributes(attrs):
    global foils, promo
    attrs = attrs.lower()
    if attrs.count("foil") > 0:
        new_foils = True
    else:
        new_foils = False
    if attrs.count("prerelease") > 0:
        new_promo = True
    else:
        new_promo = False
    if new_foils != foils:
        if new_foils:
            add_str = " <foil>"
        else:
            add_str = " <nonfoil>"
    else:
        add_str = ""
    if new_promo != promo:
        if new_promo:
            add_str += " /promo/"
        else:
            add_str += " /nonpromo/"
    else:
        add_str += ""
    foils = new_foils
    promo = new_promo
    return add_str


def add_to_rarity_dict(rarity_count, rarity, quantity, price):
    if rarity not in rarity_count:
        rarity_count[rarity] = [quantity, price]
    else:
        q, p = rarity_count[rarity]
        rarity_count[rarity] = [q+quantity, p+price]

def get_prices(filename):
    count_lines = 0
    count_cards = 0
    rarity_count = dict()
    rarity_foils = dict()
    count_en = 0
    mtg_sets = dict()
    f = open(filename, 'r')
    fw = open(filename+".codes", 'w')
    fw_foils = open(filename+".foils", 'w')
    for line in f:
        if len(line.strip())==0:
            continue
        tokens = line.strip().split('\t')
        if tokens[0][0] in {'0','1','2','3','4','5','6','7','8','9'}:
            tokens.insert(0, tokens[0].split(' ')[0])
            tokens[1] = tokens[1].split(tokens[0]+' ')[1]
        elif tokens[0][-1] in {'0','1','2','3','4','5','6','7','8','9'}:
            tokens[0] = tokens[1].split(' x')[-1]
            tokens[1] = tokens[1].split(' x'+tokens[0])[0]
        else:
            tokens.insert(0, '1')
        if len(tokens) == 2:
            tokens.append('')
        if len(tokens) == 3:
            tokens.append(',')
        print(tokens)
        if len(tokens) > 1:
            count_lines += 1
            count_cards += int(tokens[0])
            if len(tokens[3]) > 0:
                set_name = tokens[3].lower().split(',')[0]
                if set_name not in mtg_sets:
                    mtg_sets[set_name] = 0
                mtg_sets[set_name] += 1
                tokens[1]=tokens[1].strip()
                set_number, rarity = request_scryfall(tokens[1], set_name)
                add_str = get_attributes(tokens[2])
                if set_number:
                    quantity = int(tokens[0])
                    if len(add_str) > 0 and add_str.count('<nonfoil>') == 0:
                        add_to_rarity_dict(rarity_foils, rarity, quantity, 0)
                    else:
                        add_to_rarity_dict(rarity_count, rarity, quantity, 0)
                    if quantity > 1:
                        card_descr = tokens[0]+'x '+set_number
                    else:
                        card_descr = set_number
                    print(card_descr)
                    if len(add_str) > 0 and add_str.count('<nonfoil>') == 0:
                        fw_foils.write(card_descr+add_str+"\n")
                    else:
                        fw.write(card_descr+"\n")
        time.sleep(0.3)
    print(len(mtg_sets))
    print(mtg_sets)
    print(count_lines, count_cards)
    print(rarity_count)
    print(rarity_foils)
    f.close()
    fw.close()
    fw_foils.close()


if __name__ == '__main__':
    count_args = 0
    html = True
    if len(sys.argv) < 2:
        print("usage: wanttobuy.py file_tmpl.txt")
    else:
        print(sys.argv[1])
        get_prices(sys.argv[1])
