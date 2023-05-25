'''
coding:utf-8
@Software:PyCharm
@Time:2023/5/22 12:07
@Author:尘心||rocky
'''

import requests
import json
import copy
from app.utils import all_cookie

class VulInfo:

    def get_audit_info(self,vul_host,vul_headers, page=1, limit=20):
        """
        获取对外poc平台待审核漏洞信息。

        参数:
            page (int): 想要获取的页数。
            limit (int): 每页的记录数。

        返回:
            dict: 包含漏洞信息的字典。
        """
        url = vul_host + f"/api/admin/exp/user_pend_exp_list?page={page}&limit={limit}"
        headers = vul_headers

        try:
            # proxies = {
            #     "http": "http://127.0.0.1:8089",
            #     "https": "http://127.0.0.1:8089",
            # }
            res = requests.get(url=url, headers=headers, verify=False)
            # if res.status_code == 200:
            vul_data = res.json()
            print(vul_data)
            return vul_data["data"]["list"]
        except Exception as e:
            print(f"\033[0;31m[!!] get_audit_info 错误: {e}\033[0m")
        return {'code': 404}


# if __name__ == '__main__':
#     obj = VulInfo()
#     print(obj.get_audit_info())
