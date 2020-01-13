import os
import hashlib

base = 'g:/ACTAPUBLICA'
subdirectories = [f.path for f in os.scandir(base) if f.is_dir() and '_' not in f.name ]  

for directory in subdirectories:
    print(directory)
    filenames = os.listdir(directory)

    ### get hash of files in directory
    hashes = {}
    for filename in filenames:

        with open(directory+'/'+filename, 'rb') as inputfile:
            data = inputfile.read()
            h = hashlib.md5(data).hexdigest()
            if h not in hashes:
                hashes[h] = []

            hashes[h].append(directory+'\\'+filename)

    signature = directory.split('\\')[-1]
    dupdn = base+'/_dup/'+signature+'/'
    for h in hashes:
        if len(hashes[h]) != 1: # if we have multiple same files in the directory 
            print(h)
            if not os.path.isdir(dupdn):
                print(dupdn)
                os.mkdir(dupdn)
            fn = hashes[h][0].split('\\')[-1]
            os.rename(hashes[h][0],dupdn+fn)
    print('====')
  
    
"""

directory = base+'/1/'
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

print(os.path.dirname(directory).split('/')[-1])

## create a directory for duplicate files 
#os.mkdir(base+'/dup')

### delete duplicate files
"""
"""
for h in hashes:
    if len(hashes[h]) != 1: # if we have multiple same files in the directory 
        os.remove(hashes[h][0])

### rename files

filenames = os.listdir(directory)

for f in filenames: 
    if '-' not in f:
        os.rename(directory+'/'+f, directory+'/'+ )
"""
