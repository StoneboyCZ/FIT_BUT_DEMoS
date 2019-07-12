# http://docs.python-requests.org/en/master/user/quickstart/#cookies
# http://docs.python-requests.org/en/master/user/install/#install
# http://www.portafontium.eu/searching/register?field_archives=213000010&search_api_aggregation_2=&field_doc_place_field_doc_place_name=&search_api_views_fulltext=&field_register_type%5B%5D=register-birth&field_register_type%5B%5D=register-marriage&field_register_type%5B%5D=register-death&field_register_type%5B%5D=index-birth&field_register_type%5B%5D=index-marriage&field_register_type%5B%5D=index-death&search_api_aggregation_3=&field_doc_dates_field_doc_dates_from=
#http://www.portafontium.eu/searching/register?search_api_aggregation_2=&field_doc_place_field_doc_place_name=&search_api_views_fulltext=&search_api_aggregation_3=&field_doc_dates_field_doc_dates_from=&field_archives=213000010&field_register_type%5B0%5D=register-birth&field_register_type%5B1%5D=register-marriage&field_register_type%5B2%5D=register-death&field_register_type%5B3%5D=index-birth&field_register_type%5B4%5D=index-marriage&field_register_type%5B5%5D=index-death&page=1 


import requests 
import random
import time
import re
import os
import math
import html

page = 'http://www.portafontium.eu'


def getNextPage(s,n):
    #nextPageMatches = re.findall(r'<div class=\"pageIco\">[^<]*<a href=\"([^\"]*)\"><i class=\"icon-forward3',content)
    #print('http://digi.archives.cz'+html.unescape(nextPageMatches[0]))
    url = 'http://vademecum.soalitomerice.cz/vademecum/VysledekBean.action?show=&_sourcePage=-TmQel2F93rn942T12DAF5Gbin71etvUHOrfCAM_YumJvj1SrzdaYDKTYoE5_LZScHm50gBE9NkRjdl8pajpKLEr7JaFtqDP6tmkqQrZ4Lk%3D&pagerCompStateId=PAGER_RESULT&xid=09ddd7cea03b9b8d%3A30bdd2c7%3A1201ea2ef5b%3A-7e0b&entityType=10041&paginatorCompStateId=PAGINATOR_RESULT&rowPg='+str(n)
    r = s.get(url,cookies=cookies)    
    content = r.text
    return content


from requests.adapters import HTTPAdapter
#cookies = dict(
#    JSESSIONID='F660C59835309383AEA1E19AF7B8C5A5'
#)

# creates a random number
#random.seed() 


s = requests.Session()


# create a session object
s.mount(page, HTTPAdapter(max_retries=20))

# url to get -- TODO: first parameter of the script
url = 'http://www.portafontium.eu/searching/register?search_api_aggregation_2=&field_doc_place_field_doc_place_name=&search_api_views_fulltext=&search_api_aggregation_3=&field_doc_dates_field_doc_dates_from=&field_register_type%5B0%5D=register-birth&field_register_type%5B1%5D=register-marriage&field_register_type%5B2%5D=register-death&field_register_type%5B3%5D=index-birth&field_register_type%5B4%5D=index-marriage&field_register_type%5B5%5D=index-death&field_archives=213000010&page=0'

# number of entries
#matches = re.findall(r'Celkem[^:]*:[^\d]*([^<]*)',content)
#print(matches[0].strip())
#numberOfEntries = int(matches[0].strip().replace(' ',''))
numberOfPages = 318
#numberOfEntries = 12712  

index = 0 # html index to download
dn = 'html'
skip = False
for p in range(1, numberOfPages+1,1):
    # download the webpage 
    r = s.get(url)  
    content = r.text

    # get the htmls
    #htmls = re.findall(r'<tr.*?(?=<a)<a href="([^"]*)',content,re.DOTALL)
    htmls = re.findall(r'<tr\s* class.*?(?=<a)<a href="([^"]*).*?(?=iip)iipimage/([0-9]*)',content,re.DOTALL)

    for h in htmls:
        bookUrl=page+h[0]
        imageUrl=page+'/iipimage/'+h[1]
        print(bookUrl)
        print(imageUrl)
        
        
        index = index + 1 # the current book index
        fn = './'+dn+f'/{index:05d}.html'
        ifn = './'+dn+'/images/'+f'{index:05d}.html'

        # does book have images
        print(bookUrl)
        r = s.get(bookUrl)  
        
        with open(fn,'w',encoding='utf-8') as hf:
            hf.write(r.text)
        
        r = s.get(imageUrl)
        with open(ifn,'w',encoding='utf-8') as imf:
            imf.write(r.text)
        

    url = 'http://www.portafontium.eu/searching/register?search_api_aggregation_2=&field_doc_place_field_doc_place_name=&search_api_views_fulltext=&search_api_aggregation_3=&field_doc_dates_field_doc_dates_from=&field_register_type%5B0%5D=register-birth&field_register_type%5B1%5D=register-marriage&field_register_type%5B2%5D=register-death&field_register_type%5B3%5D=index-birth&field_register_type%5B4%5D=index-marriage&field_register_type%5B5%5D=index-death&field_archives=213000010&page='+str(p)
"""
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
                url = 'http://vademecum.soalitomerice.cz/vademecum/VysledekBean.action?show=&_sourcePage=-TmQel2F93rn942T12DAF5Gbin71etvUHOrfCAM_YumJvj1SrzdaYDKTYoE5_LZScHm50gBE9NkRjdl8pajpKLEr7JaFtqDP6tmkqQrZ4Lk%3D&pagerCompStateId=PAGER_RESULT&xid=09ddd7cea03b9b8d%3A30bdd2c7%3A1201ea2ef5b%3A-7e0b&entityType=10041&paginatorCompStateId=PAGINATOR_RESULT&rowPg='+str(skipIndex-1)
                r = s.get(url)  
                content = r.text
                skip = False

            with open(fn,'w',encoding="utf-8") as f:
                #content = getNextPage(s,content)
                snimky = re.findall(r'<div class="imageBlock">\s+<a href="([^"]*)"',content)

                if len(snimky) != 0:
                    fn_images = './'+dn+f'/images/{n:05d}_images.html'
                    r = s.get(page+html.unescape(snimky[0]),cookies=cookies)    
                    content_images = r.text

                    with open(fn_images,'w',encoding="utf-8") as fi:
                        fi.write(content_images)


                f.write(content)
                #time.sleep(2)
                content = getNextPage(s,n)

                
"""