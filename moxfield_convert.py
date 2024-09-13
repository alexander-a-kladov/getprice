#!/usr/bin/python3
import sys

def convert_moxfield_file(filename):
    f = open(filename, "r")
    fc = open(filename.split(".txt")[0]+"_list.txt", "w")
    ff = open(filename.split(".txt")[0]+"_foils.txt", "w")
    ff.write("<foil>\n")
    if f:
        for line in f.readlines():
            line = line.strip()
            quan = line.split(' ')[0]
            set_name = line.split('(')[1].split(')')[0].lower()
            if len(set_name)==4 and set_name!="plst":
                set_name = set_name[1:]
            if set_name=="plst":
                set_name = set_name.upper()
            number = line.split(') ')[1].split(' ')[0].split('p')[0]
            try:
                int(number[-1])
            except:
                number = number[:-1]
            number = number.lower()
            if line.find("*F*")!=-1:
                ff.write(quan+"x [en] {"+set_name+"/"+number+"}\n")
            else:
                fc.write(quan+"x [en] {"+set_name+"/"+number+"}\n")
        ff.close()
        fc.close()
    f.close()


def convert_scryfall_file(filename):
    f = open(filename, "r")
    fc = open(filename.split(".txt")[0]+"_list.txt", "w")
    ff = open(filename.split(".txt")[0]+"_foils.txt", "w")
    ff.write("<foil>\n")
    if f:
        f.readline()
        for line in f.readlines():
            line = line.strip()
            if line[0]=='"':
                index = line[1:].find('"')
                if index!=-1:
                    line = line[index:]
            tokens = line.split(',')
            quan = tokens[3]
            set_name = tokens[1].lower()
            if len(set_name)==4 and set_name!="plst":
                set_name = set_name[1:]
            if set_name=="plst":
                set_name = set_name.upper()
            number = tokens[6]
            try:
                int(number[-1])
            except:
                number = number[:-1]
            number = number.lower()
            if tokens[4]=='foil':
                ff.write(quan+"x [en] {"+set_name+"/"+number+"}\n")
            else:
                fc.write(quan+"x [en] {"+set_name+"/"+number+"}\n")
        ff.close()
        fc.close()
    f.close()




if __name__ == "__main__":
    if len(sys.argv)==2 or sys.argv[2]=='mox':
        convert_moxfield_file(sys.argv[1])
    else:
        convert_scryfall_file(sys.argv[1])

