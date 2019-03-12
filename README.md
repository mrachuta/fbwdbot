## Project name
FBWDBot - Facebook WebDriver Bot
Simple bot created only for training, without any special purposes.
## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)
* [Using](#using)
* [Thanks](#thanks)

## General info
Project was started at the beggining of 2018 as author's first steps in Python.
The main goal was to chceck, how Selenium WebDriver works, and how possibilities has this suite.
Primary version was very primitive, the final version is a little bit enhanced.

## Technologies
Code was written as a Python 3 code.

Code was tested on following platform:
* Python 3.7.1 (x64), 
* Firefox 63.0.1 (x64), 
* Gecko Driver 0.23.0 (Win-32),
* Widows 8.1 (x64)

Used libraries:
* Package and version
* beautifulsoup4 4.6.3
* bs4            0.0.1
* certifi        2018.10.15
* chardet        3.0.4
* idna           2.7
* pip            18.1
* requests       2.20.0
* selenium       3.14.1
* setuptools     40.5.0
* urllib3        1.24
* wheel          0.32.2

## Setup

Before first run, to exclude problems with proper path to Firefox-binary and Gecko Driver-binary, please see the source code (bot.py, lines 44 and 45).  
File database.txt contains responses to some pharses in a form:
```
received_pharse;response
```
for example:
```
how are you?;Thank's I am fine. And you?
```
received_pharse should be wrote lowercase letters, see examples inside file.  
Is recommended to edit file via Notepad++ for example, to keep encoding and newline characters (all next added pair, should be in new line).    

Nothing (of course if all packages are installed) more is required.

## Using

1. To get Facebook user id (partner for conversation with bot), run command below and follow steps on screen. You will be able to print partner id or save them in configuration file.:
```
python getpartnerid.py 
```
2. Run main bot code:
```
python bot.py
```
3. Insert username and password for bot account (accound must be previously created, manually)
4. If you chosed to save partner id to file, partner will be automatically selected. Otherwise you must write partner id manually.
5. Bot has four main functions:
* weather (use /weather <zip-code>, for example /weather 00-123 for link to site with weather for your localization)
* pajacyk (use /pajacyk for link to Polish Hummanitary Action)
* close (use /close for shutdown bot)
* conversation (information about responses - see [Setup](#setup))

## Thanks

I am very thankful for my girlfriend for test with her private account - of course as partner for conversation with bot.
