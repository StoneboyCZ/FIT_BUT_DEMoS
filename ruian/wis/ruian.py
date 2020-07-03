#https://wis.fit.vutbr.cz/FIT/db/vyuka/cat/cst_obce.php?submit_view=-1&start=1&limit=1000&form_f4=valid&json=1

import requests
from requests.auth import HTTPBasicAuth
import json
import getpass
import re
import time


def createSession(login):
    s = requests.Session()
    password=getpass.getpass(prompt='Password (WIS FIT): ', stream=None)
    s.auth = HTTPBasicAuth(login, password)
    s.verify = 'FIT.crt'
    return s 

def insertObec(d,obce):

    print(key)


    return obce

s = createSession('iveigend')

# number of pages
numberOfPages = 20

obce = {}
obce['pocet'] = 0
obce['data'] = {}

casti = {}
casti['pocet'] = 0
casti['data'] = {}

#for i in range(0,2,1):
for i in range(0,numberOfPages+1,1):
    url = 'https://wis.fit.vutbr.cz/FIT/db/vyuka/cat/cst_obce.php?submit_view=2&start='+str(i)+'&limit=1000&form_f4=valid&json=1'

    data = s.get(url).json()['data']
    #print(data)
    
    
    for d in data:
        
        if d['cst_obec_status'] not in 'historie':
            key = d['cst_obec_code']
            url = 'https://wis.fit.vutbr.cz/FIT/db/vyuka/cat/cst_obce.php?id='+str(key)
            detail = s.get(url).text
        
            zemeCheck = re.findall(r'<a href="cst_region[^>]*>([^<]*)',detail)[0]

            if 'CZ' not in zemeCheck:
                print(zemeCheck)
                continue
            else:
                # obec
                obce['data'][key] = {}
                obce['data'][key]['region'] = d['cst_region_name']
                obce['data'][key]['jmeno'] = d['cst_obec_name']                
                obce['pocet'] = obce['pocet'] + 1 
                
                # casti obce
                seznamCasti = re.findall(r'<a href="cst_cobce[^=]*=([^"]*)[^>]>([^<]*)',detail)
                if len(seznamCasti) > 0:
                    for c in seznamCasti:
                        print(c)
                        
                        key_cast = c[0]
                        casti['data'][key_cast] = {}
                        casti['data'][key_cast]['jmeno'] = c[1]
                        casti['data'][key_cast]['id_obce'] = key
                        casti['pocet'] = casti['pocet'] + 1


                #time.sleep(1)
    

with open('obce.json','w',encoding='utf-8') as f:
    json.dump(obce,f,ensure_ascii=False,indent=4)


with open('castiObce.json','w',encoding='utf-8') as f:
    json.dump(casti,f,ensure_ascii=False,indent=4)

    


