from lxml import etree
import json
import datetime

types = {
    'CATHOLICA': 'katolická',
    'MILITARIA': 'vojenská',
    'IUDAICA': 'židovská',
    'SAECULARA': 'civilní (matričního úřadu)',
    'EVANGELICA': 'evangelická',
    'MISCELLANEA': 'jiná'
}

def loadJSON(fn):
    with open(fn, 'r', encoding='utf-8') as f:
        j = json.load(f)

    return j

def find(data,txt):
    for d in data:
        if d['nazev'] == txt:
            return d

    return None

datetime_object = datetime.datetime.now()

ruian_obce = loadJSON('ruian/obce.json')
ruian_castiObci = loadJSON('ruian/castiObci.json')

tree = etree.parse("zao_matriky_2.xml")
root = tree.find('pomucka/kapitola')

# matriky
#data = root[0]

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

characters = []

out = {}
out['zdroj'] = 'zao'
out['vytvoreno'] = str(datetime_object)
out['vytvoreno_xml'] = tree.find('pomucka').attrib['cas-vytvoreni']
out['snimky_zaklad'] = 'http://images.archives.cz/mrimage/matriky/proxy/'
out['pocet'] = 0
out['matriky'] = []

fn = out['vytvoreno_xml'].split('T')[0].replace('-','') + '.json'

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
                #print(i.text)
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
            if s.attrib['nazev'] == 'indexProMatriky':
                matrika['indexProMatriky'] = []
                data = s.findall('matrika')
                for d in data:
                    matrika['indexProMatriky'].append(d.attrib['porCislo']) 
            if s.attrib['nazev'] == 'obsahy':
                matrika['obsah'] = {}
                data = s.findall('obsah')
                for d in data:
                    if d.attrib['charakter'] not in characters:
                        characters.append(d.attrib['charakter'])
                    if d.attrib['charakter'] == 'narozeni':
                        matrika['obsah']['Narození'] = parseMultivalueYear(d.attrib['casRozsah'])
                    elif d.attrib['charakter'] == 'snatky':
                        matrika['obsah']['Oddaní'] = parseMultivalueYear(d.attrib['casRozsah'])    
                    elif d.attrib['charakter'] == 'umrti':
                        matrika['obsah']['Zemřelí'] = parseMultivalueYear(d.attrib['casRozsah'])
                    elif d.attrib['charakter'] == 'indexNarozeni':
                        matrika['obsah']['INDEX Narozených'] = parseMultivalueYear(d.attrib['casRozsah'])
                    elif d.attrib['charakter'] == 'indexUmrti':
                        matrika['obsah']['INDEX Zemřelých'] = parseMultivalueYear(d.attrib['casRozsah'])
                    elif d.attrib['charakter'] == 'indexSnatku':
                        matrika['obsah']['INDEX Oddaných'] = parseMultivalueYear(d.attrib['casRozsah'])
            if s.attrib['nazev'] == 'propojLokality':
                matrika['obce'] = []
                
                lokality = s.findall('propojLokalita')

                for l in lokality:
                    obec = {}
                    elements = list(l)

                    for e in elements:
                        if e.tag == 'cas':
                           obec['casovyRozsah'] = parseMultivalueYear(e.text)
                        if e.tag == 'lokalita':
                            obec['umisteni'] = {}
                            obec['typ'] = ''
                            obec['varianty'] = []
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
                                    obec['typ'] = 'obec'
                                elif t.tag == 'castObce':
                                    obec['umisteni']['cast_obce'] = t.text
                                    obec['typ'] = 'castObce'
                                elif t.tag == 'varianta':
                                    polozka1 = t.find('obec')
                                    polozka2 = t.find('castObce')
                                    if polozka1 != None:
                                        obec['varianty'].append(polozka1.text)                                        
                                    if polozka2 != None:
                                        obec['varianty'].append(polozka2.text)
                    if obec['typ'] == 'obec':
                        obec['ruian'] = find(ruian_obce,obec['umisteni']['obec'])
                    elif obec['typ'] == 'castObce':
                        obec['ruian'] = find(ruian_castiObci, obec['umisteni']['cast_obce'] ) 



                    matrika['obce'].append(obec)
        
        if len(prilohy) != 0:
            matrika['snimky'] = []
            for p in prilohy:
                #print(p)
                snimek = {}
                snimek['url'] = p.attrib['rel-uri']
                attributes = p.findall('info/pole')
                for a in attributes:
                    if a.attrib['nazev'] == 'uid':
                        snimek['uid'] = a.text
                    elif a.attrib['nazev'] == 'create_date':
                        snimek['datum_vytvoreni'] = a.text
                    elif a.attrib['nazev'] == 'lastwrite_date':
                        snimek['datum_aktualizace'] = a.text
                matrika['snimky'].append(snimek)
        out['pocet'] += 1
        out['matriky'].append(matrika)

#print(characters)
#print(out['matriky'])

with open(fn,'w', encoding='utf-8') as f:
    json.dump(out, f, indent=2, ensure_ascii=False) 