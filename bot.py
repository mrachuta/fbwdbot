# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from datetime import datetime, timedelta
import getpass
import random
import re
import os

"""Facebook bot created using WebDriver package"""

print('FBWebDriver Bot Beta')
print('Za chwilę zostaniesz poproszony o login i hasło do serwisu Facebook')

time.sleep(3)

tempUL = input('Podaj login do konta na FB \n')
tempPW = getpass.getpass('Podaj hasło do konta %s \n' % tempUL)

time.sleep(3)

idsource = 'id.dat'

if os.path.exists(idsource) == True:
    file = open(idsource, 'r')
    tempPID = file.readline()
    print('Znaleziono plik %s, a w nim id partnera do konwersacji: %s' %(idsource, tempPID))

else:
    print('Nie znaleziono pliku %s, ' % (idsource))
    tempPID = input('Podaj id partnera do konwersacji ręcznie \n')

print('Rozpoczynam działanie')

class Core:

    driver = webdriver.Firefox()

    def __init__(self):

        self.url = 'https://facebook.com/' #do not change this value - bot is only for Facebook!!
        self.userLogin = tempUL
        self.userPass = tempPW
        self.partnerId = tempPID
        self.messagesList =[] #messages found during i-iteration
        self.responseDb = {} #array with loaded database.txt file

    def open_site(self):

        Core.driver.get(self.url)
        siteTitle = Core.driver.title
        assert 'Facebook' in siteTitle, 'Nie odnaleziono strony' #check that site was loaded

    def close_cookie_monit(self):

        #function only for demonstration purposses - this is not necessary

        closeCookieMonitXPath = '//button[@class="_42ft _5upp _5la0"]'
        closeCookieMonitButtonField = Core.driver.find_element_by_xpath(closeCookieMonitXPath)
        closeCookieMonitButtonField.click()

    def login_site(self):

        loginXPath = '//input[@id="email"]'
        passwordXPath = '//input[@id="pass"]'
        loginButtonXPath = '//input[(@value="Zaloguj się" or @value="Log In")]' #login button for Polish or English version of FB

        loginInputField = Core.driver.find_element_by_xpath(loginXPath)
        loginInputField.clear()
        loginInputField.send_keys(self.userLogin)
        passwordInputField = Core.driver.find_element_by_xpath(passwordXPath)
        passwordInputField.clear()
        passwordInputField.send_keys(self.userPass)
        loginButtonField = Core.driver.find_element_by_xpath(loginButtonXPath)
        loginButtonField.click()

        #This code below, confirm that fb user data (userLogin and userPass) is correct

        assert (len(Core.driver.find_elements_by_xpath('//div[@id="userNavigationLabel"]')) > 0 ), "Nie zalogowano. Czy podałeś prawidłowy login i/lub hasło?"

    def find_partner(self):

        Core.driver.get('https://www.facebook.com/messages/t/%s' % self.partnerId)

        #code below checks, that partnerId is valid

        assert self.partnerId in Core.driver.page_source, "Nie odnaleziono użytkownika. Na pewno dobrze wpisałeś numer użytkownika?"

    def send_message(self, message):

        chatWindowXPath = '//div[@class="notranslate _5rpu"]'

        #code below check that new message field exists

        assert 'notranslate _5rpu' in Core.driver.page_source, "Nie odnaleziono pola wysyłania wiadomości. Sprawdź zmienną chatWindowXPath."

        chatWindowField = Core.driver.find_element_by_xpath(chatWindowXPath)
        chatWindowField.clear()

        chatWindowField.send_keys(message)
        chatWindowField.send_keys(Keys.ENTER)
        chatWindowField.clear()

    def read_messages(self):

        #below is the list of the chars, which will be removed from incoming messages

        inappChars = {'ą':'a','ć':'c','ę':'e','ł':'l','ń':'n','ó':'','ś':'s','ż':'z','ź':'z'}
        getCurrentTime = datetime.now()
        getPastTime = getCurrentTime - timedelta(minutes=1)
        currentTime = getCurrentTime.strftime('%H:%M')
        pastTime = getPastTime.strftime('%H:%M')

        print(currentTime)
        print(pastTime)

        #search for messages from current time and (current time - 1 minute) - this statement assure, that all messages will be found

        messageXPath = '//div[@data-tooltip-position="left" and (@data-tooltip-content="%s" or @data-tooltip-content="%s")]' % (
        currentTime, pastTime)
        messages = Core.driver.find_elements_by_xpath(messageXPath)

        if len(messages) > 0:

            for message in messages:

                messageFirstAtt = message.get_attribute('body')
                messageFirstAtt = messageFirstAtt.lower()

                for char in messageFirstAtt: #for every character in Message
                    if char in inappChars: #if char is in inappChars list

                        key = inappChars[char]
                        messageFirstAtt = messageFirstAtt.replace(char, key)

                    else:

                        1 == 1

                messageSecAtt = message.get_attribute('data-tooltip-content')
                message = " / ".join([messageFirstAtt, messageSecAtt])
                self.messagesList.append(message) #add to list in form: "Message / time'

            else:

                1 == 1

        print('Znalazłem %i wiadomości.' % len(self.messagesList))

    def readdb(self):

        '''file with keys as 'part-of-message' and values as responses for this keys
        coding inside file - windows-1250, otherwise there is problem with polish letters ąść etc...'''

        fileName = 'database.txt'

        #code below check that file exists; this is the file with responses for messages.

        assert os.path.exists(fileName), "Plik database.txt w katalogu skryptu nie istnieje."
        file = open(fileName, 'r')


        for line in file:
            cutChar = line.find(';')
            endChar = line.find('\n')
            p1 = line[:cutChar]
            p2 = line[cutChar + 1:endChar]
            self.responseDb[p1] = p2

        file.close()

    def weather(self):

        zipCode = [z for z in self.messagesList if ("-" in z and z not in oldMessagesList)] #search all elements in messagesList, and add element with '-'

        if (len(zipCode) > 1 or len(zipCode) == 0):

            Core.send_message(self, 'Nie podałeś kodu lub podałeś go w innej niż wymagana formie. Użyj proszę ponownie funkcji i podaj kod pocztowy.')

        else:

            #code below extract zip-Code from string in polish zip-code format XX-XXX

            x = zipCode[0]
            y = x.find("-")
            pureZipCode = x[(y - 2):(y + 4)]

            Core.send_message(self, 'Oto pogoda dla twojego regionu: https://openweathermap.org/find?q=%s - wejdź i wybierz dokładną miejscowość/dzielnicę' % pureZipCode)

    def pajacyk(self):

        Core.send_message(self, 'http://pajacyk.pl')
        Core.send_message(self, 'Kliknij proszę w brzuszek!')

    def close(self):

        Core.send_message(self, 'Zakańczam pracę, żegnaj!')
        time.sleep(3)
        if 1 == 1:
            quit()

