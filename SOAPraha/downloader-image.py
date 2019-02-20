# <a class="manipulationButton" target="_blank" href="../../wicket/resource/org.apache.wicket.Application/Arnostovice_01__002.jpg"><span>&#9660;</span></a>

import requests 
from requests.adapters import HTTPAdapter

cookies = dict(
    JSESSIONID='66DFB9F125E94C5D544896AFB069A3B9'
)

# creates a random number
#random.seed() 

s = requests.Session()

# create a session object
s.mount('http://ebadatelna.soapraha.cz', HTTPAdapter(max_retries=20))


url = 'http://ebadatelna.soapraha.cz/d/3726/2'

r = s.get(url,cookies=cookies)    
content = r.text

with open('img.html','w',encoding="utf-8") as f:
    f.write(content)
