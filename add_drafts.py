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
    while card_name:
        card_name_str=input()
        if len(card_name_str)==0:
            continue
        card_name=int(card_name_str)
        if card_name==0:
            break
        cards.append(card_name)
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
