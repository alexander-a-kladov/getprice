#!/usr/bin/python3
# coding: utf8

import sys, requests, json

inTopic = False
result_html = 'topdeck.html'

def write_html_headers():
    fhtml.write('<html>')
    style_f = open('html/style.html', 'r')
    fhtml.write(style_f.read())
    fhtml.write('<body>')
    contacts_f = open('html/contacts.html', 'r')
    fhtml.write(contacts_f.read())
    topdeck_search_f = open('html/topdeck_search.js', 'r')
    fhtml.write('<script>')
    fhtml.write(topdeck_search_f.read())
    fhtml.write('</script>\n')


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


def write_html(filename):
    global fhtml, inTopic
    album_names = {"Стандарт:": "Standard.png", "Пионер:": "Pioneer.png", "Модерн:": "Modern.png",
                  "Коммандер:": "Commander.jpg", "Фойл:": "Foil.jpg", "Пайло:": "Piles.jpg"}
    mana_symbols = {":w::w::w:": "w.html", ":u::u::u:": "u.html", ":b::b::b:": "b.html", ":r::r::r:": "r.html",
                   ":g::g::g:": "g.html", ":c:": "colorless.html", ":mc:": "multicolor.html"}
    album_spoilers_f = open('html/album_spoilers.html', 'r')
    album_spoilers = album_spoilers_f.read()
    album_spoilers_f.close()
    f = open(filename, 'r')
    for line in f:
        if line.strip() in album_names:
            if inTopic:
                fhtml.write("</details></p>")
            fhtml.write(album_spoilers.replace('Topic_Name', '<img src=images/' + album_names[
                line.strip()] + ' alt=' + line.strip() + ' width=360px height=80px>'))
            inTopic = True
        if line[0] == '-':
            continue
        key, quantity, price = get_data(line)
        if not key:
            continue
        url = "https://api.scryfall.com/cards/"
        str0 = key.split('(')[1].split('/')[0].lower()
        str0 += "/"+key.split('(')[1].split('/')[1].split(')')[0]
        url = url + str0

        r = requests.get(url)
        if r.status_code == 404:
            print(f'{url} error=404')
            continue
        token = json.loads(r.text)
        image_uris = token.get('image_uris')
        if image_uris:
            image_url = image_uris.get('small')
        else:
            image_url = token.get('card_faces')[0].get('image_uris').get('small')
        fhtml.write('<div id="container">')
        # fhtml.write('<p>'+str(price)+' р </p>')
        fhtml.write('<input style="width:100px" type="number" />')
        fhtml.write(' <img src=')
        fhtml.write(image_url)
        fhtml.write(' alt=')
        fhtml.write('"' + str0[0].replace(" - ", "") + '"')
        fhtml.write(' height="230px"')
        fhtml.write(' onclick=comparePrice("')
        if card_name:
            compare_card_name = card_name.replace(' ', '+')
        else:
            parser = re.search('[0-9]x ', line)
        if parser:
            compare_card_name = str0[0][parser.end():].split('(')[0].strip().strip('-').strip().replace(' ', '+')
        else:
            compare_card_name = str0[0].split('(')[0].strip().strip('-').strip().replace(' ', '+')
        fhtml.write(compare_card_name)
        fhtml.write('",')
        fhtml.write('"' + en_name.replace(' ', '+') if en_name else '')
        fhtml.write('")')
        fhtml.write('>')
        fhtml.write('<h2><span>')
        if quantity > 1:
            fhtml.write(str(quantity)+"x  "+str(price) + ' р')
        else:
            fhtml.write("    " + str(price) + ' р')
        fhtml.write('</span></h2><p>')
        if get_set_present(line):
            fhtml.write(str0[0] + '<wbr>' + str1[1].strip() + '<wbr>')
        else:
            fhtml.write(str0[0] + '<wbr>' + '(' + mtgset.swapcase() + '/' + str(number) + ')' + '<wbr>' + str1[
                                1].strip() + '<wbr>')
        if foil:
            fhtml.write(' FOIL')
        if promo:
            fhtml.write(' promo')
        fhtml.write('</p>')
        fhtml.write('</div>')
        fhtml.write('\n')


if __name__ == '__main__':
    count_args = 0
    if len(sys.argv) < 2:
        print("usage: create_html.py file_tmpl.txt file_tmpl1.txt")
    else:
        print(sys.argv[1])
        fhtml = open(result_html, 'w')
        write_html_headers()
        if sys.argv[1] == "test":
            test_set = sys.argv[2]
            test = True
            if test_set[0] != '>' and test_set[0] != '<':
                print("test_set=" + test_set)
            else:
                print("test_price=" + test_set)
        write_html("topdeck.txt")
        close(fhtml)
