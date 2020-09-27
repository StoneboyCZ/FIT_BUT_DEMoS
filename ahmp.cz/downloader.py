# http://docs.python-requests.org/en/master/user/quickstart/#cookies
# http://docs.python-requests.org/en/master/user/install/#install
# http://images.archives.cz/mrimage/matriky/proxy/cz/archives/CZ-217000010/NAD-165/dao/images/0345/8b1ef2b1-eba4-4b55-805d-f79d56afada0.jpg
# http://digi.archives.cz/da/Zoomify.action?entityRef=%28%5En%29%28%28%28localArchiv%2C%5En%2Chot_%29%28unidata%29%29%28338508%29%29&scanIndex=0

# I-N_I-Z_I-O_inv_c_124a_sig_Op_VII_13_1789-1799_Katerinky_025.jpg

import requests 
import re
import os
import html
import datetime
import json

def getNextPage(s,content):
    nextPageMatches = re.findall(r'<div class=\"pageIco\">[^<]*<a href=\"([^\"]*)\"><i class=\"icon-forward3',content)
    #print(nextPageMatches)
    #print('http://digi.archives.cz'+html.unescape(nextPageMatches[0]))
    r = s.get('http://katalog.ahmp.cz'+html.unescape(nextPageMatches[0]),cookies=cookies)    
    print(r.status_code)
    content = r.text
    return content

def getPage(s,url):
    r = s.get(url,cookies=cookies)  
    print(r.status_code)
    content = r.text

    return content


from requests.adapters import HTTPAdapter
cookies = dict(
    JSESSIONID='0AE4D5C9C02487121F22C8B2DF3A7BDC'
)

# creates a random number
#random.seed() 

s = requests.Session()


# create a session object
s.mount('http://katalog.ahmp.cz', HTTPAdapter(max_retries=20))

# url to get -- TODO: first parameter of the script
lastDownloadedPage = 0

url = 'http://katalog.ahmp.cz/pragapublica/VysledekBean.action?show=&_sourcePage=9fjqriTgqw888813s2IsQZJKFaPrh8264Ej9H8jdZdEpRjFcQZ8wXm74BO18vnlv-y0KU8UGNv3vL6rrhq3OJHUWlfDadAppsm4r_N2IO2E%3D&row'+str(lastDownloadedPage)

# download the webpage 
content = getPage(s,url)


# number of entries
#matches = re.findall(r'Celkem[^:]*:[^\d]*([^<]*)',content)
#print(matches[0].strip())
#numberOfEntries = int(matches[0].strip().replace(' ',''))
numberOfEntries = 2812


dn = 'html'
if not os.path.isdir(dn):
    os.mkdir('./'+dn)

files = [f for f in os.listdir(dn) if os.path.isfile(os.path.join(dn,f))]

if not len(files) == numberOfEntries: # not all HTMLs are downloaded
    for n in range(1,numberOfEntries+1,1):
        fn = './'+dn+f'/{n:05d}.html'

        if os.path.isfile(fn): # skip 
            print(f'Skipping: {fn}')
            lastDownloadedPage = n
            #content = getNextPage(s,content)
        else: # new file
            print(fn)
            with open(fn,'w',encoding="utf-8") as f:
                if lastDownloadedPage != 0:
                    url = 'http://katalog.ahmp.cz/pragapublica/VysledekBean.action?show=&_sourcePage=9fjqriTgqw888813s2IsQZJKFaPrh8264Ej9H8jdZdEpRjFcQZ8wXm74BO18vnlv-y0KU8UGNv3vL6rrhq3OJHUWlfDadAppsm4r_N2IO2E%3D&row'+str(lastDownloadedPage)
                    content = getPage(s,url)
                    lastDownloadedPage = 0
            
                #content = getNextPage(s,content)
                snimky = re.findall(r'<div class="oneThumbBloc imageArea">\s+<a href="([^"]*)"',content)

                if len(snimky) != 0:
                    fn_images = './'+dn+'/images/'+f'{n:05d}_images.html'
                    r = s.get('http://katalog.ahmp.cz'+html.unescape(snimky[0]),cookies=cookies)
                    content_images = r.text

                    with open(fn_images,'w',encoding="utf-8") as fi:
                        fi.write(content_images)


                f.write(content)
                #time.sleep(2)
                content = getNextPage(s,content)

                

with open('info.json','w',encoding='utf-8') as f:
    info = {}
    info['downloaded'] = str(datetime.datetime.now())
    json.dump(info,f,ensure_ascii=False)