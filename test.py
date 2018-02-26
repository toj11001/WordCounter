#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# importing libraries
from urllib.request import urlopen
from html.parser import HTMLParser
from bs4 import BeautifulSoup as bs
import re, time

import StopWords
# ================================
# Functions
def remove_duplicates(in_list):
    out_list =[]
    for val in in_list:
        if not val in out_list:
            out_list.append(val)
    return out_list
            
# ================================
# get stopwords from list
stopwords = StopWords.stopwordsList() 
total = time.time()
Url = "https://www.oldbaileyonline.org/browse.jsp?id=t17800628-33&div=t17800628-33"

# read in link
InputUrl = urlopen(Url)
InputText = InputUrl.read()

# use BeautifulSoup to strip HTML tags
soup = bs(InputText, "html.parser")
text = soup.get_text().lower() # get text and convert to lower case

# remove stopwords with regex
t0 = time.time()
p  = re.compile('\\b'+'\\b|\\b'.join(stopwords)+'\\b') 
cleanedText = p.sub('',text)
# remove nonAlpha chracters and return a list with words
ListOnlyAlpha = re.compile('[a-zA-Z]+').findall(cleanedText)
# create list with word freq
wordFreqList = []
for istr in ListOnlyAlpha:
    wordFreqList.append([istr, ListOnlyAlpha.count(istr)])
clocktime = time.time() - t0
print ("Cleaning text: %f\n" % (clocktime))

t0 = time.time()
sortedList = sorted(wordFreqList, key=lambda t:t[1], reverse=True)
# print (sortedList)
sortedList = remove_duplicates(sortedList)
clocktime = time.time() - t0
print ("List: %f\n" % (clocktime))
# for pair in sortedList:
#     print (pair[0],pair[1])

# ========================================================
# create dictionary with word freq
t0 = time.time()
wordFreqDict = {istr[0]:istr[1] for istr in wordFreqList}
# sort dictionary by value
wordFreqDict = sorted(wordFreqDict.items(), key=lambda t:t[1], reverse=True)
clocktime = time.time() - t0
print ("\n\nDict: %f\n" %clocktime)
for pair in wordFreqDict:
    print (pair[0],pair[1])

clocktime = time.time() -total
print ("\nTotal: %f\n" %clocktime)