#start main part of script

c = Core()

print('Wybrana strona to %s' %c.url)

c.readdb()
dBPositions = len(c.responseDb)

print('Wczytałem listę odpowiedzi... %s odpowiedzi' % (dBPositions))

print('Loguje się do serwisu %s używając loginu %s' % (c.url , c.userLogin))

print('Otwieram stronę')

c.open_site()

print('Zamykam monit dotyczący ciasteczek')

c.close_cookie_monit()

print('Loguję się do serwisu')

c.login_site()

print('Wybieram parntera do konwersacji: %s' %c.partnerId)

c.find_partner()

time.sleep(5)

print('Witam się')

helloList = ['Siema','Witaj', 'Elo', 'Dzień Dobry', 'Hej', 'Dobry', 'Cześć', 'Hi!']

c.send_message(random.choice(helloList))
c.send_message('Jestem botem. Możesz coś do mnie napisać, lub wydać mi polecenie.')
c.send_message('Lista dostępnych poleceń:\n /weather <kod pocztowy> (np. /weather 61-001) \n /pajacyk \n /close')
c.send_message('Oczekuję na dalszą reakcję...')

print('Nasłuchuję i rozmawiam...')

oldMessagesList = [] #list with responded messages
commandsList = {'weather':c.weather ,'pajacyk':c.pajacyk ,'close':c.close}

while True:

    c.read_messages()

    if len(c.messagesList) > 0:

        '''response only to messages which are not in oldMessagesList -> take messages from c.messagesList
        (filled in each i-iteration) which are not in oldMessagesList and store it in newMessagesList'''

        newMessagesList = [message for message in c.messagesList if message not in oldMessagesList]
        print('Na %s wiadomości muszę odpisać' %len(newMessagesList))

        for message in newMessagesList:

            if any(command in message for command in commandsList): #search for command in message

                receivedCommand = ''.join(re.findall('[a-zA-Z]+', message))
                commandToRun = commandsList[receivedCommand]
                commandToRun()
                oldMessagesList.append(message)

            elif any(key in message for key in c.responseDb): #search in database.txt for specified key(string) in incoming message, to send a response to this message

                for key in c.responseDb:

                    if key in message:
                        response = c.responseDb[key]
                        c.send_message(response)
                        oldMessagesList.append(message)

                    else: #do nothing

                       1 == 1

            else: #if message was searched for key(string) and command, and nothing found

                 c.send_message('Odpisuję, nie mam tego w database.txt')
                 oldMessagesList.append(message)


    else:

        1 == 1

    del c.messagesList[:] #delete incoming message list; for next loop (next i+1 iteration)
    print('Ilość wiadomości na które odpisałem od uruchomienia: %s' % len(oldMessagesList))
    time.sleep(5)