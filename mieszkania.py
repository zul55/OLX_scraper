#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 15 14:32:54 2021

@author: julia
"""

# TODO -----------------------------------------------------------------------
# - stworzenie zmiennych: dzielnica (w której ma szukać), powierzchnia (od), ktore beda podawane do adresu url
# - dostosowanie result do podawania zmiennych
# - for nie dziala - URUCHOMIC
# - niektore ogloszenia prowadza do serwisu otodom - dostosuj for loop'a
# - dodanie zmiany strony main_page (po wiecej ogłoszeń)
# - dodanie sortowania dataframu po cenie lub po indeksie i zapisywanie top x wyników jako plik np. excel

# ustawione w result filtry: pow > 35m2 i umeblowane: Tak. Tak wyglada link z tymi filtrami: https://www.olx.pl/nieruchomosci/mieszkania/wynajem/warszawa/?search%5Bfilter_enum_furniture%5D%5B0%5D=yes&search%5Bfilter_float_m%3Afrom%5D=35
# Do dodania na końcu tego url: (jesli chcemy)
# District: Wola: &search%5Bdistrict_id%5D=359
# District: Ursynów: &search%5Bdistrict_id%5D=373
# District: Kabaty
# District: Śródmieście
# District: Mokotów

import requests
from bs4 import BeautifulSoup
import pandas as pd


# sciaga sobie dane z podanego adresu url
result = requests.get('https://www.olx.pl/nieruchomosci/mieszkania/wynajem/warszawa/?search%5Bfilter_enum_furniture%5D%5B0%5D=yes&search%5Bfilter_float_m%3Afrom%5D=35')

#sprawdza na wszelki wypadek czy jest polaczenie
print(result.status_code)

# z result interesuje nas tylko html i tu sie on wyciaga
src = result.content

# wrzucamy html do soup'a, ktory umozliwia prace na html
main_page = BeautifulSoup(src, 'html.parser')


#tworze pusty dataframe, do ktorego beda zapisywac sie wyniki
column_names = ["Indeks", "Cena całkowita", "Metraż", "Link"]
df = pd.DataFrame(columns = column_names)


#for nie dziala, wiec probuje cos z tym zrobic dzieki asseS
asses = main_page.find_all('a', href=True)
asses[75]['href']

#zmienna do sprawdzania if'a w for loop'ie
#a = 'https://www.olx.pl/d/oferta/fajne-38m2-z-osobna-sypialnia-na-ochocie-geodetow-12-CID3-IDJ4kid.html#ebfa53869f;promoted'

for a in asses:
    # a['href'] to adres url w formie Stringa, if sprawdza czy prowadzi do ogloszenia TEORETYCZNIE - SPRAWDZ
    if a['href'].startswith('https://www.olx.pl/oferta/'):
        #przypisuje zawartosc url do zmiennej link
        link = requests.get(a['href'])
        #wrzuca zawartosc strony do soup'a, zeby pracowac z zawartoscia
        offer_page = BeautifulSoup(link.content, 'html.parser')
        #sciaga cene z ogloszenia - sciaga sie w formacie 'x xxx zł'
        cena_podst_str = offer_page.find('h3', class_ ='css-8kqr5l-Text eu5v0x0').text
        #robi ze stringa, liste int'ow
        cena_podst = [int(s) for s in cena_podst_str.split() if s.isdigit()]
        #sciaga pola z dodatkowymi informacjami o mieszkaniu
        pola = offer_page.find_all('p', class_= "css-xl6fe0-Text eu5v0x0")
        #sciaga metraz - w formacie 'Powierzchnia: xx m2'
        metraz_str = pola[4].text
        #robi ze stringa, liste int'ow
        metraz = [int(s) for s in metraz_str.split() if s.isdigit()][0]
        #sciaga dodatkowy czynsz - w formacie 'Czynsz (dodatkowo): xxx zł'
        czynsz_str = pola[6].text
        #robi ze stringa, liste int'ow
        czynsz = [int(s) for s in czynsz_str.split() if s.isdigit()][0]
        
        #liczy cene razem z dodatkowym czynszem
        cena = cena_podst[0] * 1000 + cena_podst[1] + czynsz
        #liczy cene za m2
        indeks = cena / metraz
        #dict z wynikami do dataframu
        row = {"Indeks": indeks, "Cena całkowita": cena, "Metraż": metraz, "Link": a['href']}
        #dodaje wiersz do dataframu
        df = df.append(row, ignore_index=True)
    else:
        continue
    
    
    
    
    
    
    
    
    
    
    
    
    
    