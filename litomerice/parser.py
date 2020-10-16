import re
import os
import json
import datetime


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


obce = loadJSON('ruian/obce.json')
castiObci = loadJSON('ruian/castiObci.json')

dn = 'html'
files = [f for f in os.listdir(dn) if os.path.isfile(os.path.join(dn,f))]
numberOfEntries = len(files)

data = {}
data['zdroj'] = 'litomerice'
data['pocet'] = 0
data['snimky_zaklad'] = 'http://images.soalitomerice.cz/mrimage/matriky/proxy/cz/archives/'
data['vytvoreno'] = str(datetime.datetime.now())
data['stazeno'] = loadJSON('info.json')['downloaded']
data['matriky'] = []
 
with open("litomerice.json", 'w',encoding="utf-8") as f:
    for pn in range(1,numberOfEntries+1,1):
        # load a file
        fn = './'+dn+f'/{pn:05d}.html'
        print(fn)
        htmlFile = open(fn, 'r',encoding='utf-8')
        content = htmlFile.read()
        
        data['pocet'] += 1

        book = {}

        # obtain the information from the page
        puvodce = re.findall(r'div class=\"labelFloat\">Původce[^>]*[^<]*[^>]*>([^<]*)',content)
        signatura = re.findall(r'div class=\"labelFloat\">Signatura:[^>]*[^<]*[^>]*>([^<]*)',content)
        invCislo = re.findall(r'div class=\"labelFloat\">Inventární [^>]*[^<]*[^>]*>([^<]*)',content)
        typMatriky = re.findall(r'div class=\"labelFloat\">Typ [^>]*[^<]*[^>]*>([^<]*)',content)
        #jazyk = re.findall(r'div class=\"labelFloat\">Jazyk:[^>]*[^<]*[^>]*>([^<]*)',content)
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
        """
        if len(jazyk) > 0:
            if ',' in jazyk[0] and len(jazyk) != 0:
                book['jazyky'] = jazyk[0].replace(' ', '').split(',')
            else:
                book['jazyky'] = jazyk[0]
        """
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

            # find in ruian
            obec['ruian'] = findInRUIAN(umisteni['cast_obce'],castiObci)

            book['obce'].append(obec)

        # snimky
        
        # obsahuje matrika snimky?
        ifn = './'+dn+f'/images/json/{pn:05d}_images.json'
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
    

