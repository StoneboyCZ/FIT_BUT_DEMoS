import xml.etree.ElementTree as ET
import pyproj

sjtsk = pyproj.Proj("+init=epsg:5514")
wgs = pyproj.Proj("+init=epsg:4326")

staty = []
kraje = []
okresy = []
obce = []

def toGPS(s):
    c = s.split(' ')
    cc = pyproj.transform(sjtsk, wgs, float(c[0]), float(c[1]))
    coords = {}
    coords['lat'] = cc[1]
    coords['lon'] = cc[0]
    return coords    


tree = ET.parse('ruian.xml')
root = tree.getroot()
data = root[1][0]

# staty
children = list(data.iter())
stat = {}
stat['id'] = children[2].text  
stat['nazev'] = children[3].text 
staty.append(stat)

#print(children)
# vyssi spravni celky - kraje
data = root[1][3]
children = data.iter()
kraj = {}
for ch in children:
    if ch.tag == '{urn:cz:isvs:ruian:schemas:VymennyFormatTypy:v1}Vusc':
        if kraj:
            kraje.append(kraj)
        kraj = {}
    if ch.tag == '{urn:cz:isvs:ruian:schemas:VuscIntTypy:v1}Kod':
        kraj['id'] = ch.text
    if ch.tag == '{urn:cz:isvs:ruian:schemas:VuscIntTypy:v1}Nazev':
        kraj['nazev'] = ch.text


# okresy
data = root[1][4]
children = data.iter()
okres = {}
for ch in children:
#    print(ch.tag)
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

# obce 
data = root[1][7]
children = data.iter()
obec = {}
for ch in children:
    print(ch.tag)
    if ch.tag == '{urn:cz:isvs:ruian:schemas:VymennyFormatTypy:v1}Pou':
        if obec:
            obce.append(obec)
        obec = {}
    if ch.tag == '{urn:cz:isvs:ruian:schemas:PouIntTypy:v1}Kod':
        obec['id'] = ch.text
    if ch.tag == '{urn:cz:isvs:ruian:schemas:PouIntTypy:v1}Nazev':
        obec['nazev'] = ch.text
    if ch.tag == '{urn:cz:isvs:ruian:schemas:VuscIntTypy:v1}Kod':
        obec['kraj'] = ch.text

