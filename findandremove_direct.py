#!/usr/bin/python3
# coding: utf8

import sys

inputfile = "topdeck.txt"
resultfile = "topdeck_result.txt"

order_dict = dict()

def get_data(l):
    tokens = l.split(")")
    if len(tokens)>1:
        quan_token = tokens[0].split(" ")
        try:
            if quan_token[0][-1] == 'x':
                quantity = int(quan_token[0][:-1])
            else:
                quantity = int(quan_token[0])
            tokens[0]=tokens[0][len(quan_token[0]):]
        except:
            quantity = 1
        price = 0
        for p_str in tokens[1].split():
            try:
                price = int(p_str)
            except:
                pass
            if price>0:
                break
        key = '('+tokens[0].split('(')[1]+')'
        foil_token = tokens[1].split("FOIL")
        if len(foil_token)>1:
            key += " FOIL"
        return key, quantity, price
    return None, None, None


def read_orderfile(fname):
    global order_dict
    f = open(fname, "r")
    if f:
        for l in f.readlines():
            key, quantity = get_data(l)
            if key and quantity:
                if key not in order_dict:
                    order_dict[key] = quantity
                else:
                    order_dict[key] += quantity
        f.close()


def update_topdeck():
    global order_dict
    fi = open(inputfile, "r")
    fs = open(resultfile, "w")
    total_cards = 0
    total_price = 0
    lines = 0
    cards = 0
    lastl = None
    if fi and fs:
        for l in fi.readlines():
            if l[0] == '-':
                continue
            key, quantity, price = get_data(l)
            if key and quantity:
                
                if key in order_dict:
                    quan0 = quantity
                    lines += 1
                    o_quan = order_dict[key]
                    if quantity - o_quan>=0:
                        del order_dict[key]
                        quantity -= o_quan
                    else:
                        order_dict[key]-=quantity
                        quantity = 0
                    cards += quan0 - quantity
                    if quantity:
                        if l[0] in ['0','1','2','3','4','5','6','7','8','9']:
                            l = str(quantity)+l[len(str(quan0)):]
                    else:
                         l=""
                total_cards += quantity
                total_price += quantity*price
            if len(l.strip())==0 and lastl==l.strip():
                l = ""
            lastl = l
            if l:
                fs.write(l)
        print(f'found lines={lines} cards={cards}')
        print(f'cards left {total_cards} price {total_price}')
        print("not found:")
        print(order_dict)
        fi.close()
        fs.close()
                        
                        
if __name__ == "__main__":
    if len(sys.argv)==2:
        read_orderfile(sys.argv[1])
        update_topdeck()
    else:
        print("usage: ./findandremove_direct.py order_file.txt")

