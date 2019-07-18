# http://docs.python-requests.org/en/master/user/quickstart/#cookies
# http://docs.python-requests.org/en/master/user/install/#install


import requests 
import zipfile

zippedFileName = 'matriky.zip'

# just donwload the current xml and unzip it
url = 'https://digi.ceskearchivy.cz/files/export/matriky.zip'

s = requests.session()

r = s.get(url)

with open(zippedFileName,'wb') as f:
    f.write(r.content)

# unzip the downloaded filename
with zipfile.ZipFile(zippedFileName, 'r') as zip_ref:
    zip_ref.extractall()




