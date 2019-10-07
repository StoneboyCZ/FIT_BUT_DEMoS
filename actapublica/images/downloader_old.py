# http://docs.python-requests.org/en/master/user/quickstart/#cookies
# http://docs.python-requests.org/en/master/user/install/#install
# http://actapublica.eu/brno/77/cut/77-004-1-1.png

import requests 
import random
import time
import re
import os

cookies = dict(
    PHPSESSID='drnlbh1g7h572hfdp6a4957696',
    __utmc='203544448',
    __utma='203544448.1704102175.1525090029.1525106600.1525157810.4',
    __utmz='203544448.1525090029.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
    __utmt='1',
    __utmb='203544448.12.10.1525157810'
    )

# creates a random number
random.seed() 

# create a session object
s = requests.Session()

# url to get (Krtiny) -- TODO: first parameter of the script
url = 'http://actapublica.eu/puvodci/lokality/78/'

# download the webpage 
r = s.get(url,cookies=cookies)    
content = r.text

# search the content of the webpage and find the appropriate data
# <td class=\"row1\"><a href=\"http://([^/]*)/([^/]*)/([^/]*)/([^/]*)/([^/]*).\" title=\"([^/]\d*)\"
matches1 = re.findall(r'<td class=\"row1\"><a href=\"http://([^/]*)/([^/]*)/([^/]*)/([^/]*)/([^/]*).\" title=\"([^/]\d*)\"',content)
matches2 = re.findall(r'<td class=\"row1\">(\d*)',content)
print(matches1)

# remove empty elements
matches2 = list(filter(None, matches2)) 
print(matches2)

# download all image data
for book,pages in zip(matches1,matches2):
    print(book)
    print(pages)
    #download the appropriate image page
    images="http://"+"/"+book[0]+"/"+book[1]+"/"+book[2]+"/prohlizec/"+book[4]+"/"
    print(images)

    dn = "./"+book[5]

    # make the appropriate directory to save images
    if not os.path.exists(dn):
        os.makedirs(dn)

    # check if the directory contains all files, if yes, can be skipped
    if not len(os.listdir(dn)) == int(book[5]):
        # download the images
        for n in range(1,int(pages)+1,1):
            index='{num:03d}'.format(num=n)
            fn="./"+book[5]+"/"+index+".png" 
            
            if not os.path.isfile(fn): # skip the existing
                sleepTime = random.gauss(20, 3)
                link="http://"+book[0]+"/"+book[2]+"/"+book[5]+"/cut/"+book[5]+"-"+index+"-1-1.png"
                print(link)

                # request the file
                r = s.get(link,cookies=cookies)  
                    
                # save the result
                im = open(fn,"wb")
                im.write(r.content)
                im.close()
                    
                time.sleep(sleepTime) 

