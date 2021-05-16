import winreg


def read_reg():
    location = r"Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Shell Folders"
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, location)
    i = 0
    while True:
        try:
            # 获取注册表对应位置的键和值
            print(winreg.EnumValue(key, i))
            i += 1
        except OSError as error:
            winreg.CloseKey(key)
            break
if __name__ == '__main__':
    read_reg()
