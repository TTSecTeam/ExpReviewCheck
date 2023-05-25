'''
coding:utf-8
@Software:PyCharm
@Time:2023/5/22 12:07
@Author:尘心||rocky
'''

import os

import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from dotenv import find_dotenv, load_dotenv


# 获取当前文件的路径
current_path = os.path.dirname(os.path.abspath(__file__))

# 获取项目的根路径
root_path = os.path.dirname(current_path)

env_path = root_path + f"/../.env"

load_dotenv(find_dotenv(env_path))
env_dist = os.environ

headers = {
    'Cookie': '{0}'.format(env_dist.get('Cookie')),
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0'
}

front_header = {
    'Cookie': '{0}'.format(env_dist.get('Front_Cookie')),
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0'
}

host = ''

vul_headers = {
    'Authorization': '{0}'.format(env_dist.get('Authorization')),
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0)',
    'Content-Type': 'application/json;charset=utf-8'
}

vul_host = 'http://vulsub.xyz'

if __name__ == '__main__':
    print(vul_headers)
