#!/usr/bin/python3

import sys

def read_file(fn):
    tnumber = 0
    tprice  = 0
    line_num = 0
    f = open(fn,"r")
    if f:
        for line in f.readlines():
            line = line.strip()
            if len(line)==0:
                print(line)
                line_num+=1
                continue
            tokens = line.split()
            if tokens[0][-1]=='x':
                tokens[0]=tokens[0][:-1]
            try:
                quan = int(tokens[0])
            except:
                quan = 1
            price = 0
            for i in range(len(tokens)-1,0,-1):
                try:
                    price = int(tokens[i])
                except:
                    pass
                if price > 0:
                    break
            if quan>0 and price>0:
                tnumber += quan
                tprice += quan*price
                print(quan, price)
            else:
                #print("error line = ", line_num, " ",line, " ", quan, price)
                #break
                print(tokens[0])
            line_num+=1
        print("number: ", tnumber, "price: ", tprice)

if __name__ == "__main__":
    if len(sys.argv)>1:
        read_file(sys.argv[1])
    else:
        print("usage: ./calc_number_and_price.py cards.txt")

