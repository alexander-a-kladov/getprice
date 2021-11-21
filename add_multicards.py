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
        card_name=int(input())
        if card_name>0:
            if cards.get(card_name) is None:
                cards[card_name]=1
            else:
                cards[card_name]+=1
    fw=open(set_name+lang+".txt","w")
    for key in cards.keys():
        if cards[key]>1:
            print(str(cards[key])+"x ",end='')
            fw.write(str(cards[key])+"x ")
        print("["+lang+"] "+"{"+set_name+"/"+str(key)+"}")
        fw.write("["+lang+"] "+"{"+set_name+"/"+str(key)+"}"+"\n")
