# http://docs.python-requests.org/en/master/user/quickstart/#cookies
# http://docs.python-requests.org/en/master/user/install/#install
# http://images.archives.cz/mrimage/matriky/proxy/cz/archives/CZ-217000010/NAD-165/dao/images/0345/8b1ef2b1-eba4-4b55-805d-f79d56afada0.jpg
# http://digi.archives.cz/da/Zoomify.action?entityRef=%28%5En%29%28%28%28localArchiv%2C%5En%2Chot_%29%28unidata%29%29%28338508%29%29&scanIndex=0

# I-N_I-Z_I-O_inv_c_124a_sig_Op_VII_13_1789-1799_Katerinky_025.jpg

import requests 
import time
import re
import os
import html
import datetime
import json

page = 'http://vademecum.soalitomerice.cz'

from requests.adapters import HTTPAdapter
cookies = dict(
    JSESSIONID='56885677C07E478263EFAE812B51418E'
)

def getNextPage(s,n):
    url = 'http://vademecum.soalitomerice.cz/vademecum/VysledekBean.action?show=&_sourcePage=7C0Z-jshQvpMMLkbRM-OoOZm_suEKIYiRGBgIvsOKlti6ziH1UlKM96B45WXdLj0HFhxnacstk_pQnCoodICz6H8nggSB3mzvfv3cV6sjsg%3D&pagerCompStateId=PAGER_RESULT&xid=09ddd7cea03b9b8d%3A30bdd2c7%3A1201ea2ef5b%3A-7e0b&entityType=10041&paginatorCompStateId=PAGINATOR_RESULT&rowPg='+str(n)
    r = s.get(url,cookies=cookies)    
    while (r.status_code != requests.codes.ok):
        print(r.status_code)
        r = s.get(url,cookies=cookies)  
        time.sleep(1)          
    
    content = r.text
    return content

s = requests.Session()

# create a session object
s.mount(page, HTTPAdapter(max_retries=20))

# url to get -- TODO: first parameter of the script
url = 'http://vademecum.soalitomerice.cz/vademecum/VysledekBean.action?show=&_sourcePage=Ex5OXJ1ihntoqAKB5ldeJG8pmHFYHdy7BKiBPGAvXoy9Dj5QxwKE8U_ZTgOdDFcdFbvZYSljoMB9hOMTZ7NX3iaBvGMXBq_oFnlJN5ln9yM%3D&pagerCompStateId=PAGER_RESULT&xid=09ddd7cea03b9b8d%3A30bdd2c7%3A1201ea2ef5b%3A-7e0b&entityType=10041&paginatorCompStateId=PAGINATOR_RESULT&rowPg=0'

# download the webpage 
r = s.get(url,cookies=cookies)  
content = r.text

#print(content)

# number of entries
matches = re.findall(r'Celkem[^\d]*([^<]*)',content,re.DOTALL)
numberOfEntries = int(matches[0].strip().replace(' ',''))
print(numberOfEntries) 


dn = 'html'
skip = False

skipIndex = 1
for n in range(1,numberOfEntries,1):
    fn = './'+dn+f'/{n:05d}.html'

    if os.path.isfile(fn): # skip 
        skip = True
        print(f'Skipping: {fn}')
        skipIndex = n
        #content = getNextPage(s,content)
    else: # new file
        print(fn)
        if skip:
            url = 'http://vademecum.soalitomerice.cz/vademecum/VysledekBean.action?show=&_sourcePage=Ex5OXJ1ihntoqAKB5ldeJG8pmHFYHdy7BKiBPGAvXoy9Dj5QxwKE8U_ZTgOdDFcdFbvZYSljoMB9hOMTZ7NX3iaBvGMXBq_oFnlJN5ln9yM%3D&pagerCompStateId=PAGER_RESULT&xid=09ddd7cea03b9b8d%3A30bdd2c7%3A1201ea2ef5b%3A-7e0b&entityType=10041&paginatorCompStateId=PAGINATOR_RESULT&rowPg='+str(skipIndex-1)
            r = s.get(url,cookies=cookies)  
            content = r.text
            skip = False

        with open(fn,'w',encoding="utf-8") as f:
            snimky = re.findall(r'<div class="imageBlock">\s+<a href="([^"]*)"',content)

            if len(snimky) != 0:
                fn_images = './'+dn+f'/images/{n:05d}_images.html'
                #time.sleep(3)
                r = s.get(page+html.unescape(snimky[0]),cookies=cookies)    
                content_images = r.text
                while (r.status_code != requests.codes.ok):
                    print(r.status_code)
                    r = s.get(url,cookies=cookies)  
                    time.sleep(1)
                    content_images = r.text

                with open(fn_images,'w',encoding="utf-8") as fi:
                    fi.write(content_images)

            f.write(content)
            
            content = getNextPage(s,n)

with open('info.json','w',encoding='utf-8') as f:
    info = {}
    info['downloaded'] = str(datetime.datetime.now())
    json.dump(info,f,ensure_ascii=False)