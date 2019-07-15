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
data['zdroj'] = 'plzen'
data['matriky'] = []
 
with open("plzen.json", 'w',encoding="utf-8") as f:
    #f.write("""{
    #"zdroj": "opava",
    #"matriky": [""")

    #for pn in range(1,3):
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
                snimky['url'].append('http://www.portafontium.eu'+s)    


            book['snimky'] = snimky
        
        data['matriky'].append(book)  
                
    json.dump(data,f,indent=4,ensure_ascii=False)
    

