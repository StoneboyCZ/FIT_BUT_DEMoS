import xml.etree.ElementTree as ET
import pyproj
import json

sjtsk = pyproj.Proj("+init=epsg:5514")
wgs = pyproj.Proj("+init=epsg:4326")

staty = []
kraje = []
okresy = []
obceSRozsirenouPusobnosti = []
obceSPoverenymObecnimUradem = []
obce = []
casti = []

def toGPS(s):
    c = s.split(' ')
    cc = pyproj.transform(sjtsk, wgs, float(c[0]), float(c[1]))
    coords = {}
    coords['lat'] = cc[1]
    coords['lon'] = cc[0]
    return coords    

def saveJSON(fn,data):
    with open(fn+'.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

tree = ET.parse('ruian.xml')
root = tree.getroot()
data = root[1][0]

# staty
children = list(data.iter())
stat = {}
stat['id'] = children[2].text  
stat['nazev'] = children[3].text 
staty.append(stat)

saveJSON('staty',staty)

#print(children)
# vyssi spravni celky - kraje
data = root[1][3]
children = list(data.iter())
kraj = {}
for i,ch in enumerate(children):
    if ch.tag == '{urn:cz:isvs:ruian:schemas:VymennyFormatTypy:v1}Vusc':
        if kraj:
            kraje.append(kraj)
        kraj = {}
    if ch.tag == '{urn:cz:isvs:ruian:schemas:VuscIntTypy:v1}Kod':
        kraj['id'] = ch.text
    if ch.tag == '{urn:cz:isvs:ruian:schemas:VuscIntTypy:v1}Nazev':
        kraj['nazev'] = ch.text

    if i == len(children)-1:
        kraje.append(kraj)

saveJSON('kraje',kraje)


# okresy
data = root[1][4]
children = list(data.iter())
okres = {}
for i,ch in enumerate(children):
    if ch.tag == '{urn:cz:isvs:ruian:schemas:VymennyFormatTypy:v1}Okres':
        if okres:
            okresy.append(okres)
        okres = {}
    if ch.tag == '{urn:cz:isvs:ruian:schemas:OkresIntTypy:v1}Kod':
        okres['id'] = ch.text
    if ch.tag == '{urn:cz:isvs:ruian:schemas:OkresIntTypy:v1}Nazev':
        okres['nazev'] = ch.text
    if ch.tag == '{urn:cz:isvs:ruian:schemas:VuscIntTypy:v1}Kod':
        okres['kraj'] = ch.text
    
    if i == len(children) -1:
        okresy.append(okres)    

saveJSON('okresy',okresy)

# obce s rozsirenou pusobnosti
data = root[1][5]
children = list(data.iter())
obecSRozsirenouPusobnosti = {}
for i,ch in enumerate(children):
    if ch.tag == '{urn:cz:isvs:ruian:schemas:VymennyFormatTypy:v1}Orp':
        if obecSRozsirenouPusobnosti:
            obceSRozsirenouPusobnosti.append(obecSRozsirenouPusobnosti)
        obecSRozsirenouPusobnosti = {}
    if ch.tag == '{urn:cz:isvs:ruian:schemas:OrpIntTypy:v1}Kod':
        obecSRozsirenouPusobnosti['id'] = ch.text
    if ch.tag == '{urn:cz:isvs:ruian:schemas:OrpIntTypy:v1}Nazev':
        obecSRozsirenouPusobnosti['nazev'] = ch.text
    if ch.tag == '{urn:cz:isvs:ruian:schemas:VuscIntTypy:v1}Kod':
        obecSRozsirenouPusobnosti['kraj'] = ch.text
    if ch.tag == '{http://www.opengis.net/gml/3.2}pos':
        obecSRozsirenouPusobnosti['pos'] = toGPS(ch.text)

    if i == len(children)-1:
        obceSRozsirenouPusobnosti.append(obecSRozsirenouPusobnosti)    

saveJSON('obceSRozsirenouPusobnosti',obceSRozsirenouPusobnosti)

# obce s poverenym obecnim uradem
data = root[1][6]
children = list(data.iter())
obecSPoverenymObecnimUradem = {}
for i,ch in enumerate(children):
    if ch.tag == '{urn:cz:isvs:ruian:schemas:VymennyFormatTypy:v1}Pou':
        if obecSPoverenymObecnimUradem:
            obceSPoverenymObecnimUradem.append(obecSPoverenymObecnimUradem)
        obecSPoverenymObecnimUradem = {}
    if ch.tag == '{urn:cz:isvs:ruian:schemas:PouIntTypy:v1}Kod':
        obecSPoverenymObecnimUradem['id'] = ch.text
    if ch.tag == '{urn:cz:isvs:ruian:schemas:PouIntTypy:v1}Nazev':
        obecSPoverenymObecnimUradem['nazev'] = ch.text
    if ch.tag == '{urn:cz:isvs:ruian:schemas:OrpIntTypy:v1}Kod':
        obecSPoverenymObecnimUradem['orp'] = ch.text
    if ch.tag == '{http://www.opengis.net/gml/3.2}pos':
        obecSPoverenymObecnimUradem['pos'] = toGPS(ch.text)

    if i == len(children)-1:
        obceSPoverenymObecnimUradem.append(obecSPoverenymObecnimUradem)    

saveJSON('obceSPoverenymObecnimUradem',obceSPoverenymObecnimUradem)

# obce 
data = root[1][7]
children = list(data.iter())
obec = {}
for i,ch in enumerate(children):
    if ch.tag == '{urn:cz:isvs:ruian:schemas:VymennyFormatTypy:v1}Obec':
        if obec:
            obce.append(obec)
        obec = {}
    if ch.tag == '{urn:cz:isvs:ruian:schemas:ObecIntTypy:v1}Kod':
        obec['id'] = ch.text
    if ch.tag == '{urn:cz:isvs:ruian:schemas:ObecIntTypy:v1}Nazev':
        obec['nazev'] = ch.text
    if ch.tag == '{urn:cz:isvs:ruian:schemas:OkresIntTypy:v1}Kod':
        obec['okres'] = ch.text
    if ch.tag == '{urn:cz:isvs:ruian:schemas:PouIntTypy:v1}Kod':
        obec['pou'] = ch.text
    if ch.tag == '{http://www.opengis.net/gml/3.2}pos':
        obec['pos'] = toGPS(ch.text)
    
    if i == len(children)-1:
        obce.append(obec)  

saveJSON('obce',obce)

# casti mest a obci
data1 = root[1][10]
children1 = list(data1.iter())
data2 = root[1][11]
children2 = list(data2.iter())
children = children1+children2
cast = {}
for i,ch in enumerate(children):
    #print(ch.tag)
    if ch.tag == '{urn:cz:isvs:ruian:schemas:VymennyFormatTypy:v1}Momc': 
        if cast:
            cast['typ'] = 'castMesta'
            casti.append(cast)
        cast = {}
    if ch.tag == '{urn:cz:isvs:ruian:schemas:VymennyFormatTypy:v1}CastObce':
        if cast:
            cast['typ'] = 'castObce'
            casti.append(cast)
        cast = {} 
    if ch.tag == '{urn:cz:isvs:ruian:schemas:MomcIntTypy:v1}Kod' or ch.tag == '{urn:cz:isvs:ruian:schemas:CastObceIntTypy:v1}Kod':
        cast['id'] = ch.text
    if ch.tag == '{urn:cz:isvs:ruian:schemas:MomcIntTypy:v1}Nazev' or ch.tag == '{urn:cz:isvs:ruian:schemas:CastObceIntTypy:v1}Nazev':
        cast['nazev'] = ch.text
    if ch.tag == '{urn:cz:isvs:ruian:schemas:ObecIntTypy:v1}Kod' or ch.tag == '{urn:cz:isvs:ruian:schemas:ObecIntTypy:v1}Kod':
        cast['obec'] = ch.text
    if ch.tag == '{http://www.opengis.net/gml/3.2}pos':
        cast['pos'] = toGPS(ch.text)
    
    if i == len(children)-1:
        casti.append(cast)

saveJSON('castiObci',casti)
