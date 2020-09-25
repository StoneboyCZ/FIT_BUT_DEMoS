# http://docs.python-requests.org/en/master/user/quickstart/#cookies
# http://docs.python-requests.org/en/master/user/install/#install
# http://actapublica.eu/brno/77/cut/77-004-1-1.png

# prehled vsech archivu, ze kterych se bude stahovat
# https://digi.ceskearchivy.cz/DA?lang=cs&
# xml generation: https://docs.python.org/3/library/xml.etree.elementtree.html#module-xml.etree.ElementTree

import requests 
import random
import time
import re
import os
import json
import datetime

from requests.adapters import HTTPAdapter

cookies = {
    'PHPSESSID':'bi57v1rtvc1gjdpi7d2659qe57',
}

proxies = {
    "http": "[2001:67c:1220:809::93e5:90e]:3128"  
}

# creates a random number
random.seed() 

# create a session object
s = requests.Session()
s.mount('http://actapublica.eu', HTTPAdapter(max_retries=20))


# first page of the archive
url = 'http://actapublica.eu/matriky/brno/?pg=1'
print(url)

# download the webpage 
r = s.get(url,cookies=cookies, proxies=proxies)    
content = r.text

# how many pages do we need to process? Two matches, same number
matches = re.findall(r'Přejít na stranu číslo [^>]*> z celkem (\d*)',content)
numOfPages = matches[0]

if not os.path.isdir('html'):
    os.mkdir('html')

if not os.path.isdir('json'):
    os.mkdir('json')

for pn in range(1,int(numOfPages)+1,1):
    if pn != 1: # first page doesnt have to be downloaded again
        url = 'http://actapublica.eu/matriky/brno/?pg='+str(pn)
        print(url)
        time.sleep(1)
        r = s.get(url,cookies=cookies, proxies=proxies)
        while (r.status_code != requests.codes.ok):
            r = s.get(url,cookies=cookies, proxies=proxies)  
            time.sleep(1)      
        content = r.text 

    # matchesAdress[0] actapublica.eu
    # matchesAdress[1] matriky
    # matchesAdress[2] brno
    # matchesAdress[3] detail
    # matchesAdress[4] id
    # matchesAdress[5] signatura
    matchesAdress = re.findall(r'<td class="row1"><a href="http://([^/]*)/([^/]*)/([^/]*)/([^/]*)/([^/]*)." title="([^"]*)',content)
    for m in matchesAdress:
            signatura = m[5]
            i = m[4]
            fn = './html/'+signatura+'.html'
            if os.path.isfile(fn): 
                continue
            else: 
                with open(fn,'w',encoding='utf-8') as f:
                    url = 'http://actapublica.eu/matriky/brno/detail/'+i+'/'
                    print(url)
                    time.sleep(2)
                    r = s.get(url,cookies=cookies, proxies=proxies)   
                    while r.status_code != requests.codes.ok:
                        r = s.get(url,cookies=cookies, proxies=proxies)
                        print(f'{r.status_code}')
                        time.sleep(2)
                    f.write(r.text)

    # images
    matchesAdress = re.findall(r'<td class="row1"><a href=.*?title="([^"]*)".*?row1">([^<]*)',content,re.DOTALL)
    #print(matchesAdress)
    for m in matchesAdress:
        signatura = m[0]
        numberOfImages = m[2]
        fn = './json/'+signatura+'.json'
        with open(fn, 'w', encoding='utf-8') as f:
            matrika = {}
            matrika['signatura'] = signatura
            matrika['numberOfImages'] = numberOfImages
            json.dump(matrika,f,ensure_ascii=False)


with open('info.json','w',encoding='utf-8') as f:
    info = {}
    info['downloaded'] = str(datetime.datetime.now())
    json.dump(info,f,ensure_ascii=False)

