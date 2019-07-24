# O_sig_146_21_1881-1926_Krasny_Les_001
# O • sig. 146/21 • 1881 - 1926 • Krásný Les

import requests 
import random
import time
import re
import os
import math
import html
import json

page = 'http://vademecum.soalitomerice.cz'

from requests.adapters import HTTPAdapter
cookies = dict(
    JSESSIONID='1111EF3ADF4F6E00D5C34784AF19E3D2'
)

s = requests.Session()


# create a session object
s.mount(page, HTTPAdapter(max_retries=20))

dn = 'html/images'

# image base adress
base='http://images.soalitomerice.cz/mrimage/matriky/proxy/cz/archives/'

for f in os.listdir(dn):
    
    ofn = f.split('.')[0]+'.json' # output file name
    
    if not os.path.exists(dn+'/json/'+ofn):
        print(f)
        with open(dn+'/'+f,'r',encoding='utf-8') as html:
            content = html.read()
            # permanent link
            perm = re.findall(r'<a class="text headline" href="([^"]*)',content)[0]

            # get the overall number of images
            n = int(re.findall(r'<div class="pageNum">[^|]+\|.([\d]*)',content)[0])    
                
            # how many pages do we have to download?
            np = int(re.findall(r'<div class="pageNum">[^-]*-\s*([\d]*)',content)[0]) # number of images on one page
            p = int(n / np)
            #print(p)

            with open(dn+'/json/'+ofn,'w',encoding='utf-8') as of:
                snimky = {}
                
                jm = re.findall(r'<a class="text headline" .*?(?=title)title="([^"]*)',content)[0]
                jm = jm.replace(' • ','_')
                jm = jm.replace('. ','_')
                jm = jm.replace('/','_')
                jm = jm.replace(' - ','-')
                jm = jm.replace(' ','_')
                
                snimky['jmeno'] = jm
                snimky['url'] = []        

                # save all image adresses into file
                for i in range(1,p+2,1):
                    imgs = re.findall(r'<img src=\'.*?(?=nahled_maly)',content)

                    for im in imgs:
                        sp = im.split('/')
                        n = base+sp[8]+'/'+sp[9]+'/'+sp[10]+'/'+sp[11]+'/'+sp[12]+'/'+sp[13]
                        snimky['url'].append(n)        

                    # when all images from the predownloaded HTML are proccessed, get the next one
                    ni = np * i + 1
                    #print(ni)
                    url = perm+'&scan='+str(ni)                 
                    r = s.get(url,cookies=cookies)
                    content = r.text
                
                # save the images, move to the next file
                json.dump(snimky,of,indent=4,ensure_ascii=False)
    else:
        print(f'Skipping {f}')

    """
    if not os.path.isdir(path):
        with open(path, "r",encoding="utf-8") as f:
            #print(dn)
            #print(e)
            #print(ddn)
            # get the number of images
            # read the content of image html file
            content = f.read()

            # get the overall number of images
            n = int(re.findall(r'<div class="pageNum">[^|]+\|.([\d]*)',content)[0])    
            
            # how many pages do we have to download?
            np = int(re.findall(r'<div class="pageNum">[^-]*-\s*([\d]*)',content)[0])
            p = int(n / np)
            
            # image base adress
            base='http://images.soalitomerice.cz/mrimage/matriky/proxy/cz/archives/'

            with open(dn+'/'+ddn+'/'+'snimky.json','w',encoding='utf-8') as f:
                snimky = {}
                jm = re.findall(r'<a class="text headline" .*?(?=title)title="([^"]*)',content)[0]
                jm = jm.replace(' • ','_')
                jm = jm.replace('. ','_')
                jm = jm.replace('/','_')
                jm = jm.replace(' - ','-')
                jm = jm.replace(' ','_')
                snimky['jmeno'] = jm
                snimky['url'] = []

                for i in range(1,p+1,1):
                    print(p)
                    # image adresses
                    imgs = re.findall(r'<img src=\'.*?(?=nahled_maly)',content)
                    for im in imgs:
                        sp = im.split('/')
                        n = base+sp[8]+'/'+sp[9]+'/'+sp[10]+'/'+sp[11]+'/'+sp[12]+'/'+sp[13]
                        snimky['url'].append(n)

                    # when all adresses are processed and downloaded, download the next page
                    ni = np * i + 1
                    perm = re.findall(r'<a class="text headline" href="([^"]*)',content)[0]
                    url = perm+'&scan='+str(ni)                 
                    r = s.get(url,cookies=cookies)
                    content = r.text
            
                json.dump(snimky,f)

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
                                

