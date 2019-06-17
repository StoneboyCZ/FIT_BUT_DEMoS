import json
import re
import os

settings = {}
settings['inputFileName'] = 'input.txt'

with open(settings['inputFileName'],'r',encoding='utf-8') as f:
    origContent = f.readlines()

    #print(len(origContent))

    # remove first page
    contentWithoutFirstPage = origContent[65:]

    #print(contentWithoutFirstPage)

    for l in contentWithoutFirstPage:
        if re.findall(r'- [\d]* -',l):
            pass
        
        zaznamy = []
        inUradOblast = False
        if 'farní úřad' in l or 'stavovský úřad' in l:
            if '(' in l: # for malformated entries
                l = l.split('(')[0]
            inUradoblast = True
            urad = {}
            #print(l)
            #urad['nazev'] = l.split('úřad')[1][1:].strip()
            #urad['typ'] = l.split(' ')[0]
            #urad['umisteni'] = []

            #print(f"{urad['nazev']} {urad['typ']}")   
    


