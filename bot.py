# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from datetime import datetime, timedelta
import getpass
import random
import re
import os
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.action_chains import ActionChains

""" Facebook bot created using WebDriver package """

print('[FBWDBot v 1.0 - Facebook WebDriver Bot')
print('Za chwilę zostaniesz poproszony o login i hasło do serwisu Facebook')

time.sleep(3)

temp_ul = input('Podaj login do konta na FB \n')
temp_pw = getpass.getpass('Podaj hasło do konta %s \n' % temp_ul)

time.sleep(3)

id_source = 'id.dat'  # File with saved conversation's partner id

# Function below, check, that file from id_source variable exists or not and do action

if os.path.exists(id_source is True):
    file = open(id_source, 'r')
    temp_pid = file.readline()
    print('Znaleziono plik %s, a w nim id partnera do konwersacji: %s' % (id_source, temp_pid))

else:
    print('Nie znaleziono pliku %s, ' % id_source)
    temp_pid = input('Podaj id partnera do konwersacji ręcznie \n')

print('Rozpoczynam działanie')


class Core:

    # If there are some problems with run Firefox instance, check paths below
    firefox_path = 'C:\\Program Files\\Mozilla Firefox\\firefox.exe'
    gecko_path = 'C:\\Program Files\\Mozilla Firefox\\geckodriver.exe'

    driver = webdriver.Firefox(firefox_binary=FirefoxBinary(firefox_path), executable_path=gecko_path)

    def __init__(self):

        # Do not change this value - bot is only for Facebook!!
        self.url = 'https://facebook.com/'
        self.user_login = temp_ul
        self.user_pass = temp_pw
        self.partner_id = temp_pid
        self.messages = []  # Messages found during i-iteration
        self.response_db = {}  # Array with loaded database.txt file

    def open_site(self):

        Core.driver.get(self.url)
        site_title = Core.driver.title
        # Check that site was loaded
        assert 'Facebook' in site_title, 'Nie odnaleziono strony'

    def close_cookie_monit(self):

        # Function only for demonstration purposes - this is not necessary
        close_cookie_monit_xpath = '//button[@class="_42ft _5upp _5la0"]'
        close_cookie_monit_button = Core.driver.find_element_by_xpath(close_cookie_monit_xpath)
        close_cookie_monit_button.click()

    def login_site(self):

        login_xpath = '//input[@id="email"]'
        password_xpath = '//input[@id="pass"]'
        # Login button for Polish or English version of FB
        login_button_xpath = '//input[(@value="Zaloguj się" or @value="Log In")]'

        login_input = Core.driver.find_element_by_xpath(login_xpath)
        login_input.clear()
        login_input.send_keys(self.user_login)
        password_input = Core.driver.find_element_by_xpath(password_xpath)
        password_input.clear()
        password_input.send_keys(self.user_pass)
        login_button = Core.driver.find_element_by_xpath(login_button_xpath)
        login_button.click()

        # This code below, confirm that fb user data (userLogin and userPass) is correct

        assert (len(Core.driver.find_elements_by_xpath('//div[@id="userNavigationLabel"]')) > 0), \
            "Nie zalogowano. Czy podałeś prawidłowy login i/lub hasło?"

    def find_partner(self):

        Core.driver.get('https://www.facebook.com/messages/t/%s' % self.partner_id)
        assert self.partner_id in Core.driver.page_source, \
            "Nie odnaleziono użytkownika. Na pewno dobrze wpisałeś numer użytkownika?"

    def send_message(self, message):

        chat_window_xpath = '//div[@class="notranslate _5rpu"]'

        # Code below check that new message field exists

        assert 'notranslate _5rpu' in Core.driver.page_source, \
            "Nie odnaleziono pola wysyłania wiadomości. Sprawdź zmienną chatWindowXPath."

        chat_window_field = Core.driver.find_element_by_xpath(chat_window_xpath)
        chat_window_field.send_keys(message)
        chat_window_field.send_keys(Keys.ENTER)

    def read_messages(self):

        # Below is the list of the chars, which will be removed from incoming messages
        inapp_chars = {'ą': 'a', 'ć': 'c', 'ę': 'e', 'ł': 'l', 'ń': 'n', 'ó': 'o', 'ś': 's', 'ż': 'z', 'ź': 'z'}
        get_current_time = datetime.now()
        get_past_time = get_current_time - timedelta(minutes=1)
        current_time = get_current_time.strftime('%H:%M')
        past_time = get_past_time.strftime('%H:%M')

        print(current_time)
        print(past_time)

        message_xpath = '//div[contains(@class, "clearfix")]/div[@data-tooltip-position="left" and ' \
                        '(@data-tooltip-content="%s" or @data-tooltip-content="%s")]' % (current_time, past_time)
        messages = Core.driver.find_elements_by_xpath(message_xpath)

        if len(messages) > 0:

            for message in messages:

                message_text = message.get_attribute('innerText').lower()
                for char in message_text:  # For every character in Message

                    if char in inapp_chars:  # If char is in inappChars list
                        message_text = message_text.replace(char, inapp_chars[char])

                    else:
                        pass

                message_time = message.get_attribute('data-tooltip-content')
                message = " / ".join([message_text, message_time])
                self.messages.append(message)  # Add to list in form: "Message / time'

            else:
                pass

        print('Znalazłem %i nowych wiadomości.' % len(self.messages))
        print(self.messages)

    def read_db(self):

        """ File with keys as 'part-of-message' and values as responses for this keys
        coding inside file - windows-1250, otherwise there is problem with polish letters ąść etc... """

        file_name = 'database.txt'

        # Code below check that file exists; this is the file with responses for messages.
        assert os.path.exists(file_name), "Plik database.txt w katalogu skryptu nie istnieje."
        db_file = open(file_name, 'r')

        for line in db_file:
            cut_char = line.find(';')
            end_char = line.find('\n')
            key = line[:cut_char]
            value = line[cut_char + 1:end_char]
            self.response_db[key] = value

        file.close()

    def weather(self):

        # Search all elements in messagesList, and look for an element with '-'
        zip_code = [z for z in self.messages if ("-" in z and z not in old_messages)]

        if len(zip_code) > 1 or len(zip_code) == 0:

            Core.send_message(self, 'Nie podałeś kodu lub podałeś go w innej niż wymagana formie.')
            Core.send_message(self, 'Użyj proszę ponownie funkcji i podaj kod pocztowy.')

        else:

            # Code below extract zip-Code from string in polish zip-code format XX-XXX
            x = zip_code[0]
            y = x.find("-")
            pure_zip_code = x[(y - 2):(y + 4)]

            Core.send_message(self,
                              'Oto pogoda dla twojego regionu: wejdź i wybierz dokładną miejscowość/dzielnicę')
            Core.send_message(self, 'https://openweathermap.org/find?q=%s' % pure_zip_code)

    def pajacyk(self):

        Core.send_message(self, 'http://pajacyk.pl')
        Core.send_message(self, 'Kliknij proszę w brzuszek!')

    def close(self):

        Core.send_message(self, 'Zakańczam pracę, żegnaj!')
        time.sleep(3)
        if True:
            quit()

