#!/usr/bin/python3


import requests
from bs4 import BeautifulSoup
import csv, sys, os
#url_tmpl = "https://topdeck.ru/apps/toptrade/member/"
url_tmpl = "https://topdeck.ru/apps/toptrade/auctions/finished/"


def download_page(url):
    # Download the page (or read from a local file)
    print(url)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the first table (modify as needed)
    table = soup.find('table')

    # Extract rows
    rows = []
    for tr in table.find_all('tr'):
        cells = [td.get_text(strip=True) for td in tr.find_all(['td', 'th'])]
        if cells:
            rows.append(cells)

    rows.pop(0)
    
    # Write to a tab-separated file
    with open('output.tsv', 'a+', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerows(reversed(rows))


if __name__ == "__main__":
    if len(sys.argv)>2:
        os.remove("output.tsv")
        trader_id = sys.argv[1]
        number_max = int(sys.argv[2])
        url = url_tmpl# + trader_id + "/aucs/"
        for num in range(number_max, 0, -1):
            download_page(url+str(num))

