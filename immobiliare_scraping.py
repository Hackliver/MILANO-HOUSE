from bs4 import BeautifulSoup as bs
import pandas as pd
from urllib import *
import requests
import time
import random
import re

"""
txt_pretty = soup.prettify()
text_file = open(r'pretty_doc', 'w', encoding="utf-8")
text_file.write(txt_pretty)

div = soup.find("div").prettify()
div_text = open(r'preddy_div', 'w', encoding="utf-8")
div_text.write(div)
"""


def get_url(limit=80):
    url1 = "https://www.immobiliare.it/vendita-case/milano/?criterio=rilevanza"
    urls = []
    for pages in range(2, limit):
        url = "https://www.immobiliare.it/vendita-case/milano/?criterio=rilevanza&pag=" + str(pages)
        urls.append(url)

    urls.append(url1)
    return urls


# WEBSITE DECLARATION AND REQUEST
def get_all_announcements_urls(urls):
    print("Fecthing all the announcements urls...")
    all_announcements_urls = []
    for url in urls:
        response = requests.get(url)
        #.status_code
        #print(response.content)
        soup = bs(response.content)
        page_urls = soup.select(".in-card__title")
        page_urls = [url.get("href") for url in page_urls]
        all_announcements_urls.append(page_urls)

    all_announcements_urls = [url for page in all_announcements_urls for url in page]
    return all_announcements_urls


# GO TO EACH ANNOUNCEMENT AND GET INFO
def get_home_soup(url):
    response = requests.get(url)
    soup = bs(response.content)
    return soup, url


# GET PRICE
def get_price(soup):
    div2 = soup.select(".nd-list__item.in-feat__item.in-feat__item--main")
    return div2[0].get_text()


# GET INFORMATION ABOUT THE
def get_main_items(soup):
    main_items = soup.select(".nd-list__item.in-feat__item")
    items_label = ["price", "rooms", "m2", "bathrooms", "floor"]
    items_value = [item.get_text() for item in main_items]
    d_items_main = dict(zip(items_label, items_value))
    return d_items_main


# OTHER ITEMS
def get_other_items(soup):
    other_items = soup.select(".in-realEstateFeatures__list")
    items_label = ["description", "spese_condominio", "energy_class"]
    items_value = [item.get_text() for item in other_items]
    d_items_others = dict(zip(items_label, items_value))
    return d_items_others


# GET ALL ITEMS
def get_all_items(soup):
    all_items = soup.select(".in-realEstateFeatures__title")
    all_items_labels = [item.get_text() for item in all_items]
    all_values = soup.select(".in-realEstateFeatures__value")
    all_items_values = [item.get_text() for item in all_values]
    d_all = dict(zip(all_items_labels, all_items_values))
    return d_all


# ADDRESS
def get_address(soup):
    address = soup.select(".in-location")
    address = [a.get_text() for a in address]
    location_id = ["city", "neighborhood", "address"]
    d_location = dict(zip(location_id, address))
    return d_location


# CREATE PANDAS DATAFRAME
def make_dataframe(href):
    soup, url = get_home_soup(href)
    mergedDict = get_main_items(soup) | get_other_items(soup) | get_all_items(soup) | get_address(soup)
    df = pd.DataFrame(mergedDict, index=[0])
    df['href'] = url
    return df


def read_parquet(all_announcements_urls):
    df = pd.read_parquet('milano_housing_price_raw.parquet.gzip')
    href_done = df['href'].tolist()
    diff = list(set(all_announcements_urls).difference(set(href_done)))
    return diff


def main():
    sleep = random.randint(1, 10)/10

    href = get_url()
    all_announcements_urls = get_all_announcements_urls(href)
    diff = read_parquet(all_announcements_urls)
    print(f"Found {diff} new announcements to scrape")

    df = make_dataframe(href)
    df_update = pd.DataFrame()
    for index, url in enumerate(diff):
        ads_info = make_dataframe(url)
        df_update = pd.concat([df_update, ads_info], axis=0)
        time.sleep(sleep)
        print(f"Scraped {index} webpage")

    df_update = pd.concat([df, df_update], axis=0)
    df_update.to_parquet('milano_housing_price_raw.parquet.gzip', compression='gzip')
    print('done')

main()


#%%