# Start main part of script


c = Core()
print('Wybrana strona to %s' % c.url)

c.read_db()
db_positions = len(c.response_db)

print('Wczytałem listę odpowiedzi... %s odpowiedzi' % db_positions)
print('Loguje się do serwisu %s używając loginu %s' % (c.url , c.user_login))
print('Otwieram stronę')

c.open_site()

print('Zamykam monit dotyczący ciasteczek')

c.close_cookie_monit()

print('Loguję się do serwisu')

c.login_site()

print('Wybieram parntera do konwersacji: %s' % c.partner_id)

c.find_partner()

time.sleep(5)

print('Witam się')

hello = ['Siema', 'Witaj', 'Elo', 'Dzień Dobry', 'Hej', 'Dobry', 'Cześć', 'Hi!']
c.send_message(random.choice(hello))
c.send_message('Jestem botem. Możesz coś do mnie napisać, lub wydać mi polecenie.')
c.send_message('Lista dostępnych poleceń:\n /weather <kod pocztowy> (np. /weather 61-001) \n /pajacyk \n /close')
c.send_message('Oczekuję na dalszą reakcję...')

print('Nasłuchuję i rozmawiam...')

old_messages = []  # List with responded messages
commands = {'weather': c.weather, 'pajacyk': c.pajacyk, 'close': c.close}

while True:

    c.read_messages()

    if len(c.messages) > 0:

        """ Response only to messages which are not in oldMessagesList -> take messages from c.messagesList
        (filled in each i-iteration) which are not in oldMessagesList and store it in newMessagesList """

        new_messages = [message for message in c.messages if message not in old_messages]
        print('Na %s wiadomości muszę odpisać' % len(new_messages))
        print(new_messages)
        for message in new_messages:

            # Search for command in message
            if any(command in message for command in commands):

                received_command = ''.join(re.findall('[a-zA-Z]+', message))
                command_to_run = commands[received_command]
                command_to_run()
                old_messages.append(message)

            # Search in database.txt for specified key(string) in incoming message, to send a response to this message
            elif any(key in message for key in c.response_db):

                for key in c.response_db:

                    if key in message:
                        response = c.response_db[key]
                        c.send_message(response)
                        old_messages.append(message)

                    # Do nothing
                    else:
                        pass

            # If message was searched for key(string) and command, and nothing was found:
            else:

                c.send_message('Odpisuję, nie mam tego w database.txt')
                old_messages.append(message)
                print('Odpisane')
                print(old_messages)

    else:
        pass

    # Delete incoming message list; for next loop (next i+1 iteration)
    del c.messages[:]
    print('Ilość wiadomości na które odpisałem od uruchomienia: %s' % len(old_messages))
    time.sleep(5)
