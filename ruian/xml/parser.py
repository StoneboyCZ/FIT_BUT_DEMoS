import xml.etree.ElementTree as ET


tree = ET.parse('ruian.xml')
root = tree.getroot()
data = root[1][0]

children = data.iter()
for ch in children:
    print(ch)

