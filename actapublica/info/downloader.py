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

from requests.adapters import HTTPAdapter

def striplist(l):
    return([x.strip() for x in l])


cookies = {
    'PHPSESSID':'bd96pff2r2d1jordam9a6e24s7',
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

for pn in range(1,int(numOfPages)+1,1):
    if pn != 1: # first page doesnt have to be downloaded again
        url = 'http://actapublica.eu/matriky/brno/?pg='+str(pn)
        print(url)
        time.sleep(1)
        r = s.get(url,cookies=cookies, proxies=proxies)    
        content = r.text 

    # matchesAdress[0] actapublica.eu
    # matchesAdress[1] matriky
    # matchesAdress[2] brno
    # matchesAdress[3] detail
    # matchesAdress[4] id
    # matchesAdress[5] signatura
    matchesAdress = re.findall(r'<td class=\"row1\"><a href=\"http://([^/]*)/([^/]*)/([^/]*)/([^/]*)/([^/]*).\" title=\"([^\"]*)',content)
    for m in matchesAdress:
            signatura = m[5]
            fn = './html/'+signatura+'.html'
            if os.path.isfile(fn): 
                continue
            else: 
                with open(fn,'w',encoding='utf-8') as f:
                    url = 'http://actapublica.eu/matriky/brno/detail/'+m[4]+'/'
                    print(url)
                    time.sleep(2)
                    r = s.get(url,cookies=cookies, proxies=proxies)   
                    f.write(r.text)



