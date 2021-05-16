import exifread
import re
import json
import requests
import sys


def latitude_and_longitude_convert_to_decimal_system(*arg):
    return float(arg[0]) + ((float(arg[1]) + (float(arg[2].split('/')[0]) / float(arg[2].split('/')[-1]) / 60)) / 60)


def find_GPS_image(pic_path):
    GPS = {}
    date = ''
    with open(pic_path, 'rb') as f:
        tags = exifread.process_file(f)
        for tag, value in tags.items():
            if re.match('Image Make', tag):
                print('[*]手机的品牌: ' + str(value))
                a = '[*]手机的品牌: ' + str(value)
                print(a)
            if re.match('Image Model', tag):
                print('[*]拍摄手机的型号: ' + str(value))
                b = '[*]拍摄手机的型号: ' + str(value)
            if re.match('EXIF LensModel', tag):
                print('[*]摄像头: ' + str(value))
                c = '[*]摄像头: ' + str(value)
            if re.match('EXIF ExifImageWidth', tag):
                print('[*]照片分辨率: ' + str(value) + '*' + str(tags['EXIF ExifImageLength']))
                d = '[*]照片分辨率: ' + str(value) + '*' + str(tags['EXIF ExifImageLength'])
            if re.match('GPS GPSLatitudeRef', tag):
                GPS['GPSLatitudeRef'] = str(value)
            elif re.match('GPS GPSLongitudeRef', tag):
                GPS['GPSLongitudeRef'] = str(value)
            elif re.match('GPS GPSAltitudeRef', tag):
                GPS['GPSAltitudeRef'] = str(value)
            elif re.match('GPS GPSLatitude', tag):
                try:
                    match_result = re.match('\[(\w*),(\w*),(\w.*)/(\w.*)\]', str(value)).groups()
                    GPS['GPSLatitude'] = int(match_result[0]), int(match_result[1]), int(match_result[2])
                except:
                    deg, min, sec = [x.replace(' ', '') for x in str(value)[1:-1].split(',')]
                    GPS['GPSLatitude'] = latitude_and_longitude_convert_to_decimal_system(deg, min, sec)
            elif re.match('GPS GPSLongitude', tag):
                try:
                    match_result = re.match('\[(\w*),(\w*),(\w.*)/(\w.*)\]', str(value)).groups()
                    GPS['GPSLongitude'] = int(match_result[0]), int(match_result[1]), int(match_result[2])
                except:
                    deg, min, sec = [x.replace(' ', '') for x in str(value)[1:-1].split(',')]
                    GPS['GPSLongitude'] = latitude_and_longitude_convert_to_decimal_system(deg, min, sec)
            elif re.match('GPS GPSAltitude', tag):
                GPS['GPSAltitude'] = str(value)
            elif re.match('.*Date.*', tag):
                date = str(value)
    #print({'GPS_information':GPS, 'date_information': date})
    print('[*]拍摄时间: ' + date)
    return {'GPS_information': GPS, 'date_information': date}


def find_address_from_GPS(GPS):
    secret_key = 'iN1BUAoCo9WgheHwS1HF2BdplriOnQBG'
    if not GPS['GPS_information']:
        return '该照片无GPS信息'
    lat, lng = GPS['GPS_information']['GPSLatitude'], GPS['GPS_information']['GPSLongitude']
    print('[*]经度: ' + str(lat) + ' 纬度: ' + str(lng))
    baidu_map_api = "http://api.map.baidu.com/reverse_geocoding/v3/?ak={0}&coordtype=renderReverse&location={1},{2}s&output=json&pois=0".format(
        secret_key, lat, lng)
    response = requests.get(baidu_map_api)
    content = response.text.replace("renderReverse&&renderReverse(", "")
    print(content )
    print(type(content))
    content = content[85::]
    print(content)
    baidu_map_address = json.loads(content)
    formatted_address = baidu_map_address["result"]["formatted_address"]
    return formatted_address


if __name__ == '__main__':
    name = input('输入你想要查看的照片的名称')
    GPS_info = find_GPS_image(pic_path=name)
    address = find_address_from_GPS(GPS=GPS_info)
    print(address)
