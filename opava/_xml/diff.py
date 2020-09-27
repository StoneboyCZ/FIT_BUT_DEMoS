import json
import datetime

fn_orig = '20200625.json'
fn_new = '20200725.json'

def importJSON(fn):
    with open(fn,'r', encoding='utf-8') as f:
        data = json.load(f)    

        return data

def stringToDate(s):
    date = None

    if s != None:
        date = datetime.datetime.strptime(s.split(' ')[0],'%Y-%m-%d')
    else:
        date = orig_date    

    return date

orig = importJSON(fn_orig)
orig_date = datetime.datetime.strptime(orig['vytvoreno_xml'].split('T')[0],'%Y-%m-%d')   
#print(orig['vytvoreno_xml'])
#print(orig_date)
new = importJSON(fn_new)

update = {}
update['pocet_nove'] = 0
update['pocet_aktualizovane'] = 0
update['pocet_aktualizovane_prilohy'] = 0
update['matriky_nove'] = []
update['matriky_aktualizovane'] = []
update['matriky_aktualizovane_prilohy'] = []

#print(new['matriky'][0])

for m in new['matriky']:
    #print(f"{m['datum_vytvoreni']} {m['datum_aktualizace']} {m['datum_aktualizace_prilohy']}")
    if stringToDate(m['datum_vytvoreni']) > orig_date:
        #print('new')
        update['pocet_nove']+=1
        update['matriky_nove'].append(m)
    
    if stringToDate(m['datum_aktualizace']) > orig_date:
        #print('update')
        update['pocet_aktualizovane']+=1
        update['matriky_aktualizovane'].append(m)        
    
    if stringToDate(m['datum_aktualizace_prilohy']) > orig_date:
        #print('update_ext')
        update['pocet_aktualizovane_prilohy']+=1
        update['matriky_aktualizovane_prilohy'].append(m) 

with open('update.json','w',encoding='utf-8') as f:
    json.dump(update, f, ensure_ascii=False, indent=2)