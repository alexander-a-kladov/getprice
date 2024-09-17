#!/usr/bin/python3
# coding: utf8

import sys,datetime

if __name__ == '__main__':
    set_name = input("Введите сокращенное имя сета:")
    lang = input("Введите язык карт:")
    cards=dict()
    card_name=1
    print("Вводите номера карт, для завершения введите 0")
    while card_name:
        card_name_str=input()
        if len(card_name_str)==0:
            continue
        card_name=card_name_str.strip()
        if card_name != "0":
            if cards.get(card_name) is None:
                cards[card_name]=1
            else:
                cards[card_name]+=1
        else:
            break
    fw=open(set_name+lang+".txt","w")
    foil=False
    new_foil=False
    for key in cards.keys():
        num = key
        if key[-1] == 'f':
            num = key[:-1]
            new_foil=True
        else:
            new_foil=False
        if foil != new_foil:
            if new_foil:
                fw.write("<foil>\n")
            else:
                fw.write("<nonfoil>\n")
            foil = new_foil
        if cards[key]>1:
            print(str(cards[key])+"x ",end='')
            fw.write(str(cards[key])+"x ")
        print("["+lang+"] "+"{"+set_name+"/"+str(num)+"}")
        fw.write("["+lang+"] "+"{"+set_name+"/"+str(num)+"}"+"\n")