"""
import sqlite3
conn = sqlite3.connect("milan_house_db")
c = conn.cursor()
c.execute("""""")



mylist = soup.select(".in-realEstateFeatures__list")

tags, values = [], []
for tag in mylist[0].find_all("dt"):
    tags.append(tag.get_text())
for value in mylist[0].find_all("dd"):
    values.append(value.get_text())

d = dict(zip(tags, values))
d
#%%
tags, values = [], []
for tag in mylist[1].find_all("dt"):
    tags.append(tag.get_text())
for value in mylist[1].find_all("dd"):
    values.append(value.get_text())

d2 = dict(zip(tags, values))

#%%
body = soup.find("body")
ul = body.find_all("ul")

#%%
mylist = soup.select(".nd-list.nd-list--pipe.in-tabMedia")
mylist[0].get_text()



#%%
x = soup.select(".nd-list.nd-list--pipe.in-feat")

#%% DESCRIZIONE ANNUNCIO
par = soup.find_all("p")
description = [d for d in par][0:25]

#%%
import re

div = soup.find_all("ul", string=re.compile("€"))

#%%
x = soup.find_all('ul')
x2 = []
for i in x:
    if "€" in i.get_text():
        print(i.get_text())
        x2.append(i.get_text())
#x[20].get_text()

#%%
url = "https://www.immobiliare.it/annunci/98498618/"
response = requests.get(url)
response.status_code
print(response.content)
soup = bs(response.content)
soup

txt_home = soup.prettify()
text_file = open(r'txt_home', 'w', encoding="utf-8")
text_file.write(txt_home)

#%%
test2 = []
x = soup.find_all('dd')
for i in x:
    print(i)
    print(i.get_text())
    test2.append(i.get_text())
#x[0].get_text()

#%%
x2 = []
for i in x:
    if "€" in i.get_text():
        print(i.get_text())
        x2.append(i.get_text())

#%%
mylist = soup.select(".in-realEstateFeatures__list")

tags, values = [], []
for tag in mylist[0].find_all("dt"):
    tags.append(tag.get_text())
for value in mylist[0].find_all("dd"):
    values.append(value.get_text())

d = dict(zip(tags, values))
#%%
tags, values = [], []
for tag in mylist[1].find_all("dt"):
    tags.append(tag.get_text())
for value in mylist[1].find_all("dd"):
    values.append(value.get_text())

d2 = dict(zip(tags, values))
#%%

mylist[0].find_all("dd")[0].get_text()
#
#@<dl class="in-realEstateFeatures__list"><dt class="in-realEstateFeatures__title">Riferimento e Data annuncio</dt><dd class="in-realEstateFeatures__value">EK-98498618 - 31/01/2023</dd><dt class="in-realEstateFeatures__title">contratto</dt><dd class="in-realEstateFeatures__value">Vendita</dd><dt class="in-realEstateFeatures__title">unità</dt><dd class="in-realEstateFeatures__value">49 abitative</dd><dt class="in-realEstateFeatures__title">Data di inizio lavori e di consegna prevista</dt><dd class="in-realEstateFeatures__value">01/09/2022 - 30/09/2024</dd><dt class="in-realEstateFeatures__title">tipologia</dt><dd class="in-realEstateFeatures__value">Progetto</dd><dt class="in-realEstateFeatures__title">totale piani edificio</dt><dd class="in-realEstateFeatures__value">4 piani</dd><dt class="in-realEstateFeatures__title">Posti Auto</dt><dd class="in-realEstateFeatures__value">36 in garage/box</dd><dt class="in-realEstateFeatures__title">altre caratteristiche</dt><dd class="in-realEstateFeatures__value in-realEstateFeatures__tagContainer"><span class="in-realEstateFeatures__tag nd-tag">Parcheggio bici</span><span class="in-realEstateFeatures__tag nd-tag">Giardino comune</span><span class="in-realEstateFeatures__tag nd-tag">Infissi esterni in vetro / metallo</span></dd></dl>

#%%
x = {}
for index, row in enumerate(info_rows):
    print(row.find("td").get_text())
    if index==0:
        x['title'] = row.find("td").get_text()
    elif index==1:
        print(row.find("td").get_text())


#%%
soup = bs(response.content)
print(soup.prettify())
#%%
e = soup.body.div.header.select("div", class_="in-wrapper is-detailView in-landingDetail")
e[0].div.select("div", class_="nd-list nd-list--pipe in-tabMedia in-tabMedia--onlyMobile")
e
#%%
mydivs = soup.findAll('div')
for div in mydivs:
    if (div["class"] == "stylelistrow"):
        print(div)

#%%
soup = bs(response, 'html.parser')
print(soup.find('li', attrs={'class': 'spacer'}))

#%%
document.querySelector("#__next > section.in-wrapper.is-detailView.in-landingDetail > div.in-main.in-landingDetail__main > div > ul.nd-list.nd-list--pipe.in-feat.in-feat--full.in-feat__mainProperty.in-landingDetail__mainFeatures > li.nd-list__item.in-feat__item.in-feat__item--main.in-detail__mainFeaturesPrice")
#%%
<li class="nd-list__item in-feat__item in-feat__item--main in-detail__mainFeaturesPrice">€ 4.450.000</li>

#%%
html = requests.get(url).content

# creating soup object
data = bs(html, 'html.parser')
parent = data.find("body").find("ul")
text = list(parent.descendants)
print(text)
for i in range(2, len(text), 2):
    print(text[i], end=" ")

#%%
|#%%
data1 = data.find('ul')
for li in data1.find_all("li"):
    print(li.text, end=" ")


#%%
bs.findAll("span", {"class": "in-ul"})
#%%
c = soup.find(class_="nd-list__item in-feat__item in-feat__item--main in-detail__mainFeaturesPrice")
c
#%%
a_href=soup.find("href",{"class":"nd-icon__use"}).get("href")
a_href
#%%
"""