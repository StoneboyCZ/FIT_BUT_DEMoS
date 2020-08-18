# http://docs.python-requests.org/en/master/user/quickstart/#cookies
# http://docs.python-requests.org/en/master/user/install/#install
# http://images.archives.cz/mrimage/matriky/proxy/cz/archives/CZ-217000010/NAD-165/dao/images/0345/8b1ef2b1-eba4-4b55-805d-f79d56afada0.jpg
# http://digi.archives.cz/da/Zoomify.action?entityRef=%28%5En%29%28%28%28localArchiv%2C%5En%2Chot_%29%28unidata%29%29%28338508%29%29&scanIndex=0

# I-N_I-Z_I-O_inv_c_124a_sig_Op_VII_13_1789-1799_Katerinky_025.jpg

# <tr class="propojLok">\s*<[^>]*>([^<]*).*\s*</tr>\s*<tr>\s*.*?(?=va)[^>]*>(.*?)(?=</td)

from lxml import etree
import json
import datetime

tree = etree.parse('matriky.xml')
root = tree.getroot()

puvodciXML = root.findall('.//{http://www.mvcr.cz/archivy/evidence-nad/matriky}puvodce')
puvodci = {}
for p in puvodciXML:
    puvodci[p.get('idPuvodce')] = p[0].text

lokalityXML = root.findall('.//{http://www.mvcr.cz/archivy/evidence-nad/matriky}lokalita')
lokality = {}
for l in lokalityXML:
#    print(l)
    lokalita = {}
    lokalita['stat'] = l[0].text
    lokalita['kraj'] = l[1].text
    lokalita['okres'] = l[2].text
    lokalita['obec'] = l[3].text
    lokalita['cast_obce'] =l[4].text
    if l[5].text is None:
        lokalita['samota'] = ""
    else:
        lokalita['samota'] = l[5].text
    lokality[l.get('idLokality')]=lokalita

print(lokality)
"""
<matrika>
    <klicMatriky>
      <nad:c_archivu verCisNAD="499/2004">212000010</nad:c_archivu>
      <porCislo>2001</porCislo>
    </klicMatriky>
    <nad:c_karty>24</nad:c_karty>
    <oznaceniMatriky>
       <invCislo>1</invCislo>
    </oznaceniMatriky>
    <idPuvodce>1</idPuvodce>
    <uzemniRozsah></uzemniRozsah>
    <obsahMatriky charakterObsahuMatriky="N">
      <casRozsahCasti>1717-1757</casRozsahCasti>
    </obsahMatriky>
    <obsahMatriky charakterObsahuMatriky="O">
      <casRozsahCasti>1718-1757</casRozsahCasti>
    </obsahMatriky>
    <obsahMatriky charakterObsahuMatriky="Z">
      <casRozsahCasti>1717-1757</casRozsahCasti>
    </obsahMatriky>
    <casRozsah>
      <rokMin>1717</rokMin>
      <rokMax>1757</rokMax>
    </casRozsah>
    <propojLokality>
    </propojLokality>
    <idMistaUlozeni>1</idMistaUlozeni>
    <jazykMatriky>
      <jazyk>latina</jazyk>
    </jazykMatriky>
    <vybrano>1</vybrano>
    <typMatriky>katolická</typMatriky>
  </matrika>
"""
matrikyXML = root.findall('.//{http://www.mvcr.cz/archivy/evidence-nad/matriky}matrika')

data = {}
data['zdroj'] = 'trebon'
data['vytvoreno'] = str(datetime.datetime.now())
data['pocet'] = 0
data['matriky'] = []

for m in matrikyXML:
    book = {}
    
    book['signatura'] = m.find('.//{http://www.mvcr.cz/archivy/evidence-nad/matriky}porCislo').text+'/'+m.find('.//{http://www.mvcr.cz/archivy/evidence-nad/matriky}invCislo').text
    book['inv. cislo'] = m.find('.//{http://www.mvcr.cz/archivy/evidence-nad/matriky}invCislo').text

    # puvodce
    idPuvodce = m.find('.//{http://www.mvcr.cz/archivy/evidence-nad/matriky}idPuvodce').text
    book['puvodce'] = puvodci[idPuvodce]

    # obce
    """
    obce = {}
    idPuvodce = m.find('.//{http://www.mvcr.cz/archivy/evidence-nad/matriky}idPuvodce').text
    obce['umisteni'] = lokality[idPuvodce]
    book['obce'] = obce
    """

    od = m.find('.//{http://www.mvcr.cz/archivy/evidence-nad/matriky}rokMin').text
    do = m.find('.//{http://www.mvcr.cz/archivy/evidence-nad/matriky}rokMax').text
    od_do = {
      "od":od,
      "do":do
    }

    obsah = {}
    obsahXML = m.find('.//{http://www.mvcr.cz/archivy/evidence-nad/matriky}obsahMatriky').get('charakterObsahuMatriky')
    if obsahXML == 'I-N':
      obsah['INDEX Narozených'] = od_do
    elif obsahXML == 'I-Z':
      obsah['INDEX Zemřelých'] = od_do
    elif obsahXML == 'I-O':
      obsah['INDEX Oddaných'] = od_do
    elif obsahXML == 'N':
      obsah['Narození'] = od_do
    elif obsahXML == 'O':
      obsah['Oddaní'] = od_do
    elif obsahXML == 'Z':
      obsah['Zemřelí'] = od_do

    book['obsah'] = obsah

    # save just unique new books
    found = False
    for b in data['matriky']:
        if b['signatura'] == book['signatura']:
            found = True
            continue
    
    if not found:
      data['pocet']+=1
      data['matriky'].append(book)

with open('trebon.json','w',encoding='utf-8') as f:
    json.dump(data,f,indent=4,ensure_ascii=False)


'''
matriky = root.findall('.//{http://www.mvcr.cz/archivy/evidence-nad/matriky}matrika')
for m in matriky:
    print(list(m))
'''


