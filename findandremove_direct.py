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
        key = tokens[0].strip()+')'
        foil_token = tokens[1].split("FOIL")
        if len(foil_token)>1:
            key += " FOIL"
        return key, quantity
    return None, None

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
    lastl = None
    if fi and fs:
        for l in fi.readlines():
            if l[0] == '-':
                continue
            key, quantity = get_data(l)
            if key and quantity:
                if key in order_dict:
                    quan0_len = len(str(quantity))
                    o_quan = order_dict[key]
                    if quantity - o_quan>=0:
                        del order_dict[key]
                        quantity -= o_quan
                    else:
                        order_dict[key]-=quantity
                        quantity = 0
                    if quantity:
                        if l[0] in ['0','1','2','3','4','5','6','7','8','9']:
                            l = str(quantity)+l[quan0_len:]
                    else:
                         l=""
            if len(l.strip())==0 and lastl==l.strip():
                l = ""
            lastl = l
            if l:
                fs.write(l)
        fi.close()
        fs.close()
                        
                        
if __name__ == "__main__":
    if len(sys.argv)==2:
        read_orderfile(sys.argv[1])
        update_topdeck()
    else:
        print("usage: ./findandremove_direct.py order_file.txt")

