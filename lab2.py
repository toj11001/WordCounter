#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# importing libraries
from urllib.request import urlopen
from html.parser import HTMLParser
from bs4 import BeautifulSoup as bs
import re, time, psutil, os

import StopWords
# ================================
# Functions
def remove_duplicates(in_list):
    out_list =[]
    for val in in_list:
        if not val in out_list:
            out_list.append(val)
    return out_list

# -------------------------------- =
def extract_text(stringSoup, Container):
    formTag = stringSoup.find("form")
    # access main2 and get the links
    for link in formTag.find_all('a'):
        string = link.get('href').replace("\n","")
        newTab = urlopen("https://www.oldbaileyonline.org/" + string)
        Container += str(bs(newTab.read(), "html.parser").find(id="main2").get_text())
    return Container

# ================================
# get stopwords from list
stopwords = StopWords.stopwordsList()
# string to store the text
textContainer = ""

# MemBeforeReadUrl = psutil.Process(os.getpid()).memory_info()
# total = time.time() # start total time counter
Url = "https://www.oldbaileyonline.org/search.jsp?form=searchHomePage&_divs_fulltext=Smith&kwparse=and&_persNames_surname=&_persNames_given=&_persNames_alias=&_offences_offenceCategory_offenceSubcategory=&_verdicts_verdictCategory_verdictSubcategory=&_punishments_punishmentCategory_punishmentSubcategory=&_divs_div0Type_div1Type=&fromMonth=07&fromYear=1749&toMonth=01&toYear=1913&ref=&submit.x=0&submit.y=0&submit=Search"

# read in link
InputUrl = urlopen(Url)
InputText = InputUrl.read()

print("Started reading URL .....")
for i in range(1,2):
    print (i)
    # use BeautifulSoup to strip HTML tags
    soup = bs(InputText, "html.parser").find(id="main2")
    textContainer = extract_text(soup, textContainer) #.encode('utf-8')
    # get nextlink page
    nextLink = soup.find("li",{"class" : "last"}).find('a').get('href')
    nextPage = urlopen("https://www.oldbaileyonline.org/"+nextLink)
    InputText = nextPage.read()

print (textContainer)
textfile = open("Output.txt", "w")
textfile.write(textContainer()
