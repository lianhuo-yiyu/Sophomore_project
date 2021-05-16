import exifread
import re
import json
import requests
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from untitled import Ui_Form


def latitude_and_longitude_convert_to_decimal_system(*arg):
    return float(arg[0]) + ((float(arg[1]) + (float(arg[2].split('/')[0]) / float(arg[2].split('/')[-1]) / 60)) / 60)


def find_GPS_image(pic_path):
    GPS = {}
    date = ''
    with open(pic_path, 'rb') as f:
        tags = exifread.process_file(f)
        for tag, value in tags.items():
            if re.match('Image Make', tag):
                print('手机的品牌: ' + str(value))
                global a
                a = '手机的品牌: ' + str(value)
            if re.match('Image Model', tag):
                print('[*]拍摄手机的型号: ' + str(value))
                global b
                b = '拍摄手机的型号: ' + str(value)
            if re.match('EXIF LensModel', tag):
                print('[*]摄像头: ' + str(value))
                global c
                c = '摄像头: ' + str(value)
            if re.match('EXIF ExifImageWidth', tag):
                print('照片分辨率: ' + str(value) + '*' + str(tags['EXIF ExifImageLength']))
                global d
                d = '照片分辨率: ' + str(value) + '*' + str(tags['EXIF ExifImageLength'])
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
                global e
                date = str(value)
    # print({'GPS_information':GPS, 'date_information': date})
    print('拍摄时间: '+ date)
    e = '拍摄时间: '+ date
    return {'GPS_information': GPS, 'date_information': date}


def find_address_from_GPS( GPS):
    secret_key = 'iN1BUAoCo9WgheHwS1HF2BdplriOnQBG'
    if not GPS['GPS_information']:
        return '该照片无GPS信息'
    lat, lng = GPS['GPS_information']['GPSLatitude'], GPS['GPS_information']['GPSLongitude']
    print('[*]经度: ' + str(lat) + ' 纬度: ' + str(lng))
    global f, g
    f = '经度: ' + str(lat)
    g = '纬度: ' + str(lng)
    baidu_map_api = "http://api.map.baidu.com/reverse_geocoding/v3/?ak={0}&coordtype=renderReverse&location={1},{2}s&output=json&pois=0".format(
        secret_key, lat, lng)
    response = requests.get(baidu_map_api)
    content = response.text.replace("renderReverse&&renderReverse(", "")
    print(content + '1')
    print(type(content), '1')
    content = content[106:118:]
    print("具体位置:" + content)
    global h
    h = content
    baidu_map_address = json.loads(content)
    print(list(baidu_map_address))
    print(dict(content + '5555'))
    print(type(content + '2'))
    formatted_address = baidu_map_address["result"]["formatted_address"]
    return formatted_address


class MyMainForm(QMainWindow, Ui_Form):
    def __init__(self, parent=None):
        super(MyMainForm, self).__init__(parent)
        self.setupUi(self)
        # 添加登录按钮信号和槽。注意display函数不加小括号()
        self.login_Button.clicked.connect(self.display)
        # 添加退出按钮信号和槽。调用close函数
        self.cancel_Button.clicked.connect(self.close)
    def display(self):
        # 利用line Edit控件对象text()函数获取界面输入
        global username
        username = self.user_lineEdit.text()
        print(username)
        # 利用text Browser控件对象setText()函数设置界面显示
        GPS_info = find_GPS_image(pic_path=username)
        address = find_address_from_GPS(GPS=GPS_info)
        self.user_textBrowser.setText(a + '\n' + b + '\n' + d + '\n' + e + '\n' + f + '\n' + g + '\n' + "具体位置:" + h)


if __name__ == "__main__":
    # 固定的，PyQt5程序都需要QApplication对象。sys.argv是命令行参数列表，确保程序可以双击运行
    # GPS_info = find_GPS_image(pic_path=username)
    # address = find_address_from_GPS(GPS=GPS_info)
    app = QApplication(sys.argv)
    # 初始化
    myWin = MyMainForm()
    # 将窗口控件显示在屏幕上
    myWin.show()
    # 程序运行，sys.exit方法确保程序完整退出。
    sys.exit(app.exec_())