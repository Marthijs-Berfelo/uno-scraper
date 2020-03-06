import requests
from bs4 import BeautifulSoup

import pandas as pd
import random

#naar https://realpython.com/beautiful-soup-web-scraper-python/
#en: https://selenium-python.readthedocs.io/getting-started.html


result = pd.DataFrame(columns=['name', 'img', 'price', 'brandstof'])


URL = 'https://www.renault.nl/modellen.html'
page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser')

#loop door alle tabs heen van renault.nl
for tab in [0, 1, 2, 3, 4]:
    modelviewers = soup.find("div", {"class":"ResponsiveTabs ResponsiveTabs_line RangePicker__tabs"}).find_all("div", {"id":"tab-"+(str)(tab)})[0].find_all("div", {"class":"ModelViewer"})

   #loop door alle auto-modellen van die tab heen 
    for model in modelviewers:
        name = model.find("a",  {"class":'ModelViewer__imageLink'}).text
        image = 'www.renault.nl' + str(model.findAll("img")[1]['src'])
        price = model.find("span", {"class":"ModelViewer__priceNumber"}).text

#        auto_request = 'https://www.renault.nl' + model.find("a", {"class":"ModelViewer__link"})['href'].split('.')[0]+'/technische-gegevens.html'
#        auto = requests.get(auto_request)
#        auto_soup = BeautifulSoup(auto.content, 'html.parser')
#        brandstof = auto_soup.find("p", {"class":"VersionComparatorDetails__subsectionElement"})
        
        #randomize welke brandstof de auto heeft
        brandstof_kans = {'benzine': 100, 'diesel' : 50, 'electrisch': 30}
        gerold = random.random()* 100;
        for brandstof, kans in brandstof_kans.items():
            if  gerold <= kans:
                res_brandstof = brandstof
        

        result = result.append({'name': name, 'img': image, 'price' : price, 'brandstof' : res_brandstof}, ignore_index=True)
        
print(result)



json_result = result.to_json(orient='records')
f = open('renault.json', 'w')
f.write(json_result)
f.close()





