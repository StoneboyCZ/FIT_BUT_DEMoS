# http://docs.python-requests.org/en/master/user/quickstart/#cookies
# http://docs.python-requests.org/en/master/user/install/#install
# http://actapublica.eu/brno/77/cut/77-004-1-1.png

# prehled vsech archivu, ze kterych se bude stahovat
# https://digi.ceskearchivy.cz/DA?lang=cs&
# xml generation: https://docs.python.org/3/library/xml.etree.elementtree.html#module-xml.etree.ElementTree

import datetime
from json import load
import re
import os
import json


def loadJSON(fn):
    with open(fn, 'r', encoding='utf-8') as f:
        data = json.load(f)  

        return data 

def findInRUIAN(m,data):
    for d in data:
        #print(f"{d}:{data['data'][d]}")
        if d['nazev'] == m:
            return d
    
    return None 

dn = './html/'

obce = loadJSON('ruian/obce.json')
castiObci = loadJSON('ruian/castiObci.json')

data = {}
data['zdroj'] = 'actapublica'
data['vytvoreno'] = str(datetime.datetime.now())
data['stazeno'] = loadJSON('info.json')['downloaded']
data['pocet'] = 0
data['snimky_zaklad'] = 'http://actapublica.eu/brno/'
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

        # parse additional data from json
        json_info = loadJSON('json/'+matrika['id']+'.json')
        matrika['snimky'] = []
        #matrika['snimky']['pocet'] = int(json_info['numberOfImages'])

        for i in range(1, int(json_info['numberOfImages'])+1,1):
            index='{num:03d}'.format(num=i)
            snimek = {}
            snimek['url'] = matrika['id']+'/cut/'+matrika['id']+'-'+index+'-1-1.png'
            matrika['snimky'].append(snimek)
            #print(data['snimky_zaklad']+sn)

        data['matriky'].append(matrika) 
        


with open ('actapublica.json','w',encoding='utf-8') as f:
    json.dump(data, f, indent=4,ensure_ascii=False)
