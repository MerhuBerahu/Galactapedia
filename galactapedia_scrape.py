#!/usr/bin/env python

"""
=====================================
Star Citizen Galactapedia Web Scraper
=====================================
Usage: %prog
:Author: MerhuBerahu, https://github.com/MerhuBerahu
:Date: 20/08/2020

"""

import requests
import lxml
import csv
from bs4 import BeautifulSoup
 
url = "https://www.robertsspaceindustries.com/galactapedia"
 
html_doc = requests.get(url)
html_doc.raise_for_status()
 
#print(html_doc)
soup = BeautifulSoup(html_doc.content, 'html.parser')
 
links = []
links2 = []
links3 = []
 
# find all links in parsed data and create a list (links) of url links
for link in soup.find_all('a'): 
    links.append(f"https://robertsspaceindustries.com{link.get('href')}")
 
# find all url links in parsed data and create a list 
for link in links[1:]:
    r = requests.get(link)
    soup = BeautifulSoup(r.text, 'lxml')
    urls = soup.find_all('a')
    for url in urls:
        links2.append(f"https://robertsspaceindustries.com{url.get('href')}")

# get rid of links that dont lead to articles by checking if 'article' is present
# in the URL, if so add link to links3
for match in links2:
    if "article" in match:
        links3.append(match)

# trying to get rid of random hanger on links not weeded out by above
for i in links3: 
    if len(i) < 35:
        links3.pop(i)
    

# checking links by outputting to a text file 
print(links3)
file1 = open("MyFile.txt","a")
for i in links3:
    file1.write(i+"\n") 
file1.close() 
        

# open a CSV to write out scraped data to
f = csv.writer(open('galactapedia.csv', 'w', encoding='utf-8'))
f.writerow(['Name', 'Content'])

for i in links3[:-1]:
    try:
        html_doc = requests.get(i)
        soup = BeautifulSoup(html_doc.text, 'lxml')
    except:
        print("Couldnt Request")
    try:
        title = soup.find("strong", class_="c-title c-title--x-large").get_text()
    except:
        print(f"{i} - Error on title")
    try:
        content = soup.find("div", class_="c-markdown-content").get_text()
    except:
        print(f"{i} - Error on Content")
    f.writerow([title,content,i])
    
    #print(i)
    #print(title)
    #print(content) 