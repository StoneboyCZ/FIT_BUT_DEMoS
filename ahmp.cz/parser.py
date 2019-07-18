# http://docs.python-requests.org/en/master/user/quickstart/#cookies
# http://docs.python-requests.org/en/master/user/install/#install
# http://images.archives.cz/mrimage/matriky/proxy/cz/archives/CZ-217000010/NAD-165/dao/images/0345/8b1ef2b1-eba4-4b55-805d-f79d56afada0.jpg
# http://digi.archives.cz/da/Zoomify.action?entityRef=%28%5En%29%28%28%28localArchiv%2C%5En%2Chot_%29%28unidata%29%29%28338508%29%29&scanIndex=0

# I-N_I-Z_I-O_inv_c_124a_sig_Op_VII_13_1789-1799_Katerinky_025.jpg

# <tr class="propojLok">\s*<[^>]*>([^<]*).*\s*</tr>\s*<tr>\s*.*?(?=va)[^>]*>(.*?)(?=</td)

# http://images.ahmp.cz/mrimage/ahmp/proxy/cz/archives/CZ-321100010/NAD-156/dao/images/0060/8f8491b495f7b49d4b69e2c4ecef862f.jpg

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
        
        # obsahuje matrika snimky?
        ifn = './'+dn+f'/images/json/{pn:05d}_images.json'
        if os.path.exists(ifn):
            with open(ifn, 'r',encoding='utf-8') as imagesFile:
                book['snimky'] = json.load(imagesFile)

        data['matriky'].append(book)

    json.dump(data,f,indent=4,ensure_ascii=False)
    
