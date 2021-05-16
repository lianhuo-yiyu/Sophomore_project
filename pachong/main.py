import  requests
import time
from lxml import etree
url = 'https://bz.zzzmh.cn/'

headers = {"Referer": "Referer: https://bz.zzzmh.cn/",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36",}

res = requests.get(url, headers=headers)
print(res)
html = etree.HTML(res.text)
srcs = html.xpath(".//img/@src")

for i in srcs:
    imgname = i.split('/')[-1]
    img = requests.get(i, headers=headers)
    with open('img/'+imgname, 'wb') as file:
        file.write(img.content)
    print(i, imgname)

