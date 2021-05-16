import exifread
import re
import os
import sys


def Find_GPSimage(filepath):
    GPS = {}
    date = ''
    f = open(filepath, 'rb')
    tags = exifread.process_file(f)
    for tag, value in tags.items():
        if re.match('GPS GPSLatitudeRef', tag):
            GPS['GPSLatitudeRef'] = str(value)
        elif re.match('GPS GPSLongitudeRef', tag):
            GPS['GPSLongitudeRef'] = str(value)
        elif re.match('GPS GPSAltitudeRef', tag):
            GPS['GPSAltitudeRef'] = int(str(value))
        elif re.match('GPS GPSLatitude', tag):
            try:
                match_result = re.match('\[(\w*)， (\w*)， (\w.*)/(\w.*)\]', str(value)).groups()
                GPS['GPSLatitude'] = int(match_result[0]), int(match_result[1]), int(match_result[2])
            except:
                GPS['GPSLatitude'] = str(value)
        elif re.match('GPS GPSLongitude', tag):
            try:
                match_result = re.match('\[(\w*)， (\w*)， (\w.*)/(\w.*)\]', str(value)).groups()
                GPS['GPSLongitude'] = int(match_result[0]), int(match_result[1]), int(match_result[2])
            except:
                GPS['GPSLongitude'] = str(value)
        elif re.match('GPS GPSAltitude', tag):
                GPS['GPSAltitude'] = str(value)
        elif re.match('.*Date.*', tag):
            date = str(value)
    print('GPS：', GPS)
    print('时间信息：', {date})
    return {'GPSLatitudeRef标识南北纬，GPSLongitudeRef标识东西经，GPSAltitudeRef标识高度'}


if __name__=='__main__':
    print(Find_GPSimage(r"D:\pycharm\workspace\PycharmProjects\GPS3.0\20181120135.jpg"))



