# http://images.ahmp.cz/mrimage/ahmp/proxy/cz/archives/CZ-321100010/NAD-156/dao/images/0060/8f8491b495f7b49d4b69e2c4ecef862f.jpg

import re
import os
import datetime

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


dn = 'html'
files = [f for f in os.listdir(dn) if os.path.isfile(os.path.join(dn,f))]
numberOfEntries = len(files)

print(numberOfEntries)
data = {}
data['zdroj'] = 'abmp'
data['vytvoreno'] = str(datetime.datetime.now())
data['stazeno'] = loadJSON('info.json')['downloaded']
data['snimky_zaklad'] = 'http://images.ahmp.cz/mrimage/ahmp/proxy/cz/archives/'
data['pocet'] = 0
data['matriky'] = []
 
with open("abmp.json", 'w',encoding="utf-8") as f:
    for pn in range(1,numberOfEntries,1):
        # load a file
        fn = './'+dn+f'/{pn:05d}.html'
        print(fn)
        htmlFile = open(fn, 'r',encoding='utf-8')
        content = htmlFile.read()
        
        data['pocet'] += 1

        book = {}

        # obtain the information from the page
        book['puvodce'] = re.findall(r'span class="tabularLabel">\s+Fara/úřad:\s+</span>\s+<span class="tabularValue">([^<]*)',content)[0].strip()
        book['signatura'] = re.findall(r'span class="tabularLabel">\s+Signatura:\s+</span>\s+<span class="tabularValue">([^<]*)',content)[0].strip()
        obsahSvazku = re.findall(r'Obsahy:\s+</span>\s+[^>]*>(.+?(?=</span>))',content,re.DOTALL)[0].replace('<br>',' ').replace('\n','').strip().replace(' ','').replace(';;','|').split('|')
        #poznamka = re.findall(r'Poznámka.*?(?=">)">([^<]*)',content,re.DOTALL)[0]

        obsah = {}

        for o in obsahSvazku:
            #print(o)
            if len(o) != 0:
                o = reversed(o.split(';'))
                od_do = {}
                for p in o:
                    if '-' in p:
                        tmp = p.split('-')
                        od_do = {'od':tmp[0], 'do':tmp[1]} 
                    elif 'i' in p: # indexes
                        if 'N' in p or len(p) == 1:
                            obsah['INDEX Narozených'] = od_do
                        elif 'O' in p or len(p) == 1:
                            obsah['INDEX Oddaných'] = od_do
                        elif 'Z' in p or len(p) == 1:
                            obsah['INDEX Zemřelých'] = od_do  
                    else:
                        if 'N' in p:    
                            obsah['Narození'] = od_do
                        elif 'O' in p:
                            obsah['Oddaní'] = od_do
                        elif 'Z' in p:    
                            obsah['Zemřelí'] = od_do    
        book['obsah'] = obsah
        
        # obsahuje matrika snimky?
        ifn = './'+dn+f'/images/json/{pn:05d}_images.json'
        if os.path.exists(ifn):
            with open(ifn, 'r',encoding='utf-8') as imagesFile:
                book['snimky'] = json.load(imagesFile)

        data['matriky'].append(book)
        data['pocet']+= 1
    json.dump(data,f,indent=4,ensure_ascii=False)
    
