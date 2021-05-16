import os
from winreg import *


def returnDir():
    dirs = ['C:\\Recycler\\', 'C:\\Recycled', 'C:\\$Recycle.Bin\\']
    for recycleDir in dirs:
        if os.path.isdir(recycleDir):
            return recycleDir
    return None


def sid2user(sid):
    try:
        key = OpenKey(HKEY_LOCAL_MACHINE, "SOFTWARE\Microsoft\Windows NT\CurrentVersion\ProfileList\\" + sid)
        count = QueryInfoKey(key)[1]
        for j in range(count):
            name, value, type = EnumValue(key, j)
            if ('ProfileImagePath' in name):
                user = value.split('\\')[-1]
        return user
    except:
        return sid


def findRecycle(recycleDir):
    dirList = os.listdir(recycleDir)
    for sid in dirList:
        print(sid)
        files = os.listdir(recycleDir + sid)
        print(files)
        user = sid2user(sid)
        print('[*]用户:' + str(user)+'曾经删除过的文件')
        for file in files:
            print('[+]Found File:' + str(file))
        print("")


def main():
    res = returnDir()
    print(res)
    findRecycle(res)


if __name__ == '__main__':
    main()
