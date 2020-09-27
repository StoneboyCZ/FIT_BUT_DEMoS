import os
import re

dn = 'html'
files = [f for f in os.listdir(dn) if os.path.isfile(os.path.join(dn,f))]
numberOfEntries = len(files)

signatury = {}
inv = []

for pn in range(1,numberOfEntries+1,1):
	fn = './'+dn+f'/{pn:05d}.html'
	htmlFile = open(fn, 'r',encoding='utf-8')
	content = htmlFile.read()

	signatura = re.findall(r'div class=\"labelFloat\">Signatura [^>]*[^<]*[^>]*>([^<]*)',content)
	invCislo = re.findall(r'div class=\"labelFloat\">Inventární [^>]*[^<]*[^>]*>([^<]*)',content)
	signatura = signatura[0]
	if signatura == '':
		print(f'Missing signature: {fn} - {signatura}')
	
	invCislo = invCislo[0]
	if invCislo == '':
		inv.append(fn)

	"""
	if invCislo not in inv:
		inv.append(invCislo)
	else:
		print(f'Duplicate inv. number {invCislo}')
	"""

	if signatura in signatury:
		signatury[signatura].append(fn)
	else:
		signatury[signatura] = []
		signatury[signatura].append(fn)

for i in inv:
	print(i)

for s in signatury:
	if len(signatury[s]) > 1:  
		print(f'{s} - {signatury[s]}')