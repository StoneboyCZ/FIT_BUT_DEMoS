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

base = 'http://ebadatelna.soapraha.cz'

# number of files in the dn directory
dn = 'html-info'
files = [f for f in os.listdir(dn) if os.path.isfile(os.path.join(dn,f))]

data = {}
data['zdroj'] = 'SOAPraha'
data['matriky'] = []
 
with open("soa.json", 'w',encoding="utf-8") as of :
    #f.write("""{
    #"zdroj": "opava",
    #"matriky": [""")

    #for pn in range(1,3):
    for fn in files:
        # load a file
        fn = './'+dn+'/'+fn
        print(fn)
        with open(fn,'r',encoding="utf-8") as f:
            content = f.read()
        

        book = {}
        # obtain the information from the page
        puvodce = re.findall(r'Původce.*?(?=<span)<span>([^<]*)',content,re.DOTALL)[0]
        jazyk = re.findall(r'Jazyk.*?(?=<div>)<div>([^<]*)',content,re.DOTALL)[0]
        narozeni = list(re.findall(r'Narození / index.*?(?=<div>)<div>([^<]*).*?(?=<div>)<div>([^<]*)',content, re.DOTALL))
        oddani = list(re.findall(r'Oddaní / index.*?(?=<div>)<div>([^<]*).*?(?=<div>)<div>([^<]*)',content, re.DOTALL))
        zemreli = list(re.findall(r'Zemřelí / index.*?(?=<div>)<div>([^<]*).*?(?=<div>)<div>([^<]*)', content, re.DOTALL))
        uzemniRozsah = re.findall(r'obecCastLabel">([^<]*)',content,re.DOTALL)
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
        '''



        book['puvodce'] = puvodce

        # jazyky
        book['jazyky'] = None
        if '---' not in jazyk:
            book['jazyky'] = []
            jazyky = jazyk.split('část')
            jazyky = list(filter(None, jazyky))
            for j in jazyky:
                j = j.replace('a ','').replace(',','').strip()
                book['jazyky'].append(j)

        # obsah
                print(narozeni)



        # remove nbsp
        #narozeni = [item.replace('&nbsp;','') for item in narozeni]
        #oddani = [item.replace('&nbsp;','') for item in oddani]
        #zemreli = [item.replace('&nbsp;','') for item in zemreli]

        print(narozeni)
        print(oddani)
        print(zemreli)

        book['obsah'] = {}
        
        
         

        # obce
        book['obce'] = []
        
        nazvyAll = []
        for uz in uzemniRozsah:
            nazvy = uz.split('/')
            nazvy = [item.strip() for item in nazvy]
            nazvyAll.append(nazvy)

        book['obce'] = nazvyAll


        
        #print(book['puvodce'])
        #print(book['jazyky'])
        #print(narozeni)
        #print(oddani)
        #print(zemreli)

        data['matriky'].append(book)
           
    json.dump(data,of,indent=4,ensure_ascii=False)
    #f.write(']}')
    

