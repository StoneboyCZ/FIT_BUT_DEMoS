# http://docs.python-requests.org/en/master/user/quickstart/#cookies
# http://docs.python-requests.org/en/master/user/install/#install
# http://images.archives.cz/mrimage/matriky/proxy/cz/archives/CZ-217000010/NAD-165/dao/images/0345/8b1ef2b1-eba4-4b55-805d-f79d56afada0.jpg
# http://digi.archives.cz/da/Zoomify.action?entityRef=%28%5En%29%28%28%28localArchiv%2C%5En%2Chot_%29%28unidata%29%29%28338508%29%29&scanIndex=0

# I-N_I-Z_I-O_inv_c_124a_sig_Op_VII_13_1789-1799_Katerinky_025.jpg

# <tr class="propojLok">\s*<[^>]*>([^<]*).*\s*</tr>\s*<tr>\s*.*?(?=va)[^>]*>(.*?)(?=</td)

import random
import time
import re
import os
import math
import html
import json
import pyproj
import requests
from requests.adapters import HTTPAdapter

def loadJSON(fn):
    with open(fn, 'r', encoding='utf-8') as f:
        data = json.load(f)  

        return data 

def findInRUIAN(m,data):
    print(m)
    for d in data['data']:
        #print(f"{d}:{data['data'][d]}")
        
        if data['data'][d]['jmeno'] == m:
            return d
    
    return None 


def downloadFromRUIAN(n,o):
    coords = {}
    r = ''
    if o: # jedna se o obec
        i = findInRUIAN(n,obce)
        #print(i)
        if i != None:
            url = 'https://vdp.cuzk.cz/vdp/ruian/obce/'+str(i)
            r = s.get(url).text
    else: # jedna se o cast obce
        i = findInRUIAN(n,castiObci)
        if i != None:
            url = 'https://vdp.cuzk.cz/vdp/ruian/castiobce/'+str(i)
            r = s.get(url).text

    #print(o)
    #print(r)

    if 'nalezena' not in r and r != '':
        c = re.findall(r'Definiční bod Y: ([^ ]*) X: ([^<]*)',r)[0]

        if len(c) != 0:
            xx = c[1].replace(',','.')
            yy = c[0].replace(',','.')
            xx = '-'+xx
            yy = '-'+yy
            #print(xx)
            cc = pyproj.transform(sjtsk, wgs, float(yy), float(xx))
            coords['lat'] = cc[1]
            coords['lon'] = cc[0]        

    return coords

def getInterval(t):
    od_do = {}
    if re.match(r'\d+-\d+',t) != None:
        sp = t.split('-')
        od_do = {'od':sp[0], 'do':sp[1]} 
    elif re.match(r'\d+',t) != None:
        od_do = {'od':t, 'do':t} 
    
    return od_do 

sjtsk = pyproj.Proj("+init=epsg:5514")
wgs = pyproj.Proj("+init=epsg:4326")
obce = loadJSON('obce.json')
castiObci = loadJSON('castiObce.json')

ruianCache = {}
ruianCache['obce'] = {}
ruianCache['casti_obce'] = {}

s = requests.Session()

# create a session object
s.mount('https://vdp.cuzk.cz/', HTTPAdapter(max_retries=20))


dn = 'html'
files = [f for f in os.listdir(dn) if os.path.isfile(os.path.join(dn,f))]
numberOfEntries = len(files)

print(numberOfEntries)
data = {}
data['zdroj'] = 'opava-zaool'
data['matriky'] = []
 
