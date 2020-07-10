# http://docs.python-requests.org/en/master/user/quickstart/#cookies
# http://docs.python-requests.org/en/master/user/install/#install
# http://images.archives.cz/mrimage/matriky/proxy/cz/archives/CZ-217000010/NAD-165/dao/images/0345/8b1ef2b1-eba4-4b55-805d-f79d56afada0.jpg
# http://digi.archives.cz/da/Zoomify.action?entityRef=%28%5En%29%28%28%28localArchiv%2C%5En%2Chot_%29%28unidata%29%29%28338508%29%29&scanIndex=0

# I-N_I-Z_I-O_inv_c_124a_sig_Op_VII_13_1789-1799_Katerinky_025.jpg

import requests 
import random
import time
import re
import os
import math
import html

#from lxml import etree as ET

def getNextPage(s,content):
    nextPageMatches = re.findall(r'<div class=\"pageIco\">[^<]*<a href=\"([^\"]*)\"><i class=\"icon-forward3',content)
    #print('http://digi.archives.cz'+html.unescape(nextPageMatches[0]))
    r = s.get('http://digi.archives.cz'+html.unescape(nextPageMatches[0]),cookies=cookies)    
    content = r.text
    return content


from requests.adapters import HTTPAdapter
cookies = dict(
    JSESSIONID='FD0B5EA7B8D5CCB99F956E7130121202'
)

# creates a random number
#random.seed() 

s = requests.Session()


# create a session object
s.mount('http://digi.archives.cz', HTTPAdapter(max_retries=20))

# url to get -- TODO: first parameter of the script
url = 'http://digi.archives.cz/da/VysledekBean.action?show=&_sourcePage=J9iWHLkyp5z4HhNGlq9mM6oqvvkYA-alEcnabTkYvDuUufdZS6ayHaGqORKEQgWjvu_j1cA1cj_9xOZPuJLUy5_njHgRzedHY0K3t3M2Yb8%3D&pagerCompStateId=PAGER_RESULT&xid=be8358d0-f13c-102f-8255-0050568c0263&entityType=10041&paginatorCompStateId=PAGINATOR_RESULT&rowPg=0'

# download the webpage 
r = s.get(url,cookies=cookies)  
content = r.text


# number of entries
#matches = re.findall(r'Celkem[^:]*:[^\d]*([^<]*)',content)
#print(matches[0].strip())
#numberOfEntries = int(matches[0].strip().replace(' ',''))
numberOfEntries = 12565 


dn = 'html'
skip = False
if not len(os.listdir(dn)) == numberOfEntries: # not all HTMLs are downloaded
    skipIndex = 1
    for n in range(1,numberOfEntries+1,1):
        fn = './'+dn+f'/{n:05d}.html'

        if os.path.isfile(fn): # skip 
            skip = True
            print(f'Skipping: {fn}')
            skipIndex = n
            #content = getNextPage(s,content)
        else: # new file
            print(fn)
            if skip:
                # http://digi.archives.cz/da/PaginatorResult.action?rowTxt=100&_sourcePage=bKkSO0TO8RtI9RGPJPEB93qDqgiP3YIQgQwie3n9TJ9BZE3FphATgqDTR617KAFT8FB3j2wSKX57ZGWxGNct5rNv1LLCCOG4yp8lVlYDwNI%3D&__fp=MPjVUQf3i5IFDRc3twy2vUXNFwiB6s6MM4DjAFqfs-DngYMZtHs3-mkw002DWqEt
                # http://digi.archives.cz/da/PaginatorResult.action?rowTxt=11492&_sourcePage=EZK_5C4HIqBn7-K-DY9IMaGW1utfeadQ6TliuekchMQQAADoWtW9Z9Cj5bh3uclGhR73lbNOZathrY7sKJ3yjMLYxtfFNy7P35SnGcxDyPU%3D&__fp=fSaqZKzFoJmTJONsGzZYi-j-Xrlla5xKz1C1IR9qiRsd0xeSepWZjI7XP4d6_0Nv
                url = 'http://digi.archives.cz/da/PaginatorResult.action?rowTxt='+str(skipIndex+1)+'&_sourcePage=EZK_5C4HIqBn7-K-DY9IMaGW1utfeadQ6TliuekchMQQAADoWtW9Z9Cj5bh3uclGhR73lbNOZathrY7sKJ3yjMLYxtfFNy7P35SnGcxDyPU%3D&__fp=fSaqZKzFoJmTJONsGzZYi-j-Xrlla5xKz1C1IR9qiRsd0xeSepWZjI7XP4d6_0Nv'
                r = s.get(url,cookies=cookies)  
                content = r.text
                skip = False

            with open(fn,'w',encoding="utf-8") as f:
                #content = getNextPage(s,content)
                snimky = re.findall(r'<div class="imageBlock">\s+<a href="([^"]*)"',content)

                if len(snimky) != 0:
                    fn_images = './'+dn+f'/images/{n:05d}_images.html'
                    r = s.get('http://digi.archives.cz'+html.unescape(snimky[0]),cookies=cookies)    
                    content_images = r.text

                    with open(fn_images,'w',encoding="utf-8") as fi:
                        fi.write(content_images)


                f.write(content)
                #time.sleep(2)
                content = getNextPage(s,content)

                
