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

    allContent = re.findall(r'(farní|stavovský|okresní) úřad(.*?)(?=______)',fixed4,re.DOTALL)

    
    for c in allContent:
        uloziste = {}
        uloziste['typ'] = c[0]
        print(uloziste['typ'])

        for l in c[1].split('\n'):
            if 'územní obvod' in l:
                print(l)
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


