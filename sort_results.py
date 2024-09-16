#!/usr/bin/python3
import sys

TOKEN_KEY='<div id="container">'
PRICE_KEY='<span>'
PRICE_KEY2='р</span>'

def sort_html_file(filename):
    price_dict=dict()
    f = open(filename, "r")
    fc = open(filename.split(".html")[0]+"_sorted.html", "w")
    print(filename.split(".html")[0]+"_sorted.html")
    if f and fc:
        for line in f.readlines():
            if line.find(TOKEN_KEY) == -1:
                fc.write(line)
                continue;
            line1 = line.split(PRICE_KEY)[1].split(PRICE_KEY2)[0].strip()
            if len(line1.split('x '))>1:
                line1 = line1.split('x ')[1]
            try:
                price = int(line1)
            except:
                price = 0
            if price not in price_dict:
                price_dict[price] = [line]
            else:
                price_dict[price].append(line)
        f.close()
    

    if fc:
        for key in sorted(price_dict.keys(), reverse=True):
            for line in price_dict[key]:
                fc.write(line)
        fc.close()


if __name__ == "__main__":
    sort_html_file(sys.argv[1])

