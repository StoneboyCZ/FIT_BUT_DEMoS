import requests 
import random
import time
import re
import os
import math
import html

page = 'http://vademecum.soalitomerice.cz'

from requests.adapters import HTTPAdapter
cookies = dict(
    JSESSIONID='84CFF0821477E292D04263477CDC1AE6'
)

s = requests.Session()


# create a session object
s.mount(page, HTTPAdapter(max_retries=20))


dn = 'html/images'

for e in os.listdir(dn):
    path = os.path.join(dn, e)
    #print(f'path:{path}')
    #print(f'e:{e}')
    ddn = e.split('.')[0].split('_')[0]
    #print(ddn) 
    #print(path)
    # filter files
    if not os.path.isdir(path):
        with open(path, "r",encoding="utf-8") as f:
            # get the number of images
            # read the content of image html file
            content = f.read()

            n = int(re.findall(r'<div class="pageNum">[^|]+\|.([\d]*)',content)[0])    
            #url = re.findall(r'<div class="pageNum">[^|]+\|.([\d]*)',content)[0]        
            perm = re.findall(r'<a class="text headline" href="([^"]*)',content)[0]
            p = os.path.join(dn,ddn)
            print(p)
            for i in range(1,n+1,1):
                fn=f'{i:03d}.html'
                
                if i==1:
                    with open(p+'/'+fn,'w',encoding='utf-8') as ff:
                        ff.write(content)
                else:
                    print(url)
                    r = s.get(url,cookies=cookies)

                    content = r.text
                    
                    with open(p+'/'+fn,'w',encoding='utf-8') as ff:
                        ff.write(content)
                
                ii = i+1
                url = perm+'&scan='+str(ii)
                
                                

              
"""
for fn in os.listdir(dn):
    dm = fn.split('.')[0].split('_')[0]
    # make directory for the image files, if it doesn´t exist
    d = dn+'/'+dm
    if not os.path.isdir(d):
        os.mkdir(d)
    
    print(fn)
    print(dm)
    with open(dn+'/'+fn, "r",encoding="utf-8") as f:
        # get the number of images
        # read the content of image html file
        content = f.read()

        n = int(re.findall(r'<div class="pageNum">[^|]+\|.([\d]*)',content)[0])    
        
        print(n)  

"""