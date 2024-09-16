#!/usr/bin/python3
# coding: utf8

import sys,datetime

if __name__ == '__main__':
    set_name = input("Введите сокращенное имя сета:")
    lang = input("Введите язык карт:")
    cards=list()
    count_cards=0
    count_boosters=1
    card_name=1
    print("Вводите номера карт, для завершения введите 0")
    inputf=open("draft_data.txt","r")
    for card_name in inputf.readlines():
        if len(card_name.strip())>0:
            cards.append(int(card_name.strip()))
    fw=open("draft_"+set_name+".txt","w")
    for card in cards:
        if count_cards==0:
            print("\nBooster "+str(count_boosters))
            fw.write("\nBooster "+str(count_boosters)+"\n")
        count_cards+=1
        if count_cards==15:
            count_boosters+=1
            count_cards=0
        print("["+lang+"] "+"{"+set_name+"/"+str(card)+"}")
        fw.write("["+lang+"] "+"{"+set_name+"/"+str(card)+"}"+"\n")
    fw.close()
