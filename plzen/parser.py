# http://docs.python-requests.org/en/master/user/quickstart/#cookies
# http://docs.python-requests.org/en/master/user/install/#install
# http://images.archives.cz/mrimage/matriky/proxy/cz/archives/CZ-217000010/NAD-165/dao/images/0345/8b1ef2b1-eba4-4b55-805d-f79d56afada0.jpg
# http://digi.archives.cz/da/Zoomify.action?entityRef=%28%5En%29%28%28%28localArchiv%2C%5En%2Chot_%29%28unidata%29%29%28338508%29%29&scanIndex=0

# I-N_I-Z_I-O_inv_c_124a_sig_Op_VII_13_1789-1799_Katerinky_025.jpg

# <tr class="propojLok">\s*<[^>]*>([^<]*).*\s*</tr>\s*<tr>\s*.*?(?=va)[^>]*>(.*?)(?=</td)

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

obceRUIAN = loadJSON('ruian/obce.json')
castiObciRUIAN = loadJSON('ruian/castiObci.json')


dn = 'html'
files = [f for f in os.listdir(dn) if os.path.isfile(os.path.join(dn,f))]
numberOfEntries = len(files)

print(numberOfEntries)

data = {}
data['zdroj'] = 'plzen'
data['vytvoreno'] = str(datetime.datetime.now())
data['stazeno'] = loadJSON('info.json')['downloaded']
data['pocet'] = 0
data['snimky_zaklad'] = 'http://www.portafontium.eu'
data['matriky'] = []
 
