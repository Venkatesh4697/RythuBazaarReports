from datetime import datetime

import requests
from bs4 import BeautifulSoup
from boltons import iterutils
import csv


def url_ok(url):
    r = requests.head(url)
    return r.status_code


def get_prices_rbzts():
    url = "http://183.82.5.184/rbzts/DailyPrices.aspx"
    status_code = url_ok(url)
    if status_code == 503 or status_code == 502 or status_code == 504 or status_code == 500:
        return "SCRAPE FAILED! Rbzts Service/Website is currently DOWN or not available"
    else:
        try:
            req = requests.get(url)

            soup = BeautifulSoup(req.content, "html.parser")
            table = soup.find(
                lambda tag: tag.name == 'table' and tag.has_attr('id') and tag[
                    'id'] == "ctl00_ContentPlaceHolder1_GridView1")
            rows = table.findAll(lambda tag: tag.name == 'td')
            prices = []
            fields = ['District', 'Rythu Bazar', 'Vegetable', 'Arrivals', 'LocalMarket Rate', 'RythuBazar Rate']

            for td in rows:
                for child in td.children:
                    for child2 in child.children:
                        prices.append(child2.text.strip())

            it = iterutils.chunked(prices, 6)
            date = str(datetime.today().strftime('%Y%m%d'))
            with(open('rbzts_prices_report_' + date + '.csv', 'w', newline='')) as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(fields)
                writer.writerows(it)
            return "Scrape Success. File generated: " + str(csvfile.name)
        except Exception as e:
            return str(e)


def get_prices_tsmarketing():
    url = "http://tsmarketing.in/DailyArrivalsnPricesCommoditywise.aspx"
    status_code = url_ok(url)
    if status_code == 503 or status_code == 502 or status_code == 504 or status_code == 500:
        return "SCRAPE FAILED! TsMarketing Service/Website is currently not available"
    else:
        try:
            req = requests.get(url)

            soup = BeautifulSoup(req.content, "html.parser")
            table = soup.find(
                lambda tag: tag.name == 'table' and tag.has_attr('id') and tag[
                    'id'] == "ContentPlaceHolder1_GridView1")
            rows = table.findAll(lambda tag: tag.name == 'tr')
            prices = []
            rowspan = 0
            item = ''

            for td in rows:
                if rowspan > 0:
                    prices.append(item)
                    rowspan = rowspan - 1
                for child in td.children:
                    if child.getText() != '\n':
                        if child.get('rowspan') is not None:
                            rowspan = int(child.get('rowspan')) - 1
                            item = child.text.strip()
                        prices.append(child.text.strip())

            it = iterutils.chunked(prices, 8)
            date = str(datetime.today().strftime('%Y%m%d'))
            with(open('tsmarketing_prices_report_' + date + '.csv', 'w', newline='')) as csvfile:
                writer = csv.writer(csvfile)
                writer.writerows(it)
            return "Scrape Success. File generated: " + str(csvfile.name)
        except Exception as e:
            return str(e)


def get_prices_tsmarketing_marketwise():
    url = "http://tsmarketing.in/DailyArrivalsnPrices.aspx"
    status_code = url_ok(url)
    if status_code == 503 or status_code == 502 or status_code == 504 or status_code == 500:
        return "SCRAPE FAILED! TsMarketing Service/Website is currently not available"
    else:
        try:
            req = requests.get(url)

            soup = BeautifulSoup(req.content, "html.parser")
            table = soup.find(
                lambda tag: tag.name == 'table' and tag.has_attr('id') and tag[
                    'id'] == "ContentPlaceHolder1_GridView1")
            rows = table.findAll(lambda tag: tag.name == 'tr')
            prices = []
            rowspan = 0
            item = ''

            for td in rows:
                if rowspan > 0:
                    prices.append(item)
                    rowspan = rowspan - 1
                for child in td.children:
                    if child.getText() != '\n':
                        if child.get('rowspan') is not None:
                            rowspan = int(child.get('rowspan')) - 1
                            item = child.text.strip()
                        prices.append(child.text.strip())

            it = iterutils.chunked(prices, 8)
            date = str(datetime.today().strftime('%Y%m%d'))
            with(open('tsmarketing_marketwise_prices_report_' + date + '.csv', 'w', newline='')) as csvfile:
                writer = csv.writer(csvfile)
                writer.writerows(it)
            return "Scrape Success. File generated: " + str(csvfile.name)
        except Exception as e:
            return str(e)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    rbzts_response = get_prices_rbzts()
    print(rbzts_response)

    tsmarketing_response = get_prices_tsmarketing()
    print(tsmarketing_response)

    tsmarketing_marketwise_response = get_prices_tsmarketing_marketwise()
    print(tsmarketing_marketwise_response)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
