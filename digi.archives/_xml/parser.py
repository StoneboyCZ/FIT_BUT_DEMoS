from lxml import etree
import json

types = {
    'CATHOLICA': 'katolická',
    'MILITARIA': 'vojenská',
    'IUDAICA': 'židovská',
    'SAECULARA': 'civilní (matričního úřadu)',
    'EVANGELICA': 'evangelická',
    'MISCELLANEA': 'jiná'
}


tree = etree.parse("zao_matriky.xml")
root = tree.find('pomucka/kapitola')

# matriky
#data = root[0]

""" types = []
test = tree.findall('.//pole[@nazev="typyMatriky"]')
for t in test:
    arr = []
    #if type(t.text) != str:
    #    print(type(t.text))

    if type(t.text) != str:
        continue
    elif ',' in t.text:
        arr = t.text.split(',')
        arr = list(map(str.strip,arr))
    else:
        arr.append(t.text)
    
    for a in arr:
        if a not in types:
            types.append(a) 

print(types)
"""

def parseMultivalue(text):
    seznam = []
    if type(text) != str or len(text) == 0:
        return None
    elif ',' in text:
        seznam = text.split(',')
        seznam = list(map(str.strip,seznam))
    else:
        seznam.append(text)
    
    return seznam

def parseMultivalueYear(text):
    d = {}
    if type(text) != str or len(text) == 0:
        return None
    elif '-' in text:
        seznam = list(map(str.strip,text.split('-')))
        d['od'] = seznam[0]
        d['do'] = seznam[1]    
    else:
        d['od'] = text
        d['do'] = text
    
    return d

out = {}
out['zdroj'] = 'zao'
out['pocet'] = 0
out['matriky'] = []

# kapitoly
data = list(root)

for ch in data:
    matriky = ch.findall('zaznam')
    for m in matriky:
        matrika = {}        

        informace = m.findall('pole')
        subdata = m.findall('subdata')
        prilohy = m.findall('priloha')

        matrika['casovyRozsah'] = {}

        for i in informace:
            if i.attrib['nazev'] == 'uid':
                matrika['uid'] = i.text
            elif i.attrib['nazev'] == 'cnad':
                matrika['cnad'] = i.text     
            elif i.attrib['nazev'] == 'porCislo':
                matrika['porCislo'] = i.text
            elif i.attrib['nazev'] == 'signArch':
                matrika['signatura_archivu'] = i.text
            elif i.attrib['nazev'] == 'signPuv':
                matrika['signatura_puvodce'] = i.text
            elif i.attrib['nazev'] == 'invCislo':
                print(i.text)
                matrika['invCislo'] = i.text
            elif i.attrib['nazev'] == 'casRozsahMin':
                matrika['casovyRozsah']['min'] = i.text
            elif i.attrib['nazev'] == 'casRozsahMax':
                matrika['casovyRozsah']['max'] = i.text
            elif i.attrib['nazev'] == 'uzemniRozsah':
                matrika['obce_seznam'] = parseMultivalue(i.text)
            elif i.attrib['nazev'] == 'uzemniRozsahPuvodni':
                matrika['obce_seznam_puvodni'] = parseMultivalue(i.text)
            elif i.attrib['nazev'] == 'jazyky':
                matrika['jazyky'] =  parseMultivalue(i.text)                
            elif i.attrib['nazev'] == 'poznamka':
                matrika['poznamka'] = i.text
            elif i.attrib['nazev'] == 'create_date':
                matrika['datum_vytvoreni'] = i.text
            elif i.attrib['nazev'] == 'lastwrite_date':
                matrika['datum_aktualizace'] = i.text
            elif i.attrib['nazev'] == 'lastwrite_date_ext':
                matrika['datum_aktualizace_prilohy'] = i.text

        for s in subdata:
            if s.attrib['nazev'] == 'obsahy':
                matrika['obsah'] = {}
                data = s.findall('obsah')
                for d in data:
                    if d.attrib['charakter'] == 'narozeni':
                        matrika['obsah']['Narození'] = parseMultivalueYear(d.attrib['casRozsah'])
                    elif d.attrib['charakter'] == 'snatky':
                        matrika['obsah']['Oddaní'] = parseMultivalueYear(d.attrib['casRozsah'])    
                    elif d.attrib['charakter'] == 'umrti':
                        matrika['obsah']['Zemřelí'] = parseMultivalueYear(d.attrib['casRozsah']) 
            if s.attrib['nazev'] == 'propojLokality':
                matrika['obce'] = []
                
                lokality = s.findall('propojLokalita')

                for l in lokality:
                    obec = {}
                    elements = list(l)

                    for e in elements:
                        if e.tag == 'cas':
                           print(e.text)
                           obec = parseMultivalueYear(e.text)
                        if e.tag == 'lokalita':
                            obec['umisteni'] = {}
                            for t in list(e):
                                #print(t.tag)
                                if t.tag == 'stat':
                                    obec['umisteni']['stat'] = t.text
                                elif t.tag == 'kraj':
                                    obec['umisteni']['kraj'] = t.text
                                elif t.tag == 'okres':
                                    obec['umisteni']['okres'] = t.text
                                elif t.tag == 'obec':
                                    obec['umisteni']['obec'] = t.text
                                elif t.tag == 'castObce':
                                    obec['umisteni']['cast_obce'] = t.text
                            print(obec)
                    matrika['obce'].append(obec)




        out['matriky'].append(matrika)

print(out['matriky'])