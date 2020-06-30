import xml.etree.ElementTree as ET

staty = []
kraje = []

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

data = root[1][3]
children = data.iter()
kraj = {}
for ch in children:
    if ch.tag == '{urn:cz:isvs:ruian:schemas:VymennyFormatTypy:v1}Vusc':
        if kraj:
            kraje.append(kraj)
        kraj = {}
        kraj['okresy'] = [] 
    if ch.tag == '{urn:cz:isvs:ruian:schemas:VuscIntTypy:v1}Kod':
        kraj['id'] = ch.text
    if ch.tag == '{urn:cz:isvs:ruian:schemas:VuscIntTypy:v1}Nazev':
        kraj['nazev'] = ch.text



