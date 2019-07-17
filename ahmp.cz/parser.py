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

dn = 'html'
files = [f for f in os.listdir(dn) if os.path.isfile(os.path.join(dn,f))]
numberOfEntries = len(files)

print(numberOfEntries)
data = {}
data['zdroj'] = 'abmp'
data['matriky'] = []
 
with open("abmp.json", 'w',encoding="utf-8") as f:
    #f.write("""{
    #"zdroj": "opava",
    #"matriky": [""")

    #for pn in range(1,3):
    for pn in range(1,numberOfEntries,1):
        # load a file
        fn = './'+dn+f'/{pn:05d}.html'
        print(fn)
        htmlFile = open(fn, 'r',encoding='utf-8')
        content = htmlFile.read()
        
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

        idn = './'+dn+f'/images/{pn:05d}'
        print(idn)
        #if os.path.exists(ifn):
        #    with open(ifn, 'r',encoding='utf-8') as iif:
        #        imContent = iif.read()
        #        images = 
        '''
        signatura = re.findall(r'div class=\"labelFloat\">Signatura [^>]*[^<]*[^>]*>([^<]*)',content)
        invCislo = re.findall(r'div class=\"labelFloat\">Inventární [^>]*[^<]*[^>]*>([^<]*)',content)
        typMatriky = re.findall(r'div class=\"labelFloat\">Typ [^>]*[^<]*[^>]*>([^<]*)',content)
        jazyk = re.findall(r'div class=\"labelFloat\">Jazyk:[^>]*[^<]*[^>]*>([^<]*)',content)
        casovyRozsah = re.findall(r'div class=\"labelFloat\">Časový[^>]*[^<]*[^>]*>([^<]*)',content)
        obsahSvazku = re.findall(r'div class=\"labelFloat\">Obsah [^>]*[^<]*[^>]*>([^<]*)',content)
        mistoUlozeni = re.findall(r'div class=\"labelFloat\">Místo [^>]*[^<]*[^>]*>([^<]*)',content) 
        uzemniRozsahSeznam = re.findall(r'div class=\"labelFloat\">Územní [^>]*[^<]*[^>]*>([^<]*)',content)
        uzemniRozsah = re.findall(r'<tr class="propojLok">\s*<[^>]*>([^<]*).*\s*</tr>\s*<tr>\s*.*?(?=va)[^>]*>(.*?)(?=</td)',content)
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
            obsahSvazku = obsahSvazku[0].strip().replace('\n','')
            obsahSvazku = obsahSvazku.split('                                                                  ')
            
    #       print(obsahSvazku)
        
            od_do = {}
            for t in obsahSvazku:
                #print(len(t))
                if len(t) > 1 and ' • ' in t:
                    t = t.split(' • ')
                    if '-' in t[1]:
                        t[1] = t[1].split('-')
                        t[1][0] = (t[1][0]).strip()
                        t[1][1] = (t[1][1]).strip()
                        od_do = {'od':t[1][0], 'do':t[1][1]} 
                    else:
                        t[1] = (t[1])
                        od_do = {'od':t[1], 'do':t[1]} 
                
                if t[0] == 'I-N':
                    obsah['INDEX Narozených'] = od_do
                elif t[0] == 'I-Z':
                    obsah['INDEX Zemřelých'] = od_do
                elif t[0] == 'I-O':
                    obsah['INDEX Oddaných'] = od_do
                elif t[0] == 'N':
                    obsah['Narození'] = od_do
                elif t[0] == 'O':
                    obsah['Oddaní'] = od_do
                elif t[0] == 'Z':
                    obsah['Zemřelí'] = od_do
                else:
                    obsah['Poznámka'] = t
            
            #print(obsah)
                       
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
            
            
            umisteni = {}
            misto = uzemi[1].split('; ')
            #print(misto)
            # stat, kraj, okres, obec, cast_obce, samota
            umisteni['stat'] = misto[0]
            umisteni['kraj'] = misto[1]
            umisteni['okres'] = misto[2]
            umisteni['obec'] = misto[3].replace('<b>', '').replace('</b>','')
            umisteni['cast_obce'] = misto[4]
            umisteni['samota'] = misto[5]  
            
            obec['umisteni'] = umisteni 
            book['obce'].append(obec)

        # snimky
        
        # obsahuje matrika snimky?
        ifn = './'+dn+f'/images/{pn:05d}_images.html'
        if os.path.exists(ifn):
            imagesFile = open(ifn, 'r',encoding='utf-8')
            imContent = imagesFile.read()
            jsonString = re.findall(r'resultJSON = (.*?(?=};)})',imContent)
            jsonString = jsonString[0]
            j = json.loads(jsonString)
            snimky = {}
            snimky['jmeno'] = j['entity']['saveAs']
            snimky['url'] = []
            for entry in j['media']:
                url = 'http://images.archives.cz/mrimage/matriky/proxy/'+entry['uri']
                snimky['url'].append(url)
            book['snimky'] = snimky
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
    '''

