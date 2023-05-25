'''
coding:utf-8
@Software:PyCharm
@Time:2023/5/24 00:07
@Author:尘心||rocky
'''


import json
import os
import zipfile

import requests

from app.utils import all_cookie

# 默认的文件操作编码为 utf-8
DEFAULT_ENCODING = 'utf-8'


# 定义文件写操作函数
def write(content: str, path: str, mode: str = 'a', encoding: str = DEFAULT_ENCODING):
    """
    写入文件内容。

    Args:
        content (str): 要写入的内容。
        path (str): 文件路径。
        mode (str, optional): 文件打开模式。默认为 'a'（追加模式）。
        encoding (str, optional): 文件编码。默认为 utf-8。
    """
    with open(path, mode, encoding=encoding) as f:
        f.write(content)


# 定义文件读操作函数
def read(path: str, encoding: str = DEFAULT_ENCODING) -> list[str]:
    """
    读取文件内容。

    Args:
        path (str): 文件路径。
        encoding (str, optional): 文件编码。默认为 utf-8。

    Returns:
        list[str]: 文件的每一行内容。
    """
    with open(path, encoding=encoding) as f:
        lines = f.readlines()
    return lines


# 定义从url中获取文件名函数
def get_file_name(url: str) -> str:
    """
    从给定的URL中获取文件名。

    Args:
        url (str): 文件的URL。

    Returns:
        str: URL的文件名部分。
    """
    return os.path.basename(url)


# 定义下载文件函数
def download(file_hash: str, file_path: str):
    """
    根据给定的文件哈希和文件路径，下载文件,不解压。

    Args:
        file_hash (str): 文件的哈希值。
        file_path (str): 要保存文件的路径。

    Returns:
        dict: 下载结果。如果成功，返回的字典包含'code'和'fileName'键。
    """
    url = all_cookie.vul_host + f"/api/admin/vul/down_file/{file_hash}"
    try:
        res = requests.get(url, verify=False)
        if res.status_code == 200:
            file_name = res.headers['Content-Disposition'].split(';')[1].strip().split('=')[1].strip('"')
            with open(os.path.join(file_path, file_name), 'wb') as file:
                file.write(res.content)
            return {'code': 200, 'fileName': file_name}
    except requests.RequestException as e:
        print(f"\033[0;31m[!!] Download error: {e}\033[0m")
    return {'code': 500}


def download_and_unzip_keep(file_hash: str, save_path: str):
    """
    从指定URL下载文件，保存并如果是zip文件则解压到指定路径，保留下载的zip文件。

    Args:
        file_hash (str): 文件的哈希值。
        save_path (str): 保存和解压文件的路径。

    Returns:
        dict: 包含下载情况的字典，键'code'的值为200表示下载成功，500表示下载失败。
    """
    url = all_cookie.vul_host + f"/api/admin/vul/down_file/{file_hash}"
    response = requests.get(url, stream=True)

    if response.status_code == 200:
        file_name = response.headers.get('Content-Disposition', '').split(';')[1].strip().split('=')[1].strip('"')
        file_path = os.path.join(save_path, file_name)
        with open(file_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)

        # 尝试解压文件
        if file_name.endswith('.zip'):
            try:
                with zipfile.ZipFile(file_path, 'r') as zip_ref:
                    zip_ref.extractall(save_path)
            except zipfile.BadZipFile:
                return {'code': 500, 'fileName': file_name}
        return {'code': 200, 'fileName': file_name}
    else:
        return {'code': 500}


def download_and_unzip(file_hash: str, save_path: str):
    """
    从指定URL下载文件，保存并如果是zip文件则解压到指定路径。

    Args:
        file_hash (str): 文件的哈希值。
        save_path (str): 保存和解压文件的路径。

    Returns:
        dict: 包含下载情况的字典，键'code'的值为200表示下载成功，500表示下载失败。
    """

    url = all_cookie.vul_host + f"/api/admin/vul/down_file/{file_hash}"
    response = requests.get(url, stream=True)

    if response.status_code == 200:
        file_name = response.headers.get('Content-Disposition', '').split(';')[1].strip().split('=')[1].strip('"')
        file_path = os.path.join(save_path, file_name)
        with open(file_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
        # 尝试解压文件
        try:
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(save_path)
            # 删除原始的zip文件
            os.remove(file_path)
            return {'code': 200, 'fileName': file_name}
        except zipfile.BadZipFile:
            print(f"{file_path} may not be a zip file. Skipping.")
            return {'code': 200, 'message': 'File downloaded but not unzipped', 'fileName': file_name}
    else:
        return {'code': 500, 'message': f"Failed to download file. HTTP status code: {response.status_code}"}


# 定义从漏洞信息中获取编号函数
def get_vul_num(data: dict[str, str]) -> str:
    """
    从给定的漏洞信息中获取编号。

    Args:
        data (dict[str, str]): 包含漏洞信息的字典。

    Returns:
        str: 漏洞的编号。
    """
    return data.get("name", "")


# 定义生成调用接口时需要的body函数
def build_data(detail: dict) -> dict:
    """
    根据详细信息生成调用接口时需要的数据。

    Args:
        detail (dict): 详细信息字典。

    Returns:
        dict: 调用接口时需要的数据字典。
    """
    with open('./resource/post.json', encoding=DEFAULT_ENCODING) as f:
        post_data = json.load(f)

    base_path = f"./resource/vul_data/{detail['bug_no']}/"

    for k in post_data.keys():
        # 注意你的 copy 函数还没有实现
        copy(post_data, detail, k)

    post_data['bug_detail'] = read(os.path.join(base_path, 'res.html'))[0]

    if os.path.exists(os.path.join(base_path, 'poc.html')):
        post_data['poc_code'] = read(os.path.join(base_path, 'poc.html'))[0]

    post_data.setdefault('product_tag_id', 'EnhXv63UBKg=')
    post_data.setdefault('ver_open_date', '2022-08-24 11:11:11')
    post_data.setdefault('bug_type', '110')
    post_data.setdefault('bug_desc', 'tmp')

    post_data['side_commit'] = '5'

    return post_data
