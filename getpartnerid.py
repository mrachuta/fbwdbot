# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup as bs4

"""
Addon to FBWebDriver Bot.
This tool helps you to get facebook user id in 
(digit form) - if FB user profile is public available.
If you want this value can be saved and used every time when you run bot.
"""

def get_id(url):

    my_headers = requests.utils.default_headers()
    my_headers.update(
        {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0',
        }
    )

    q = requests.get(url, headers=my_headers)
    r = q.text

    soup = bs4(r, 'html.parser')

    # Check that user insert valid http adress to profile

    assert 'al:android:url' in r, "Brak ID w kodzie strony. Podałeś na pewno poprawny adres do profilu na facebook'u? Być może profil nie jest publicznie dostępny?"

    partner_id = soup.find(property='al:android:url').get('content')[13:]
    return partner_id


print('Za chwilę zostaniesz poproszony o link do profilu osoby z którą chcesz rozmawiać za pośrednictwem bota')
url = input('-> Podaj link do profilu w formacie http[/s]://facebook.[com/pl]/nazwauzytkownika: \n')

pure_id = get_id(url)
id_source = 'id.dat'

while True:

    choose = input('-> Czy chcesz zapisać te dane? [T]ak/[N]ie/[A]nuluj \n')

    if choose == 'T':
        file = open(id_source, 'w')
        file.write(pure_id)
        file.close()
        print('Zapisano w pliku %s' % id_source)
        break
    elif choose == 'N':
        print('-> OK, nie zapisuje; skopiuj wartość pomiędzy >> << do schowka.')
        print('>>' + pure_id + '<<' )
        break
    elif choose == 'A':
        print('-> Zamykam')
        quit()






