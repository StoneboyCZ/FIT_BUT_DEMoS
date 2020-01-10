import os
import hashlib

directory = 'd:/tmp/acta/1'
filenames = os.listdir(directory)

### get hash of files in directory
hashes = {}
for filename in filenames:

    with open(directory+'/'+filename, 'rb') as inputfile:
        data = inputfile.read()
        h = hashlib.md5(data).hexdigest()
        if h not in hashes:
            hashes[h] = []

        hashes[h].append(directory+'/'+filename)

### delete duplicate files
for h in hashes:
    if len(hashes[h]) != 1: # if we have multiple same files in the directory 
        os.remove(hashes[h][0])

### rename files
filenames = os.listdir(directory)

for f in filenames: 
    if '-' not in f:
        os.rename(directory+'/'+f, directory+'/'+ )

"""
for h in hashes:
    if h['hash'] in unique:

    else: 
        unique.append(h['hash'])        

"""