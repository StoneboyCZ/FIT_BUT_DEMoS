import requests 
import os

def getNextPage(s,url):
    r = s.get(url,cookies=cookies)    
    content = r.text
    return content


from requests.adapters import HTTPAdapter
cookies = dict(
    JSESSIONID='AB4202898707BB5C940DC829356E0EB1'
)

s = requests.Session()

# create a session object
s.mount('http://ebadatelna.soapraha.cz', HTTPAdapter(max_retries=20))

# base url
base = 'http://ebadatelna.soapraha.cz'

# url to get -- TODO: first parameter of the script
url = base+'/pages/SearchMatrikaPage?1'

# number of pages to be downloaded
numberOfPages = 107

dn = 'html'

if not os.path.isdir(dn):
    os.mkdir('./'+dn)

for pn in range(1,numberOfPages+1,1): 
    if pn != 1:
        input("Switch the page in the browser, then press ENTER")

    print(f'Current page: {pn}')
    fn = './'+dn+f'/{pn:03d}.html'
    content = getNextPage(s,url)
    with open(fn,'w',encoding="utf-8") as f:
        f.write(content)            
