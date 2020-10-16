import os
import re

dn = 'html'
files = [f for f in os.listdir(dn) if os.path.isfile(os.path.join(dn,f))]
numberOfEntries = len(files)

signatury = []

for pn in range(1,numberOfEntries+1,1):
    fn = './'+dn+f'/{pn:05d}.html'
    htmlFile = open(fn, 'r',encoding='utf-8')
    content = htmlFile.read()

    signatura = re.findall(r'div class=\"labelFloat\">Signatura:[^>]*[^<]*[^>]*>([^<]*)',content)
    if len(signatura) != 1:
        print(f'{fn} - {signatura}')
    
    if signatura not in signatury:
        signatury.append(signatura)
    else:
        print(f'Duplicate signature {signatura}, file {fn}')
    
