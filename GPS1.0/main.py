import exifread
import re


def read():
    GPS = {}
    date = ''
    f = open(r"D:\pycharm\workspace\PycharmProjects\GPS3.0\20181120135.jpg", 'rb')
    contents = exifread.process_file(f)
    for key in contents:
        if key == "GPS GPSLongitude":
            print("经度: ", contents[key],contents['GPS GPSLatitudeRef'])
            print("纬度: ",contents['GPS GPSLatitude'],contents['GPS GPSLongitudeRef'])
            print("高度基准: ",contents['GPS GPSAltitudeRef'])
            print("海拔高度: ",contents['GPS GPSAltitude'])
        if re.match('Image Make', key):
            print('品牌信息: ' , contents[key])
        if re.match('Image Model', key):
            print('具体型号: ' , contents[key])
        if re.match('Image DateTime', key):
            print('拍摄时间: ' , contents[key])
        if re.match('EXIF ExifImageWidth', key):
            print('照片尺寸: ' , contents[key],'*',contents['EXIF ExifImageLength'])
        if re.match('Image ImageDescription',key):
            print('图像描述: ' , contents[key])


if __name__ == '__main__':
    read()
