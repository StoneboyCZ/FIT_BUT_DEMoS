import json
import re
import os

# 87 + 535

settings = {}
settings['inputFileName'] = 'input.txt'

with open(settings['inputFileName'],'r',encoding='utf-8') as f:
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
        of.write(fixed6)


    for c in allContent:
        #print(c)
        uloziste = {}
        uloziste['typ'] = c[0]
        uloziste['misto'] = c[1].strip()

        info = c[2].strip()
        # uzemni obvod
        obvod = re.findall(r'územní obvod[:]*([^:]*)$',info,flags=re.DOTALL|re.MULTILINE)[0].strip().split('\n')
        uloziste['uzemni_obvod'] = []
        for o in obvod:
            uloziste['uzemni_obvod'].append(o)

        # zbytek informaci o ulozisti


    """
    origContent = f.readlines()

    #print(len(origContent))

    # remove first page
    contentWithoutFirstPage = origContent[65:]

    # split the document into sections
    oblasti = []
    inOblast = False
    for i,l in enumerate(contentWithoutFirstPage):
        #print(l)
        if re.findall(r'- [\d]* -',l):
            pass
        if 'farní úřad' in l or 'stavovský úřad' in l:

            if not inOblast:
                #print(l)
                inOblast = True
                #continue # skip to next line
            # oblast.append(l)
            else:


        if inOblast:
            #print(l)
            oblast = [] 
            
            if 'farní úřad' in l or 'stavovský úřad' in l:
                print(oblast)
                # konec oblasti
                inOblast = False
                oblasti.append(oblast)
            else:
                #print(l)
                oblast.append(l)    

    print(oblasti)

    """
    """
    for l in contentWithoutFirstPage:
        if re.findall(r'- [\d]* -',l):
            pass
        
        inOblast = False
        if 'farní úřad' in l or 'stavovský úřad' in l:
            if '(' in l: # for malformated entries
                l = l.split('(')[0]
            inOblastnn = True
            urad = {}

            #print(l)
            urad['nazev'] = l.split('úřad')[1][1:].strip()
            urad['typ'] = l.split(' ')[0]
            urad['umisteni'] = []

            #print(f"{urad['nazev']} {urad['typ']}")   
    """


