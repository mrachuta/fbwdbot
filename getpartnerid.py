# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup as bs4

def get_id(url):

    myheaders = requests.utils.default_headers()
    myheaders.update(
        {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0',
        }
    )

    q = requests.get(url, headers = myheaders)
    r = q.text

    soup = bs4(r, 'html.parser')
    partnerid = soup.find(property = 'al:android:url').get('content')[13:]
    return partnerid

print('Za chwilę zostaniesz poproszony o link do profilu osoby z którą chcesz rozmawiać za pośrednictwem bota')
url = input('-> Podaj link do profilu w formacie http[/s]://facebook.[com/pl]/nazwauzytkownika: \n')

pureid = get_id(url)

idsource = 'id.dat'

while True:

    choose = input('-> Czy chcesz zapisać te dane? [T]ak/[N]ie/[A]nuluj \n')

    if choose == 'T':
        file = open(idsource, 'w')
        file.write(pureid)
        file.close()
        print('Zapisano w pliku %s' %(idsource))
        break
    elif choose == 'N':
        print('-> OK, nie zapisuje; skopiuj wartość pomiędzy >> << do schowka.')
        print('>>' + pureid + '<<' )
        break
    elif choose == 'A':
        print('-> Zamykam')
        quit()






