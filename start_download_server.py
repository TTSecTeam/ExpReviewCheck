'''
coding:utf-8
@Software:PyCharm
@Time:2023/5/24 19:05
@Author:尘心||rocky
'''

from app.console.PocDownloader import PocDownloader
from app.utils import all_cookie


def main():
    vul_headers = all_cookie.vul_headers
    vul_host = all_cookie.vul_host

    # 拉取对外poc平台待审核的EXP，可以设置分页
    downloader = PocDownloader()
    downloader.download_pocs(vul_host=vul_host, vul_headers=vul_headers, path="./storage/vul_data/",
                                               page=1, limit=20)


if __name__ == '__main__':
    main()
