import json
import re
import os
import datetime

# 87 + 535

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

data = {}
data['zdroj'] = 'zamrsko'
data['vytvoreno'] = str(datetime.datetime.now())
data['stazeno'] = '2020-08-18'
data['pocet'] = 0
data['matriky'] = []

with open('input.txt','r',encoding='utf-8') as f:
    content = f.read()
    fixed1 = re.sub(r'farní úřad',r'______\nfarní úřad',content)
    fixed2 = re.sub(r'stavovský úřad',r'______\nstavovský úřad',fixed1)
    fixed3 = re.sub(r'okresní úřad',r'______\nokresní úřad',fixed2)
    fixed4 = re.sub(r'- [\d]* -',r'',fixed3)
    fixed5 = re.sub(r'E v i d e n č n í   ú d a j e   o   f o n d u',r'______\nE v i d e n č n í   ú d a j e   o   f o n d u',fixed4)
    fixed6 = re.sub(r'farní úřad: Mlýnický Dvůr',r'farní úřad: Mlýnický Dvůr\núzemní obvod:\n',fixed5)
    fixed7 = re.sub(r'farní úřad: Moravský Karlov',r'farní úřad: Moravský Karlov\núzemní obvod:\n',fixed6)

    allContent = re.findall(r'(farní|stavovský|okresní) úřad:([^\n]*)(.*?)(?=[\d]+ sign.)(.*?)(?=______)',fixed7,re.DOTALL)

    with open('fixed4.txt','w',encoding='utf-8') as of:
        of.write(fixed7)

    for c in allContent:
        #print(c)
        #uloziste = {}
        #uloziste['typ'] = c[0]
        #uloziste['misto'] = c[1].strip()

        # uzemni obvod
        info = re.findall(r'územní obvod[:]*[^$]([^:]*^)(.*)',c[2],flags=re.DOTALL|re.MULTILINE)[0]
        """
        uloziste['uzemni_obvod'] = []
        for o in obvod:
            uloziste['uzemni_obvod'].append(o)
        """
        # matriky
        matriky = re.findall(r'([\d]+) sign\. (.*?)(?=index|matrika)([^\d]*)(\S*).*?územní rozsah: (.*?)\n^[\d+].*?fol.,([^\n]*)',c[3],flags=re.DOTALL|re.MULTILINE)
        #print(c[3])
        

        for m in matriky:
            #print(m[0])
            matrika = {}
            matrika['id'] = m[0].strip()
            matrika['signatura'] = m[1].strip()
            matrika['typ'] = c[0].strip()
            matrika['puvodce'] = c[1].strip()

            # jazyky
            jazyky = []
            j = m[5].split(',')

            for jj in j:
                if 'čeština' in jj:
                    jazyky.append('čeština')
                elif 'němčina' in jj:
                    jazyky.append('němčina')
                elif 'latina' in jj:
                    jazyky.append('latina')
            
            matrika['jazyky'] = jazyky
            
            tmp = m[3].split('-')
            od_do = {}
            if len(tmp) == 1:
                od_do['od'] = tmp[0]
                od_do['do'] = tmp[0]
            else:
                od_do['od'] = tmp[0]
                od_do['do'] = tmp[1]
            
            obsah = {}
            
            o = m[2].strip().split(' ')
            #print(o)
            
            for i,op in enumerate(o):
                if 'matrika' in op:
                    if 'N' in o[i+1]:
                        obsah['Narození'] = od_do
                    
                    if 'O' in o[i+1]:
                        obsah['Oddaní'] = od_do
                    
                    if 'Z' in o[i+1]:
                        obsah['Zemřelí'] = od_do
                elif 'index' in op:
                    if 'N' in o[i+1]:
                        obsah['INDEX Narozených'] = od_do
                    if 'O' in o[i+1]:
                        obsah['INDEX Zemřelých'] = od_do
                    if 'Z' in o[i+1]:
                        obsah['INDEX Oddaných'] = od_do 
            
            matrika['obsah'] = obsah
            
            obce = m[4].replace('\n','').split(',')
            obce = list(map(str.strip,obce))
            
            matrika['obce'] = obce

            data['pocet'] = data['pocet'] + 1
            data['matriky'].append(matrika)

with open('zamrsk.json','w',encoding='utf-8') as f:
    json.dump(data,f,indent=4,ensure_ascii=False)           
