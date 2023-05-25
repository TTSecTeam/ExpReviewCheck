'''
coding:utf-8
@Software:PyCharm
@Time:2023/5/25 07:40
@Author:尘心||rocky
'''

from app.console.DirectoryChecker import DirectoryChecker


def main():
    obj = DirectoryChecker()
    obj.check(directory="./storage/vul_data")

if __name__ == '__main__':
    main()
