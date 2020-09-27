# http://docs.python-requests.org/en/master/user/quickstart/#cookies
# http://docs.python-requests.org/en/master/user/install/#install
# http://actapublica.eu/brno/77/cut/77-004-1-1.png

# prehled vsech archivu, ze kterych se bude stahovat
# https://digi.ceskearchivy.cz/DA?lang=cs&
# xml generation: https://docs.python.org/3/library/xml.etree.elementtree.html#module-xml.etree.ElementTree

import time
import re
import os
import json
import requests
import pyproj


def loadJSON(fn):
    with open(fn, 'r', encoding='utf-8') as f:
        data = json.load(f)  

        return data 

def findInRUIAN(m,data):
    for d in data['data']:
        #print(f"{d}:{data['data'][d]}")
        if data['data'][d]['jmeno'] == m:
            return d
    
    return None 

def downloadFromRUIAN(i,o):
    if o: # jedna se o obec
        url = 'https://vdp.cuzk.cz/vdp/ruian/obce/'+str(i)
        r = requests.get(url).text
        return r
    else: # jedna se o cast obce
        url = 'https://vdp.cuzk.cz/vdp/ruian/castiobce/'+str(i)
        r = requests.get(url).text
        return r


dn = './html/'

sjtsk = pyproj.Proj("+init=epsg:5514")
wgs = pyproj.Proj("+init=epsg:4326")
obce = loadJSON('obce.json')
castiObci = loadJSON('castiObce.json')

data = {}
data['zdroj'] = 'actapublica'
data['pocet'] = 0
data['matriky'] = []



for fn in os.listdir(dn):
    print(dn+fn)
    
    with open(dn+fn, 'r', encoding='utf-8') as f:
        content = f.read()

        matrika = {}

        data['pocet'] = data['pocet'] + 1

        matches = re.findall(r'<h3>([^<]*)',content)
        matrika['id'] = matches[0]
        
        matches = re.findall(r'Původce[^(]*[^>]*>([^<]*)',content)
        matrika['typ'] = matches[0]

        matches = re.findall(r'Okres[^>]*>([^<]*)',content)
        matrika['okres'] = matches[0]

        ## municipality (obec)
        """
        municipalities = {}
        matches = re.findall(r'Obce[^>]*>[^>]*>[^>]*>([^<]*)',content)
        # split by delimiter
        split = matches[0].split(',')

        for m in split:
            m = m.strip()
            municipalities[m] = {}
        """
        # languages (jazyky)
        matrika['jazyky'] = []
        matches = re.findall(r'Jazyk[^>]*>([^&]*|[^<]*)',content)
        # pre-processing
        for lang in matches:
            # split the languages?
            splitList = lang.split('.')
            if len(splitList) > 1: # more languages 
                splitList = list(filter(None, splitList))

                for sp in splitList:
                    if sp == 'čes':                    
                        matrika['jazyky'].append('čeština')
                    elif sp == 'něm':
                        matrika['jazyky'].append('němčina')
                    elif sp == 'lat':
                        matrika['jazyky'].append('latina')
            else: # one language
                matrika['jazyky'].append(str(lang))

        # origin (puvodce)
        matches = re.findall(r'Původce[^>(]*>([^>(]*)',content)
        matrika['puvodce'] = str(matches[0]).strip()

        # municipality (obec)
        matrika['obce'] = {}
        matches = re.findall(r'Obce[^>]*>[^>]*>[^>]*>([^<]*)',content)

        # split by delimiter
        split = matches[0].split(',')
        #print(split)

        for m in split:
            m = m.strip()
            matrika['obce'][m] = {}

            # find in ruian
            obec = True
            i = findInRUIAN(m,obce)
            if i == None: # obec nenalezena, zkousime casti
                i = findInRUIAN(m,castiObci)
                obec = False
            
            matrika['obce'][m]['id'] = i

            # download additional information from RUIAN
            if i != None: 
                ruian = downloadFromRUIAN(i,obec)
                #print(m)    
                print(f'{i} {obec}')
                if 'nalezena' not in ruian:
                    c = re.findall(r'Definiční bod Y: ([^ ]*) X: ([^<]*)',ruian)[0]
                    

                    if len(c) != 0:
                        xx = c[1].replace(',','.')
                        yy = c[0].replace(',','.')
                        xx = '-'+xx
                        yy = '-'+yy
                        #print(xx)
                        cc = pyproj.transform(sjtsk, wgs, float(yy), float(xx))
                        matrika['obce'][m]['souradnice'] = {}
                        matrika['obce'][m]['souradnice']['lat'] = cc[1]
                        matrika['obce'][m]['souradnice']['lon'] = cc[0]
                    

            #print(pyproj.transform(sjtsk, wgs, float(c(1), float(c(0))))
            #print(c)


        # \<td\>(\d*)...(\d*)
        # content (obsah kroniky)
        # pole, ktere obsahuje typy
        typesListNames = ['Narození','Oddaní','Zemřelí','INDEX Narozených','INDEX Oddaných','INDEX Zemřelých']
        matrika['obsah'] = {}
        matches = re.findall(r'\<td\>(\d*)...(\d*)',content) # all ranges

        #print(matches)

        for match,typeName in zip(matches,typesListNames):
            if match[0] and match[1]:
                
                #print(typeName)
                #print(match)
                matrika['obsah']['typ'] = typeName
                matrika['obsah']['rozsah'] = {}
                matrika['obsah']['rozsah']['od'] = match[0]
                matrika['obsah']['rozsah']['do'] = match[1]        

        data['matriky'].append(matrika) 
        


with open ('actapublica.json','w',encoding='utf-8') as f:
    json.dump(data, f, indent=4,ensure_ascii=False)
