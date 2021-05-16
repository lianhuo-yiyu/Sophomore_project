import  requests
import time
from lxml import etree
url = 'http://desk.zol.com.cn/dongman/1920x1080/'

headers = {"Referer":"Referer: http://desk.zol.com.cn/dongman/1920x1080/",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",}

resq = requests.get(url,headers = headers)

print(resq)

html = etree.HTML(resq.text)
srcs = html.xpath(".//img/@src")

def download_img(url):
    imgname = url.split('/')[-1]
    img = requests.get(url, headers = headers)
    with open('imgs1/'+imgname,'wb') as file:
        file.write(img.content)
        print(url, imgname)

def next_page(url):
    res = requests.get(url, headers = headers)
    html = etree.HTML(res.text)
    srcs = html.xpath(".//img/@src")
    for i in srcs:
        download_img(i)
    next_page_link = html.xpath('.//a[@id="pageNext"]/@href')
    return next_page_link

def main():
    current_page = 1
    next_page_base = 'http://desk.zol.com.cn/dongman/1920x1080/'
    next_page_link = html.xpath('.//a[@id="pageNext"]/@href')
    while next_page_link:
        current_page=current_page + 1
        next_page_link = next_page(next_page_base+str(current_page)+'.html')
        if current_page > 10:
            break

if __name__ == '__main__':
    main()

