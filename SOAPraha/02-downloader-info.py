import requests 
import re
import os
import json
import datetime
"""
from requests.adapters import HTTPAdapter
cookies = dict(
    JSESSIONID='1E8B1A4679E06229C6E4EBFDD27D90E1'
)
"""

#s = requests.Session()

# create a session object
#s.mount('http://ebadatelna.soapraha.cz', HTTPAdapter(max_retries=20))

# base url
base = 'http://ebadatelna.soapraha.cz'

# url to get -- TODO: first parameter of the script
url = base+'/pages/SearchMatrikaPage?1'

# number of pages to be downloaded
dn_html = 'html'
files = [f for f in os.listdir(dn_html) if os.path.isfile(os.path.join(dn_html,f))]
numberOfEntries = len(files)

dn_info = 'html/info'

if not os.path.isdir(dn_info):
    os.mkdir('./'+dn_info)

# for every downloaded html, download the information table
for f in files:
    fn = './'+dn_html+'/'+f

    with open(fn,'r',encoding="utf-8") as fi:
        content = fi.read()

        # get all content links
        links = re.findall(r'onclick="renderRowClasses.*?(?=" href)" href="([^"]*)">',content)

        for link in links:
            url = base+link
            
            # download link
            r = requests.get(url)    
            content = r.text
    
            id = link.split('/')[-1]
            ifn = './'+dn_info+'/'+id+'.html'
            
            with open(ifn,'w',encoding="utf-8") as fii:
                fii.write(content)                

with open('info.json','w',encoding='utf-8') as f:
    info = {}
    info['downloaded'] = str(datetime.datetime.now())
    info['zaklad'] = 'http://ebadatelna.soapraha.cz/'
    json.dump(info,f,ensure_ascii=False)