with open("opava-zaool.json", 'w',encoding="utf-8") as f:
    #f.write("""{
    #"zdroj": "opava",
    #"matriky": [""")

    #for pn in range(1,20):
    for pn in range(1,numberOfEntries+1,1):
        # load a file
        fn = './'+dn+f'/{pn:05d}.html'
        print(fn)
        htmlFile = open(fn, 'r',encoding='utf-8')
        content = htmlFile.read()
        
        book = {}

        # obtain the information from the page
        puvodce = re.findall(r'div class=\"labelFloat\">Původce[^>]*[^<]*[^>]*>([^<]*)',content)
        signatura = re.findall(r'div class=\"labelFloat\">Signatura [^>]*[^<]*[^>]*>([^<]*)',content)
        invCislo = re.findall(r'div class=\"labelFloat\">Inventární [^>]*[^<]*[^>]*>([^<]*)',content)
        typMatriky = re.findall(r'div class=\"labelFloat\">Typ [^>]*[^<]*[^>]*>([^<]*)',content)
        jazyk = re.findall(r'div class=\"labelFloat\">Jazyk:[^>]*[^<]*[^>]*>([^<]*)',content)
        casovyRozsah = re.findall(r'div class=\"labelFloat\">Časový[^>]*[^<]*[^>]*>([^<]*)',content)
        obsahSvazku = re.findall(r'div class=\"labelFloat\">Obsah [^>]*[^<]*[^>]*>([^<]*)',content)
        mistoUlozeni = re.findall(r'div class=\"labelFloat\">Místo [^>]*[^<]*[^>]*>([^<]*)',content) 
        uzemniRozsahSeznam = re.findall(r'div class=\"labelFloat\">Územní [^>]*[^<]*[^>]*>([^<]*)',content)
        #uzemniRozsah = re.findall(r'<tr class="propojLok">\s*<[^>]*>([^<]*).*\s*</tr>\s*<tr>\s*.*?(?=va)[^>]*>(.*?)(?=</td)',content)
        uzemniRozsah = re.findall(r'<tr class="propojLok">.*?<td colspan="3".*?borderLeft">([^<]*).*?lokalita indent">(.*?)</td>',content,re.DOTALL)
        poznamka = re.findall(r'div class="labelFloat">Poznámka:[^>]*[^<]*[^>]*>([^<]*)',content)
        
        book['signatura'] = signatura[0]
        book['typ'] = typMatriky[0]
        book['inv. cislo'] = invCislo[0]
        #print(len(jazyk))
        if len(jazyk) > 0:
            if ',' in jazyk[0] and len(jazyk) != 0:
                book['jazyky'] = jazyk[0].replace(' ', '').split(',')
            else:
                book['jazyky'] = jazyk[0]
        book['puvodce'] = puvodce[0]

        obsah = {}
        if obsahSvazku:
            #print(obsahSvazku) 
            obsahSvazku = obsahSvazku[0].strip().strip().replace('\n','').replace(' • ','•').replace(' - ','-')
            obsahSvazku = re.sub(r'\s\s+','•',obsahSvazku)
            obsahSvazku = obsahSvazku.split('•')
            print(obsahSvazku)
            
            od_do = {}
            i = 0
            l = len(obsahSvazku)
            while i < l:
                t = obsahSvazku[i]
                
                if l > 1 and i != l-1:
                    if t == 'I-N':
                        obsah['INDEX Narozených'] = getInterval(obsahSvazku[i+1])
                    elif t == 'I-Z':
                        obsah['INDEX Zemřelých'] = getInterval(obsahSvazku[i+1])
                    elif t == 'I-O':
                        obsah['INDEX Oddaných'] = getInterval(obsahSvazku[i+1])
                    elif t == 'N':
                        obsah['Narození'] = getInterval(obsahSvazku[i+1])
                    elif t == 'O':
                        obsah['Oddaní'] = getInterval(obsahSvazku[i+1])
                    elif t == 'Z':
                        obsah['Zemřelí'] = getInterval(obsahSvazku[i+1])
                    else:
                        obsah['Poznámka'] = t

                i+=1 

            book['obsah'] = obsah

        uzemniRozsahSeznam = uzemniRozsahSeznam[0].strip()
        #print(uzemniRozsah)
        if ',' in uzemniRozsahSeznam:
            uzemniRozsahSeznam = uzemniRozsahSeznam.split(',')
            uzemniRozsahSeznam = [obec.lstrip() for obec in uzemniRozsahSeznam]

        book['obce_seznam'] = uzemniRozsahSeznam

        book['obce'] = []
        for uzemi in uzemniRozsah:
            obec = {}
            od_do = uzemi[0]
            if '-' in uzemi[0]:
                od_do = od_do.split('-')
                obec['od'] = od_do[0]
                obec['do'] = od_do[1]
            else:
                obec['od'] = od_do
                obec['do'] = od_do

            #print(f"{obec['od-do']}")

            obec['typ'] = []

            umisteni = {}
            misto = uzemi[1].split('; ')
            #print(misto)
            # stat, kraj, okres, obec, cast_obce, samota
            umisteni['stat'] = misto[0]
            umisteni['kraj'] = misto[1]
            umisteni['okres'] = misto[2]
            umisteni['obec'] = misto[3].replace('<b>', '').replace('</b>','')
            umisteni['cast_obce'] = misto[4].replace('<b>', '').replace('</b>','')
            umisteni['samota'] = misto[5]  
            
            if len(misto[4]) > 0:
                obec['typ'] = 'cast_obce'
                if umisteni['cast_obce'] in ruianCache['casti_obce']:
                    print(f"hit cast {umisteni['cast_obce']}")
                    obec['souradnice'] = ruianCache['casti_obce'][umisteni['cast_obce']]
                else:
                    obec['souradnice'] = downloadFromRUIAN(umisteni['cast_obce'],False)
                    ruianCache['casti_obce'][umisteni['cast_obce']] = obec['souradnice']
            elif len(misto[5]) > 0:
                obec['typ'] = 'samota'
            else:
                obec['typ'] = 'obec'  
                if umisteni['obec'] in ruianCache['obce']: 
                    print(f"hit obec  {umisteni['obec']}")
                    obec['souradnice'] = ruianCache['obce'][umisteni['obec']]
                else:
                     obec['souradnice'] = downloadFromRUIAN(umisteni['obec'],True)
                     ruianCache['obce'][umisteni['obec']] = obec['souradnice']

            obec['umisteni'] = umisteni 
            book['obce'].append(obec)

        # snimky
        
        # obsahuje matrika snimky?
        ifn = f'./{dn}/images/json/{pn:05d}_images.json'
        if os.path.exists(ifn):
            imagesFile = open(ifn, 'r',encoding='utf-8')
            book['snimky'] = json.load(imagesFile)
            imagesFile.close()

        #print(len(poznamka))
        if len(poznamka) != 0:
            book['poznamka'] = poznamka[0]

        data['matriky'].append(book)
        #json.dump(book,f,indent=4,ensure_ascii=False)
        #f.write(',')
        htmlFile.close()
    
    json.dump(data,f,indent=4,ensure_ascii=False)
    #f.write(']}')
    

