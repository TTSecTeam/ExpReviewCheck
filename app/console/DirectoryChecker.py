'''
coding:utf-8
@Software:PyCharm
@Time:2023/5/24 10:59
@Author:尘心||rocky
'''


from plugins.fingertest_tools import check

class DirectoryChecker:
    def check(self, directory, _file=None, _ignore=False):

        check.main(directory, _file, _ignore)


if __name__ == '__main__':
    obj = DirectoryChecker()
    test = obj.check(directory="../../storage/vul_data/")
