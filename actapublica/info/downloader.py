# http://docs.python-requests.org/en/master/user/quickstart/#cookies
# http://docs.python-requests.org/en/master/user/install/#install
# http://actapublica.eu/brno/77/cut/77-004-1-1.png

# prehled vsech archivu, ze kterych se bude stahovat
# https://digi.ceskearchivy.cz/DA?lang=cs&
# xml generation: https://docs.python.org/3/library/xml.etree.elementtree.html#module-xml.etree.ElementTree

import requests 
import random
import time
import re
import os
#import xml.etree.ElementTree as ET # XML
from lxml import etree as ET

from requests.adapters import HTTPAdapter

def striplist(l):
    return([x.strip() for x in l])


cookies = dict(
    PHPSESSID='uld0otqg6r04pdel6upin4j676',
    __utmc='203544448',
    __utma='203544448.1704102175.1525090029.1528284701.1528701007.12',
    __utmz='203544448.1526036435.8.2.utmcsr=mza.cz|utmccn=(referral)|utmcmd=referral|utmcct=/a8web/a8apps1/a8apps1.htm',
    __utmt='1',
    __utmb='203544448.6.10.1528701007'
    )

# creates a random number
random.seed() 

# create a session object
s = requests.Session()
s.mount('http://actapublica.eu', HTTPAdapter(max_retries=20))
# first page of the archive
url = 'http://actapublica.eu/matriky/brno/?pg=1'

# download the webpage 
r = s.get(url,cookies=cookies)    
content = r.text

# how many pages do we need to process? Two matches, same number
matches = re.findall(r'Přejít na stranu číslo [^>]*> z celkem (\d*)',content)
numOfPages = matches[0]
#print(numOfPages)

# create root of the XML document
root = ET.Element('matriky')
root.set('zdroj','ActaPublica')

with open("actapublica.xml", 'w',encoding="utf-8") as f:
    string = ET.tostring(root,encoding='unicode')
    f.write(string)

    #for pn in range(1,2,1):
    #for pn in range(1,int(numOfPages)+1,1):
    for pn in range(1,int(numOfPages)+1,1):
        if pn != 1: # first page doesnt have to be downloaded again
            url = 'http://actapublica.eu/matriky/brno/?pg='+str(pn)
            r = s.get(url,cookies=cookies)    
            content = r.text 

        # match all adresses
        # matchesAdress[0] actapublica.eu
        # matchesAdress[1] matriky
        # matchesAdress[2] brno
        # matchesAdress[3] detail
        # matchesAdress[4] id
        # matchesAdress[5] signatura
        
        # find all rows on the page
        #matchesAdress = re.findall(r'<td class=\"row1\"><a href=\"http://([^/]*)/([^/]*)/([^/]*)/([^/]*)/([^/]*).\" title=\"([^/]\d*)\"',content)
        matchesAdress = re.findall(r'<td class=\"row1\"><a href=\"http://([^/]*)/([^/]*)/([^/]*)/([^/]*)/([^/]*).\" title=\"([^\"]*)',content)

        #print(matchesAdress)
        # get the number of pages <td class=\"row1\">(\d*)</td>
        matchesNumberOfPages = re.findall(r'<td class=\"row1\">(\d*)</td>',content)

        # remove empty
        matchesAdress = list(filter(None, matchesAdress))
        matchesNumberOfPages = list(filter(None, matchesNumberOfPages))

        # work with each match
        for adress,numberOfPages in zip(matchesAdress,matchesNumberOfPages):
            #sleepTime = random.gauss(2, 0.5)
            sleepTime = 1
            print(adress)
            print(numberOfPages)

            # add book to XML
            book = ET.SubElement(root,'kniha')
            # add signature to the book
            book.set('signatura',adress[5])

            # request the info page
            url = 'http://'+adress[0]+'/'+adress[1]+'/'+adress[2]+'/'+adress[3]+'/'+adress[4]+'/'
            print(url)
            r = s.get(url,cookies=cookies,timeout=10)    
            content = r.text # content of the info page

            # create the appropriate XML tags and save the data        
            type = ET.SubElement(book,'typ')
            matches = re.findall(r'Původce[^(]*[^>]*>([^<]*)',content)
            print(str(matches[0]))
            type.text = str(matches[0])

            # county (okres)
            county = ET.SubElement(book,'okres')
            matches = re.findall(r'Okres[^>]*>([^<]*)',content)
            print(str(matches[0]))
            county.text = str(matches[0])


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