# 注册
from winreg import *
import os


def val2addr(val):
    addr = ""
    for ch in val:
        addr += ("%02x " % ord(ch))
    addr = addr.strip(' ').replace(" ",":")[0:17]
    return addr


def printNets():
        location = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\NetworkList\Signatures\Unmanaged"
        key = OpenKey(HKEY_LOCAL_MACHINE, location)
        hostname = os.getenv('computername')
        print("计算机" + hostname + "浏览过以下的网络")
        for i in range(100):
            try:
                guid = EnumKey(key, i)
                netKey = OpenKey(key, str(guid))
                (n, addr, t) = EnumValue(netKey, 5)  # 5是地址
                # print('名称',  n)
                # print('地址', addr)
                # print('类型', t)
                (n, name, t) = EnumValue(netKey, 4)  # 4是名字
                print('名称', n)
                print('地址', addr)
                print('类型', t)
                macAddr = val2addr(addr)
                SSID = str(name).strip()
                print(macAddr)
                CloseKey(netKey)
            except Exception as e:
                print('chucuo')


if __name__=='__main__':
    printNets()