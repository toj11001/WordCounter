#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from urllib.request import urlopen
Url = "https://www.oldbaileyonline.org/browse.jsp?id=t17800628-33&div=t17800628-33"

# read in link
InputUrl = urlopen(Url)
InputText = InputUrl.read()

print (InputText)