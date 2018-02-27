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
            
# ================================
# get stopwords from list
stopwords = StopWords.stopwordsList() 
MemBeforeReadUrl = psutil.Process(os.getpid()).memory_info()
total = time.time() # start total time counter
Url = "https://www.oldbaileyonline.org/browse.jsp?id=t17800628-33&div=t17800628-33"

# read in link
InputUrl = urlopen(Url)
InputText = InputUrl.read()

InputText = InputText[4590:24300] # shrink string down to the interesting text

# use BeautifulSoup to strip HTML tags
soup = bs(InputText, "html.parser")
text = soup.get_text().lower() # get text and convert to lower case
# ----------------
# alternative solution to using the above text shrinking but first one is faster
# soup = soup.find(id="main2")
# text = soup.get_text()
# ----------------

# remove stopwords with regex
t0 = time.time()
p  = re.compile('\\b'+'\\b|\\b'.join(stopwords)+'\\b') 
cleanedText = p.sub('',text)
# remove nonAlpha chracters and return a list with words
ListOnlyAlpha = re.compile('[a-zA-Z]+').findall(cleanedText)
# --------------------------------------------------------
# create list with word freq
MemBeforeWordFreqList = psutil.Process(os.getpid()).memory_info()
wordFreqList = []
for istr in ListOnlyAlpha:
    wordFreqList.append([istr, ListOnlyAlpha.count(istr)])
clocktime = time.time() - t0
print ("Cleaning text processing time: %f\n" % (clocktime))
# --------------
MemBeforeListSort = psutil.Process(os.getpid()).memory_info()
t0 = time.time()
# sort list by wordCount
sortedList = sorted(wordFreqList, key=lambda t:t[1], reverse=True)
# print (sortedList)
sortedList = remove_duplicates(sortedList) # remove duplicate words in list
clocktime = time.time() - t0
print ("List sorting processing time: %f\n" % (clocktime))
# print sorted list
for pair in sortedList[:20]:
    print (pair[0],pair[1])

# ========================================================
# create dictionary with word freq
MemBeforeDictSort = psutil.Process(os.getpid()).memory_info()
t0 = time.time()
# copy words and count from freqList to a dictionary
wordFreqDict = {istr[0]:istr[1] for istr in wordFreqList}
# sort dictionary by word count
wordFreqDict = sorted(wordFreqDict.items(), key=lambda t:t[1], reverse=True)
clocktime = time.time() - t0
print ("\nDict processing time: %f\n" %clocktime)
for pair in wordFreqDict[:20]:
    print (pair[0],pair[1])

clocktime = time.time() -total
print ("\nTotal Program Time: %f\n" %clocktime)
# Memory Usage
MemTotal = psutil.Process(os.getpid()).memory_info()
print("Memory Usage before read URL: ", MemBeforeReadUrl.rss/1000, " Kb")
print("Memory Usage BeforeWordFreqList: ", MemBeforeWordFreqList.rss/1000, " Kb")
print("Memory Usage BeforeListSort: ", MemBeforeListSort.rss/1000, " Kb")
print("Memory Usage BeforeDictSort: ", MemBeforeDictSort.rss/1000, " Kb")
print("Memory Usage Total: ", MemTotal.rss/1000, " Kb")