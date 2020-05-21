import json

data = {}
with open('actapublica_ruian.json','r',encoding='utf-8') as f:
    data = json.load(f)

missing = []
matriky = data['matriky']
for m in matriky:
    obce = m['obce']
    for o in obce:
        if obce[o]['id'] == None:
            missing.append(m['puvodce']+'-'+o)

miss = set(missing)

with open('missing.txt','w',encoding='utf-8') as f: 
    for m in miss:
        f.write(m+'\n')