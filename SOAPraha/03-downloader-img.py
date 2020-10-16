import requests 
import re
import os
import json

# base url
base = 'http://ebadatelna.soapraha.cz/pages/DataMatrikaPage/matrikaId/'

# get indexes that we will use in links
dn_info = 'html/info'
ids = [f.replace('.html', '') for f in os.listdir(dn_info) if os.path.isfile(os.path.join(dn_info,f))]

json_img = 'html/info/json'

if not os.path.isdir(json_img):
    os.mkdir('./'+json_img)

for i in ids:
    print(i)
    url = base+i
    r = requests.get(url)
    content = r.text

    if 'Kniha není digitalizována' in content:
        continue

    numberOfImages = int(re.findall(r'<a class="pageNumber" href="javascript:;" [^>]*><span>([^<]*)',content)[0])
    jmeno = re.findall(r'<a class="manipulationButton" target="_blank" href="([^"]*)',content,re.DOTALL)[0].split('/')
    jp = jmeno[6].split('_')

    imageName = ''
    for idx, j in enumerate(jp):
        #print(f'index: {idx}')
        if len(jp)-1 == idx:
            imageName = imageName + '_'
            break

        if idx == 0:
            imageName = imageName + j
        else:
            imageName = imageName + '_' + j

    #print(imageName)
    data = {}
    data['snimky'] = []
    
    for n in range(1,numberOfImages+1,1):
        nstr = '{:03}'.format(n)

        iurl = jmeno[3]+'/'+jmeno[4]+'/'+jmeno[5]+'/'+imageName+nstr+'.jpg'
        
        snimek = {}
        snimek['url'] = iurl
        data['snimky'].append(snimek)


    fn = './'+json_img+'/'+i+'.json'
    with open(fn,'w',encoding="utf-8") as f:
        json.dump(data,f,indent=4,ensure_ascii=False)
    


    


    #print(content)  


'''
dn_info = 'html-info'

if not os.path.isdir(dn_info):
    os.mkdir('./'+dn_info)

# for every downloaded html, download the information table

for f in files:
    fn = './'+dn_html+'/'+f

    with open(fn,'r',encoding="utf-8") as fi:
        content = fi.read()

        # get all content links
        links = re.findall(r'onclick="renderRowClasses.*?(?=" href)" href="([^"]*)">',content)

        for link in links:
            url = base+link
            
            # download link
            r = s.get(url,cookies=cookies)    
            content = r.text
    
            id = link.split('/')[-1]
            ifn = './'+dn_info+'/'+id+'.html'
            
            with open(ifn,'w',encoding="utf-8") as fii:
                fii.write(content)                
'''

'''
# download the webpage 
r = s.get(url,cookies=cookies)  
content = r.text
with open('test.html','w',encoding="utf-8") as f:
    f.write(content)

url = base+'/pages/MatrikaPage/matrikaId/3726'
r = s.get(url,cookies=cookies)  
content = r.text

with open('test1.html','w',encoding="utf-8") as f:
    f.write(content)


# number of entries
#matches = re.findall(r'Celkem[^:]*:[^\d]*([^<]*)',content)
#print(matches[0].strip())
#numberOfEntries = int(matches[0].strip().replace(' ',''))
#numberOfEntries = 2812

'''
'''
dn = 'html'
if not os.path.isdir(dn):
    os.mkdir('./'+dn)




if not len(os.listdir(dn)) == numberOfEntries: # not all HTMLs are downloaded
    for n in range(1,numberOfEntries+1,1):
        fn = './'+dn+f'/{n:05d}.html'

        if os.path.isfile(fn): # skip 
            print(f'Skipping: {fn}')
            #content = getNextPage(s,content)
        else: # new file
            print(fn)
            with open(fn,'w',encoding="utf-8") as f:
                #content = getNextPage(s,content)
   s             snimky = re.findall(r'<div class="oneThumbBloc imageArea">\s+<a href="([^"]*)"',content)

                if len(snimky) != 0:
                    fn_images = './'+dn+f'/{n:05d}_images.html'
                    r = s.get('http://katalog.ahmp.cz'+html.unescape(snimky[0]),cookies=cookies)    
                    content_images = r.text

                    with open(fn_images,'w',encoding="utf-8") as fi:
                        fi.write(content_images)


                f.write(content)
                #time.sleep(2)
                content = getNextPage(s,content)

                
'''

