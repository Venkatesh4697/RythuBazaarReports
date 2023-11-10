from datetime import datetime

import requests
from bs4 import BeautifulSoup
from serpapi import GoogleSearch
from boltons import iterutils
import csv


def soap_call():
    url = "https://prdchub506.unix.gsm1900.org:4443/eai_anon_enu/start.swe?SWEExtSource=AnonWebService&SWEExtCmd=Execute"

    # structured XML
    payload = """<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
   <soap:Body>
      <ns2:SearchCustomerSummary_Input xmlns="http://www.t-mobile.com/u2/xml/TMOCustomerSummaryIO" xmlns:ns2="http://www.t-mobile.com/u2/mdm/customer" xmlns:ns3="http://www.t-mobile.com/u2/xml/PostpaidU2CCIDLookUp">
         <ListOfCustomerSummary>
            <CustomerSummary>
               <BAN>70448180</BAN>
            </CustomerSummary>
         </ListOfCustomerSummary>
         <ns2:PageSize>10</ns2:PageSize>
         <ns2:StartRowNum>0</ns2:StartRowNum>
      </ns2:SearchCustomerSummary_Input>
   </soap:Body>
</soap:Envelope>"""
    # headers
    headers = {
        'Content-Type': 'text/xml; charset=utf-8'
    }
    # POST request
    response = requests.request("POST", url, headers=headers, data=payload, verify=False)

    # prints the response
    print(response.text)
    print(response)


def get_hospitals_from_google():
    params = {
        "engine": "google_maps",
        "q": "hospitals in hyderabad",
        "type": "search",
        "location": "Hyderabad,Telangana",
        "api_key": "69e943f98d9e05e989b6231ebf20a0c9f26b13ee62b14efd78a344d190959adf"
    }
    client = GoogleSearch(params)
    data = client.get_dict()
    for result in data['local_results']:
        print(f"""
    Title: {result['title']}
    Address: {result['address']}
    Rating: {result['rating']}
    Reviews: {result['reviews']}""")


def get_hospitals_from_medifee():
    req = requests.get(
        "https://www.medifee.com/hospitals-in-hyderabad")

    soup = BeautifulSoup(req.content, "html.parser")
    table = soup.find(lambda tag: tag.name == 'tbody')
    rows = table.findAll(lambda tag: tag.name == 'tr')
    hospital_names = []

    for td in rows:
        for child in td.children:
            for child2 in child.children:
                hospital_names.append(child2.text.strip())

    for string in hospital_names:
        if string == '\n' or string == ' ':
            hospital_names.remove(string)
    newList = list(filter(None, hospital_names))

    print(newList)

    # print(newList)


def get_prices():
    req = requests.get(
        "http://183.82.5.184/rbzts/DailyPrices.aspx")

    soup = BeautifulSoup(req.content, "html.parser")
    table = soup.find(lambda tag: tag.name == 'table' and tag.has_attr('id') and tag['id']=="ctl00_ContentPlaceHolder1_GridView1")
    rows = table.findAll(lambda tag: tag.name == 'td')
    prices = []
    fields = ['District','Rythu Bazar','Vegetable','Arrivals','LocalMarket Rate','RythuBazar Rate']

    for td in rows:
        for child in td.children:
            for child2 in child.children:
                prices.append(child2.text.strip())

    it = iterutils.chunked(prices,6)
    date = str(datetime.today().strftime('%Y%m%d'))
    with(open('prices_report_'+date+'.csv','w',newline='')) as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(fields)
        writer.writerows(it)
    print(it)


def get_hospitals_from_websites():
    req = requests.get(
        "https://www.nirujahealthtech.com/15-best-hospitals-in-hyderabad/")
    str_list = []

    soup = BeautifulSoup(req.content, "html.parser")

    tag = soup.body
    # div_tag = tag.find('div', {'class': 'entry-content clear'})
    for string in tag.strings:
        str_list.append(string)

    # str_list = [x for x in str_list if x]

    for string in str_list:
        if string == '\n' or string == ' ':
            str_list.remove(string)

    for s in str_list:
        print(s)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # soap_call()
    # get_hospitals_from_websites()
    # get_hospitals_from_google()
    #get_hospitals_from_medifee()
    get_prices()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
