'''
coding:utf-8
@Software:PyCharm
@Time:2023/5/22 12:07
@Author:尘心||rocky
'''

import os

from app.console.VulInfo import VulInfo
from app.utils import util
from app.utils import all_cookie

vul_heards = all_cookie.vul_headers
vul_host = all_cookie.vul_host

DOWNLOAD_MSG = "[*] 正在下载."
SUCCESS_MSG = "[*] 文件下载成功!"
FAILED_MSG = "[*] 文件下载失败!"
ERROR_MSG = "下载或解压时出现错误: {}"


class PocDownloader:
    def get_poc_file(self, path, vul_num, exp_flow_s3_hash, exp_code_s3_hash):
        """
        下载POC文件到指定路径。

        :param path: 下载文件的路径。
        :param vul_num: 与漏洞关联的编号。
        :param exp_flow_s3_hash: exp_flow_s3文件的哈希值。
        :param exp_code_s3_hash: exp_code_s3文件的哈希值。
        :return: 下载的exp_flow_s3和exp_code_s3文件的文件名。
        """
        file_path = os.path.join(path, str(vul_num))
        os.makedirs(file_path, exist_ok=True)
        print(DOWNLOAD_MSG)

        try:
            start_down_exp_flow = util.download_and_unzip(exp_flow_s3_hash, file_path)
            start_down_exp_code = util.download_and_unzip(exp_code_s3_hash, file_path)
            if start_down_exp_flow and start_down_exp_code:
                if start_down_exp_flow['code'] == 200 and start_down_exp_code['code'] == 200:
                    print(SUCCESS_MSG)
                    return "[+]{0} {1}".format(start_down_exp_flow['fileName'], start_down_exp_code['fileName'])
                else:
                    print(FAILED_MSG)
            else:
                print("start_down_exp_flow 或 start_down_exp_code 为空")
        except Exception as e:
            print(ERROR_MSG.format(e))

    def download_pocs(self, vul_host,vul_headers,path, page=3, limit=20):
        """
        下载多个POC文件。

        :param path: 下载文件的路径。
        :param page: 开始下载的页码（默认为3）。
        :param limit: 下载POC文件的最大数量（默认为20）。
        """
        audit_data = VulInfo()
        audit_data_list = audit_data.get_audit_info(vul_host=vul_host,vul_headers=vul_headers,page=page, limit=limit)
        print(audit_data_list)
        for data in audit_data_list:
            print(self.get_poc_file(
                path=path,
                vul_num=data["vul_num"],
                exp_flow_s3_hash=data["exp_flow_s3_hash"],
                exp_code_s3_hash=data["exp_code_s3_hash"]
            ))


if __name__ == '__main__':
    downloader = PocDownloader()
    downloader.download_pocs(vul_headers=vul_heards,vul_host=vul_host,path="../../storage/vul_data/")
