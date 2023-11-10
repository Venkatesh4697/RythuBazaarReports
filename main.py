from datetime import datetime

import requests
from bs4 import BeautifulSoup
from boltons import iterutils
import csv


def get_prices():
    req = requests.get(
        "http://183.82.5.184/rbzts/DailyPrices.aspx")

    soup = BeautifulSoup(req.content, "html.parser")
    table = soup.find(
        lambda tag: tag.name == 'table' and tag.has_attr('id') and tag['id'] == "ctl00_ContentPlaceHolder1_GridView1")
    rows = table.findAll(lambda tag: tag.name == 'td')
    prices = []
    fields = ['District', 'Rythu Bazar', 'Vegetable', 'Arrivals', 'LocalMarket Rate', 'RythuBazar Rate']

    for td in rows:
        for child in td.children:
            for child2 in child.children:
                prices.append(child2.text.strip())

    it = iterutils.chunked(prices, 6)
    date = str(datetime.today().strftime('%Y%m%d'))
    with(open('prices_report_' + date + '.csv', 'w', newline='')) as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(fields)
        writer.writerows(it)
    print(it)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    get_prices()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
