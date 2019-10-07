# http://docs.python-requests.org/en/master/user/quickstart/#cookies
# http://docs.python-requests.org/en/master/user/install/#install
# http://actapublica.eu/brno/77/cut/77-004-1-1.png

import requests 
import random
import time
import re
import os

cookies = dict(
    PHPSESSID='2i7nugtblavchjklt1es0077h0',
    __utma='§203544448.705625239.1570457305.1570457305.1570457305.1',
    __utmc='203544448',
    __utmz='203544448.1570457305.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
    __utmt='1',
    __utmb='203544448.37.9.1570458437834'
)

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'cs-CZ,cs;q=0.9,en;q=0.8,en-US;q=0.7',
    'Cache-Control': 'max-age=0',
    'Host': 'actapublica.eu',
    'Proxy-Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
    'Referer': 'http://actapulica.eu/hledej/'
    }

f = range(4401,4407,1) # 4401 - 4406

# creates a random number
random.seed() 

s = requests.Session()

# create a session object
#s.mount('http://actapublica.eu', HTTPAdapter(max_retries=20))

url = 'http://actapublica.eu'

# download the webpage 
r = s.get(url,headers=headers,cookies=cookies)    
content = r.text

print(content)

# how many pages do we need to process? Two matches, same number
matches = re.findall(r'Přejít na stranu číslo [^>]*> z celkem (\d*)',content)
print(matches)
numOfPages = matches[0]

for pn in range(1,int(numOfPages)+1,1):
    if pn != 1: # first page doesnt have to be downloaded again
        url = 'http://actapublica.eu/matriky/brno/?pg='+str(pn)
        r = s.get(url,cookies=cookies)    
        content = r.text

    print("Downloading page " + str(pn))
    print("========================")

    # find all rows on the page
    matchesAdress = re.findall(r'<td class=\"row1\"><a href=\"http://([^/]*)/([^/]*)/([^/]*)/([^/]*)/([^/]*).\" title=\"([^\"]*)',content)
    print(matchesAdress)

    # get the number of pages <td class=\"row1\">(\d*)</td>
    matchesNumberOfPages = re.findall(r'<td class=\"row1\">(\d*)</td>',content)
    #print(matchesNumberOfPages)

    # remove empty
    matchesAdress = list(filter(None, matchesAdress))
    matchesNumberOfPages = list(filter(None, matchesNumberOfPages))
         
    for adress,numberOfPages in zip(matchesAdress,matchesNumberOfPages):
        if f in matchesAdress[5]:
            #sleepTime = 1
            print(adress)
            print(numberOfPages)

            dn = "./"+adress[5]

            # make the appropriate directory to save images
            if not os.path.exists(dn):
                os.makedirs(dn)

            # check if the directory contains all files, if yes, can be skipped
            if not len(os.listdir(dn)) == adress[5]:
                if int(numberOfPages) > 0:
                    for n in range(1,int(numberOfPages)+1,1):
                        index='{num:03d}'.format(num=n)
                        fn="./"+adress[5]+"/"+index+".png"

                        if not os.path.isfile(fn): # skip the existing
                            sleepTime = random.gauss(10, 2)
                            #sleepTime = random.randrange(10)
                            url = "http://"+adress[0]+"/"+adress[2]+"/"+adress[5]+"/cut/"+adress[5]+"-"+index+"-1-1.png"
                            # request the file
                            print(url)

                            r = s.get(url,cookies=cookies)  
                        
                            # save the result
                            im = open(fn,"wb")
                            
                            im.write(r.content)
                            im.close()
                            time.sleep(sleepTime)     



'''
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

'''