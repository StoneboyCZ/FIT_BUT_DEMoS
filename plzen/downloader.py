# http://docs.python-requests.org/en/master/user/quickstart/#cookies
# http://docs.python-requests.org/en/master/user/install/#install
# http://www.portafontium.eu/searching/register?field_archives=213000010&search_api_aggregation_2=&field_doc_place_field_doc_place_name=&search_api_views_fulltext=&field_register_type%5B%5D=register-birth&field_register_type%5B%5D=register-marriage&field_register_type%5B%5D=register-death&field_register_type%5B%5D=index-birth&field_register_type%5B%5D=index-marriage&field_register_type%5B%5D=index-death&search_api_aggregation_3=&field_doc_dates_field_doc_dates_from=
#http://www.portafontium.eu/searching/register?search_api_aggregation_2=&field_doc_place_field_doc_place_name=&search_api_views_fulltext=&search_api_aggregation_3=&field_doc_dates_field_doc_dates_from=&field_archives=213000010&field_register_type%5B0%5D=register-birth&field_register_type%5B1%5D=register-marriage&field_register_type%5B2%5D=register-death&field_register_type%5B3%5D=index-birth&field_register_type%5B4%5D=index-marriage&field_register_type%5B5%5D=index-death&page=1 


import requests 
import re
import os
import datetime

page = 'http://www.portafontium.eu'


from requests.adapters import HTTPAdapter

s = requests.Session()


# create a session object
s.mount(page, HTTPAdapter(max_retries=20))

# url to get -- TODO: first parameter of the script
url = 'http://portafontium.eu/searching/register?field_archives=213000010&search_api_views_fulltext=&search_api_views_fulltext_1=&search_api_views_fulltext_2=&field_register_type%5B0%5D=register-birth&field_register_type%5B1%5D=register-marriage&field_register_type%5B2%5D=register-death&field_register_type%5B3%5D=index-birth&field_register_type%5B4%5D=index-marriage&field_register_type%5B5%5D=index-death&search_api_aggregation_3=&field_doc_dates_field_doc_dates_from=&page=0'

# number of entries
#matches = re.findall(r'Celkem[^:]*:[^\d]*([^<]*)',content)
#print(matches[0].strip())
#numberOfEntries = int(matches[0].strip().replace(' ',''))
numberOfPages = 323
#numberOfEntries = 12712  


index = 0 # html index to download
dn = 'html'
skip = False

if not os.path.isdir('html'):
    os.mkdir('html')
if not os.path.isdir('html/images'):
    os.mkdir('html/images')

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


with open('info.json','w',encoding='utf-8') as f:
    info = {}
    info['downloaded'] = str(datetime.datetime.now())
    json.dump(info,f,ensure_ascii=False)