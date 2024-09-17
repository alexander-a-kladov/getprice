# getprice
get prices for collection of mtg cards via rest api from scryfall, and other functions

install:
download, add execute mode to *.py files, through chmod a+x *.py
install all required python packages, through pip install <package>
create local sqlite mycards.db, through cd create_db ./create_db.py and ./create_tables.py

usage:
to get lists with prices and names (from scryfall.com)
./getprice.py topdeck_tmpl.txt topdeck_modern.txt ... topdeck_foils.txt

output: topdeck.txt, topdeck.html
it saves some information to sqlite mycards.db, names, prices when works, to not save data of prices use
./getprice.py test all topdeck_tmpl.txt topdeck_modern.txt ... topdeck_foils.txt
'all' can be changed to name of set lower case (e.g. mh1, akh ...) or ">price"/"<price", to show cards only of some set and price that greater/lesser then price

price_modificators:
you can modify prices mutiplicatos for sets by adding new records to price_dict inside getprice.py script, default value is 1.0, or add multiplicator for every card in input txt files e.g. 1.2
you can write fixed price for some card e.g. 100

to remove cards from topdeck_lists input files
./findandremove.py name_set_number_attributes_list.txt

to get topdeck_lists from lists of card names, e.g. to evaluate prices for mass cards sale auctions on topdeck.ru
./wanttobuy.py quantity_name_list

to get topdeck_list from exported moxfield.com lists, or something exported from scryfall (or other unknown site)
./moxfield_convert.py file.list mox, or ./moxfield_convert.py file.list

to sort html files in descending price order
./sort_results.py topdeck.html

find cards in mycards.db by deck lists exported from mtggoldfish.com
./find_cards.py mtggoldfish_deck.txt

other script should not be used without understand what they do
all script are used as is, without any guarantee
