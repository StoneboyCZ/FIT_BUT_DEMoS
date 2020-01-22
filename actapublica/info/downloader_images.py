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

cookies = {
    'PHPSESSID':'asfdde6g564kdscfb2a85ul771',
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

    # matchesAdress[0] id
    # matchesAdress[1] signatura
    # matchesAdress[2] pocet stranek
    matchesAdress = re.findall(r'<td class="row1"><a href="http://actapublica\.eu/matriky/brno/detail/([^/]*)/" title="([^"]*)".*?row2"></td>.*?row1">([^<]*)',content,re.DOTALL)
    for m in matchesAdress:
            signatura = m[1]
            fn = './html_images/'+signatura+'.html'
            if os.path.isfile(fn) or int(m[2]) == 0: 
                continue
            else: 
                with open(fn,'w',encoding='utf-8') as f:
                    url = 'http://actapublica.eu/matriky/brno/prohlizec/'+m[0]+'/'
                    print(url)
                    time.sleep(2)
                    r = s.get(url,cookies=cookies, proxies=proxies)   
                    f.write(r.text)



