#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# importing libraries
from urllib.request import urlopen
from html.parser import HTMLParser
from bs4 import BeautifulSoup as bs
import re

import StopWords
# ================================
# get stopwords from list
stopwords = StopWords.stopwordsList() 

Url = "https://www.oldbaileyonline.org/browse.jsp?id=t17800628-33&div=t17800628-33"

# read in link
InputUrl = urlopen(Url)
InputText = InputUrl.read()

# use BeautifulSoup to strip HTML
soup = bs(InputText, "html.parser")
text = soup.get_text().lower() # get text and convert to lower case

# remove stopwords with regex
p  = re.compile('\\b'+'\\b|\\b'.join(stopwords)+'\\b') 
cleanedText = p.sub('',text)
# remoe nonAlpha chracters and return a list with words
ListOnlyAlpha = re.compile('[a-zA-Z]+').findall(cleanedText)

# create list with word freq
wordFreqList = []
for istr in ListOnlyAlpha:
    wordFreqList.append([istr, ListOnlyAlpha.count(istr)])

# for istr in wordFreqList:
    # if (istr[1] > 1):
        # wordFreqList.remove(istr)

# wordFreq.sort()
# print (wordFreq)

# ========================================================
# create dictionary with word freq
wordFreqDict = {istr[0]:istr[1] for istr in wordFreqList}
# sort dictionary by value
wordFreqDict = sorted(wordFreqDict.items(), key=lambda t:t[1], reverse=True)
for pair in wordFreqDict:
    print (pair[0],pair[1])