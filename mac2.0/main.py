from winreg import *
import os


def val2addr(val):
    addrlst = []
    for ch in val:
        addrlst.append(str(hex(ch))[-2:])
    MAC_ADDR = ':'.join(addrlst)
    return MAC_ADDR


def printNets():
        location = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\NetworkList\Signatures\Unmanaged"
        key = OpenKey(HKEY_LOCAL_MACHINE, location)
        hostname = os.getenv('computername')
        print("计算机" + hostname + "曾经浏览过这些网络")
        for i in range(100):
            try:
                guid = EnumKey(key, i)
                netKey = OpenKey(key, str(guid))
                (n, addr, t) = EnumValue(netKey, 5)
                (n, name, t) = EnumValue(netKey, 4)  
                macAddr = val2addr(addr)
                SSID = str(name).strip()
                if SSID == '网络':
                    CloseKey(netKey)
                else:
                    print(end='')
                    print('%-10s' % SSID, end='')
                    print('%-10s' % '对应的MAC地址', end='')
                    print(macAddr)
                CloseKey(netKey)
            except Exception as e:
                break


if __name__=='__main__':
    printNets()
