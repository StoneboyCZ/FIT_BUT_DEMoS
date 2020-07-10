import json

data = {}
data['zdroj'] = 'opava'
data['matriky'] = []

files = [
    'zao/opava-zao.json',
    'zaool/opava-zaool.json'
]  

for fn in files:
    with open(fn,'r',encoding='utf-8') as f:
        data['matriky'] = data['matriky'] + json.load(f)['matriky']

with open('opava.json','w',encoding='utf-8') as f:
    json.dump(data,f,indent=4,ensure_ascii=False)