import os
import re
import json

matriky = []
with open('opava.json','r',encoding='utf-8') as f:
	matriky = json.load(f)['matriky']

signatury = {}

for i,m in enumerate(matriky):

	signatura = m['signatura']
	
	if signatura in signatury:
		signatury[signatura].append(i)
	else:
		signatury[signatura] = []
		signatury[signatura].append(i)

for s in signatury:
	if len(signatury[s]) > 1:  
		print(f'{s} - {signatury[s]}')