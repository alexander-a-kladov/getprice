#!/usr/bin/python3
# coding: utf8

import sys,datetime

lang=''
set_name=''
common_cards_q=0
uncommon_cards_q=0
rare_cards_q=0
land_cards_q=0
foil_cards_q=0

def addToDict(d,card):
    if d.get(card) is None:
        d[card]=1
    else:
        d[card]+=1

def writeToFile(fw,header,d, quantity):
    global lang,set_name
    header+= str(quantity)+" карт, "+str(len(d.keys()))+" уникальных"
    print(header)
    fw.write(header+"\n")
    for key in sorted(d.keys()):
        if d[key]>1:
            print(str(d[key])+"x ",end='')
            fw.write(str(d[key])+"x ")
        print("["+lang+"] "+"{"+set_name+"/"+str(key)+"}")
        fw.write("["+lang+"] "+"{"+set_name+"/"+str(key)+"}"+"\n")

if __name__ == '__main__':
    set_name = input("Введите сокращенное имя сета:")
    lang = input("Введите язык карт:")
    cards=dict()
    common_cards=dict()
    uncommon_cards=dict()
    rare_cards=dict()
    land_cards=dict()
    foil_cards=dict()
    error_prz=False
    card_name=1
    count_cards=0
    count_boosters=0
    inputf=open(set_name+"/"+set_name+"_data.txt","r")
    for card_names in inputf.readlines():
        cards_list=card_names.strip().split(',')
        common_count=0
        try:
            ind = cards_list.index('f')
        except ValueError:
            ind = None
        if ind:
            common_count-=len(cards_list)-ind-1
            cards_list.pop(ind)
        for card_name in cards_list:
            if len(card_name)>0:
                card=int(card_name)
                count_cards+=1
                if count_cards<=common_count:
                    addToDict(common_cards,card)
                    common_cards_q+=1
                elif count_cards<=common_count+3:
                    addToDict(uncommon_cards,card)
                    uncommon_cards_q+=1
                elif count_cards<=common_count+3+1:
                    addToDict(rare_cards,card)
                    rare_cards_q+=1
                elif count_cards<=common_count+3+1+1:
                    addToDict(land_cards,card)
                    land_cards_q+=1
                elif count_cards<=len(cards_list):
                    addToDict(foil_cards,card)
                    foil_cards_q+=1
                if count_cards==len(cards_list):
                    if (count_cards!=common_count+3+1+1) and len(card_names.strip())>0:
                        print("booster error count =  "+str(count_cards)+" booster = "+str(count_boosters+1))
                        print(card_names)
                        error_prz=True
                    count_cards=0
                    count_boosters+=1
    if error_prz:
        sys.exit(1)
    fw=open(set_name+lang+".txt","w")
    fw.write("<foil>\n")
    writeToFile(fw,"Foils: ", foil_cards, foil_cards_q)
    fw.write("<nonfoil>\n")
    writeToFile(fw,"Lands: ", land_cards, land_cards_q)
    writeToFile(fw,"Rares & Mythics: ", rare_cards, rare_cards_q)
    writeToFile(fw,"Uncommons: ", uncommon_cards, uncommon_cards_q)
    writeToFile(fw,"Commons: ", common_cards, common_cards_q)
    fw.close()
    print("common_cards: "+str(common_cards_q))
    print("uncommon_cards: "+str(uncommon_cards_q))
    print("rare_cards: "+str(rare_cards_q))
    print("land_cards: "+str(land_cards_q))
    print("foil_cards: "+str(foil_cards_q))
    print("Count cards: "+str(count_boosters*15+count_cards))
