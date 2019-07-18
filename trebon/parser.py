# http://docs.python-requests.org/en/master/user/quickstart/#cookies
# http://docs.python-requests.org/en/master/user/install/#install
# http://images.archives.cz/mrimage/matriky/proxy/cz/archives/CZ-217000010/NAD-165/dao/images/0345/8b1ef2b1-eba4-4b55-805d-f79d56afada0.jpg
# http://digi.archives.cz/da/Zoomify.action?entityRef=%28%5En%29%28%28%28localArchiv%2C%5En%2Chot_%29%28unidata%29%29%28338508%29%29&scanIndex=0

# I-N_I-Z_I-O_inv_c_124a_sig_Op_VII_13_1789-1799_Katerinky_025.jpg

# <tr class="propojLok">\s*<[^>]*>([^<]*).*\s*</tr>\s*<tr>\s*.*?(?=va)[^>]*>(.*?)(?=</td)

import random
import time
import re
import os
import lxml
from lxml import etree
import json


tree = etree.parse('matriky.xml')
root = tree.getroot()

puvodciXML = root.findall('.//{http://www.mvcr.cz/archivy/evidence-nad/matriky}puvodce')
puvodci = {}
for p in puvodciXML:
    puvodci[p.get('idPuvodce')] = p.findall('nazevPuvodce')
    print( p.findall('nazevPuvodce'))

'''
matriky = root.findall('.//{http://www.mvcr.cz/archivy/evidence-nad/matriky}matrika')
for m in matriky:
    print(list(m))
'''


