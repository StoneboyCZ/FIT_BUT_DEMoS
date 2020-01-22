# http://docs.python-requests.org/en/master/user/quickstart/#cookies
# http://docs.python-requests.org/en/master/user/install/#install
# http://actapublica.eu/brno/77/cut/77-004-1-1.png

# prehled vsech archivu, ze kterych se bude stahovat
# https://digi.ceskearchivy.cz/DA?lang=cs&
# xml generation: https://docs.python.org/3/library/xml.etree.elementtree.html#module-xml.etree.ElementTree

import time
import re
import os
import json

dn = './html/'

data = {}
data['zdroj'] = 'actapublica'
data['matriky'] = []

for fn in os.listdir(dn):
    print(fn)
    
    with open(fn, 'r', encoding='utf-8') as f:
        content = f.read()

        matrika = {}

        matches = re.findall(r'Původce[^(]*[^>]*>([^<]*)',content)
        matrika['typ'] = matches[0]

        matches = re.findall(r'Okres[^>]*>([^<]*)',content)
        matrika['okres'] = matches[0]

        ## municipality (obec)
        municipalities = {}
        matches = re.findall(r'Obce[^>]*>[^>]*>[^>]*>([^<]*)',content)
        # split by delimiter
        split = matches[0].split(',')

        ## https://vdp.cuzk.cz/vdp/ruian/obce/vyhledej?vc.kod=&op.kod=&ok.kod=&pu.kod=&ob.nazev=Adamov&ob.statusKod=&ob.kod=&ohrada.id=&obg.sort=UZEMI&search=Vyhledat

        for m in split:
            municipalities[m] = {}
            m = m.strip()
            municipalities[m]['nazev'] = m


            

        # languages (jazyky)
        languages = ET.SubElement(book,'jazyky')
        matches = re.findall(r'Jazyk[^>]*>([^&]*|[^<]*)',content)

        # pre-processing

        
        for lang in matches:
            # split the languages?
            splitList = lang.split('.')
            if len(splitList) > 1: # more languages 
                splitList = list(filter(None, splitList))
                striplist(splitList)

                for sp in splitList:
                    language = ET.SubElement(languages,'jazyk')
                    if sp == 'čes':                    
                        language.text = 'čeština'
                    elif sp == 'něm':
                        language.text = 'němčina'
                    elif sp == 'lat':
                        language.text = 'latina'
            else: # one language
                language = ET.SubElement(languages,'jazyk')
                language.text = str(lang)

        # origin (puvodce)
        origin = ET.SubElement(book,'puvodce')
        matches = re.findall(r'Původce[^>(]*>([^>(]*)',content)
        origin.set('jmeno',str(matches[0]).strip())

        # municipality (obec)
        municipalities = ET.SubElement(book,'obce')
        matches = re.findall(r'Obce[^>]*>[^>]*>[^>]*>([^<]*)',content)

        # split by delimiter
        split = matches[0].split(',')
        #print(split)

        for m in split:
            obec = ET.SubElement(municipalities,'obec')
            m = m.strip()
            obec.text = str(m)

        # \<td\>(\d*)...(\d*)
        # content (obsah kroniky)
        # pole, ktere obsahuje typy
        typesListNames = ['Narození','Oddaní','Zemřelí','INDEX Narozených','INDEX Oddaných','INDEX Zemřelých']
        contentBook = ET.SubElement(book,'obsah')
        matches = re.findall(r'\<td\>(\d*)...(\d*)',content) # all ranges

        #print(matches)

        for match,typeName in zip(matches,typesListNames):
            if match[0] and match[1]:
                contentType = ET.SubElement(contentBook,'typ')
                print(typeName)
                print(match)
                contentType.set('nazev',typeName)
                contentTypeRange = ET.SubElement(contentType,'rozsah')
                contentTypeRange.set('od',match[0])
                contentTypeRange.set('do',match[1])        

        images = ET.SubElement(book,'snimky')
        images.set('pocet',numberOfPages)
        # download information and adresses of images associated with the book
        
        dn = "./"+book[5]

        # make the appropriate directory to save images
        if not os.path.exists(dn):
            os.makedirs(dn)
        
        if int(numberOfPages) > 0:
            for n in range(1,int(numberOfPages)+1,1):
                index='{num:03d}'.format(num=n)
                url = "http://"+adress[0]+"/"+adress[2]+"/"+adress[5]+"/cut/"+adress[5]+"-"+index+"-1-1.png"
                print(url)
                
                # get information about the image
                #im = s.get(url,cookies=cookies)    

                image = ET.SubElement(images,'snimek')
                #print(str(len(im.content)/1024))
                #image.set('velikost',str(len(im.content)/1024))
                image.text = url

                #time.sleep(sleepTime)
                
                
                ET.dump(book)

                string = ET.tostring(book,encoding='unicode',pretty_print='true')
                f.write(string)

                time.sleep(sleepTime)
            
        f.write('</matriky>')

