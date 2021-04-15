#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 15 14:32:54 2021

@author: julia
"""

import requests
from bs4 import BeautifulSoup
from lxml import html

# ustawione filtry: pow > 35m2 i umeblowane: Tak : https://www.olx.pl/nieruchomosci/mieszkania/wynajem/warszawa/?search%5Bfilter_enum_furniture%5D%5B0%5D=yes&search%5Bfilter_float_m%3Afrom%5D=35
# District: Wola: &search%5Bdistrict_id%5D=359
# District: Ursynów: &search%5Bdistrict_id%5D=373
# District: Kabaty
# District: Śródmieście
# District: Mokotów


result = requests.get('https://www.olx.pl/nieruchomosci/mieszkania/wynajem/warszawa/?search%5Bfilter_enum_furniture%5D%5B0%5D=yes&search%5Bfilter_float_m%3Afrom%5D=35')

print(result.status_code)

src = result.content

soup = BeautifulSoup(src, 'lxml')

for a in soup.find_all('a', href=True):
    print (a['href'])

        