with open("plzen.json", 'w',encoding="utf-8") as f:
    for pn in range(1,numberOfEntries+1,1):
        # load a file
        fn = './'+dn+f'/{pn:05d}.html'
        print(fn)
        htmlFile = open(fn, 'r',encoding='utf-8')
        content = htmlFile.read()
        
        book = {}

        # obtain the information from the page
        puvodce = re.findall(r'Původce.*?(?="field-item )[^>]*>([^<]*)',content)
        signatura = re.findall(r'Signatura.*?(?="field-item )[^>]*>([^<]*)',content)
        mista = re.findall(r'Místo:.*(?=even")even">([^<]*)',content)
        #typMatriky = re.findall(r'Sbírka matrik západních Čech.*?(?=">)">([^<]*)',content)
        jazyk = re.findall(r'div class=\"labelFloat\">Jazyk:[^>]*[^<]*[^>]*>([^<]*)',content)
        obsahSvazku = re.findall(r'<span class="fieldset-legend">Datace.*?(?="field-item )[^>]*>([^<]*)',content)
        poznamka = re.findall(r'Obsah:.*?(?="field-item )[^>]*>(.*?)(?=</div)',content,re.DOTALL)
        mistoUlozeni = re.findall(r'Archiv.*?(?="field-item )[^>]*>([^<]*)',content) 
        snimkyList = re.findall(r'<div class="iip-thumbnail-number">.*?(?=src)src="([^"]*)',content) 

        
        book['signatura'] = signatura[0]
        #book['typ'] = typMatriky[0]
        book['misto_ulozeni'] = mistoUlozeni[0]
       
        if len(jazyk) > 0:
            if ',' in jazyk[0] and len(jazyk) != 0:
                book['jazyky'] = jazyk[0].replace(' ', '').split(',')
            else:
                book['jazyky'] = jazyk[0]
        
        book['puvodce'] = puvodce[0]

        
        
        
        if len(mista) > 0:
            book['obce'] = {}
            obce = {}
            state = 'outBracket'
            jmeno = ''
            varianta = ''
            varianty = []
            
            for i,m in enumerate(mista[0]):
                #print(f'{m} {state} {i}')
                if m == '(':
                    state = 'beginBracket'
                
                if state == 'outBracket':
                    if m == ',': 
                        jmeno=jmeno.strip()
                        obce[jmeno] = {}
                        obce[jmeno]['varianty'] = varianty
                        obce[jmeno]['ruian'] = None
                        obce[jmeno]['ruian'] = findInRUIAN(jmeno, obceRUIAN)
                        if obce[jmeno]['ruian'] == None:
                            obce[jmeno]['ruian'] = findInRUIAN(jmeno, castiObciRUIAN)    
                        jmeno = ''
                        varianty = []
                    elif m == ')':
                        continue
                    else:
                        jmeno = jmeno + m

                
                if state == 'beginBracket':
                    if m == ',':
                        #print('append')
                        varianty.append(varianta)
                    if m == ')':
                        #print('append')
                        varianty.append(varianta)
                        state = 'outBracket'
                    elif m == '(':
                        varianta = ''
                    else:
                        varianta = varianta + m
            
                if i==len(mista[0])-1:
                    jmeno = jmeno.strip()
                    obce[jmeno] = {}
                    obce[jmeno]['varianty'] = varianty
                    obce[jmeno]['ruian'] = None
                    obce[jmeno]['ruian'] = findInRUIAN(jmeno, obceRUIAN)
                    if obce[jmeno]['ruian'] == None:
                        obce[jmeno]['ruian'] = findInRUIAN(jmeno, castiObciRUIAN)  
                    jmeno = ''
                    varianty = []    
            
            book['obce'] = obce
        



        #for o in ob:
        #    o = o.strip()
            
            #print(o)
            #reg = re.findall(r'([^\(]*).*=?\((.*)',o)
            #print(reg[0])
            #o = o.split(' (')
            #print(o)
            
        """
        reg = re.findall(r'([\S]*)',o)
        print(reg)
        for i, r in enumerate(reg):
            if i == 0:
                book['obce'][reg[0]] = {}
            elif i==1:
                book['obce'][reg[0]]['varianty'] = []    
                book['obce'][reg[0]]['varianty'].append(reg[i])
            else:
                book['obce'][reg[0]]['varianty'].append(reg[i])
        
        book['obce'][reg[0]]['ruian'] = None
        book['obce'][reg[0]]['ruian'] = findInRUIAN(reg[0],obce)
        if book['obce'][reg[0]]['ruian'] == None:
            book['obce'][reg[0]]['ruian'] = findInRUIAN(reg[0],castiObci)    
        """
        

        obsah = {}
        if obsahSvazku:
            # preproceess
            obsahSvazku = obsahSvazku[0].split(',')
            tmp = obsahSvazku[0].split(' ')
            del[obsahSvazku[0]]

            for t in reversed(tmp):
                obsahSvazku.insert(0,t)
            
            od_do = {}
            for t in obsahSvazku:
                t = t.strip()

                if '-' in t: # dates
                    tmp = t.split('-')
                    od_do = {'od':tmp[0], 'do':tmp[1]}    
                elif t == '*':
                    obsah['Narození'] = od_do
                elif t == 'oo':
                    obsah['Oddaní'] = od_do
                elif t == '+':
                    obsah['Zemřelí'] = od_do
                elif t == '*i':
                    obsah['INDEX Narozených'] = od_do
                elif t == 'ooi':
                    obsah['INDEX Oddaných'] = od_do
                elif t == '+i':
                    obsah['INDEX Zemřelých'] = od_do       

        if len(poznamka) > 0:
            poznamka = poznamka[0]
            poznamka = poznamka.replace('<p>','').replace('</p>','').replace('<br />','\n')
            obsah['poznamka'] = poznamka
        
        book['obsah'] = obsah

        # snimky
       
        if len(snimkyList) > 0:
            snimky = {}

            jmeno = snimkyList[0].split('/')[-1].split('.')[0]+'.jpg'
            #print(jmeno)
            snimky['jmeno'] = jmeno

            snimky['url'] = []
            for s in snimkyList:
                s = s.replace('wid=100','wid=2000')
                snimek = {}
                snimek['url'] = s
                snimky['url'].append(snimek)    

            book['snimky'] = snimky
        
        data['matriky'].append(book)  
        data['pocet'] += 1            
    json.dump(data,f,indent=4,ensure_ascii=False)
    

