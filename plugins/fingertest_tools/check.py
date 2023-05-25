#!/usr/bin/env python3

import os
import re
import json
import shutil
import platform
import argparse
from argparse import RawTextHelpFormatter
from subprocess import PIPE, Popen

from pocsuite3.api import init_pocsuite, POC_CATEGORY, VUL_TYPE
from pocsuite3.lib.core.common import set_paths
from pocsuite3.lib.core.data import kb, logger

script_dir = os.path.dirname(__file__)

# 获取当前文件的路径
current_path = os.path.dirname(os.path.abspath(__file__))

# 获取项目的根路径
root_path = os.path.dirname(current_path)

print("Current path:", current_path)
print("Root path:", root_path)

def load_config():
    poc_config_path = os.path.join(script_dir, 'config_list.json')
    with open(poc_config_path, encoding='utf-8') as f:
        data = json.load(f)
        return data['app_name'], data['severity']

def load_pocsuite(config):
    try:
        init_pocsuite(config)
    except Exception as e:
        print(e)
        return []

def create_urls():
    try:
        with open(f"{current_path}/urls.txt","w") as f:
            for name, poc in kb.registered_pocs.items():
                f.write(f"{poc.targets}\n")
    except Exception as e:
        logger.error(e)
    f.close()


def ast_pocs(_dir, _file):
    pocs = []
    if _dir:
        for root, dirs, files in os.walk(_dir, topdown=False):
            pocs += [os.path.join(root, name)
                     for name in files if name.endswith('.py') and name != 'test.py']
    elif _file:
        pocs = [_file]
    return pocs


def ast_fingers(_dir, _file):
    fingers = []
    if _dir:
        for root, dirs, files in os.walk(_dir, topdown=False):
            fingers += [os.path.join(root, name)
                     for name in files if name.endswith('.json') and name != 'config_list.json']
    return fingers

vultypes = VUL_TYPE()
categories = POC_CATEGORY()
VALID_APP_NAMES, VALID_SEVERITIES = load_config()

def good_category(category):
    cats = []
    for cat in [getattr(categories, attr) for attr in dir(categories) if not callable(getattr(categories, attr)) and not attr.startswith("__")]:
        cats.extend(cat.values())
    return category in cats


def good_type(vulnType):
    return vulnType in [getattr(vultypes, attr) for attr in dir(vultypes) if not callable(getattr(vultypes, attr)) and not attr.startswith("__")]


def validate_config(poc_name, poc, _ignore):
    try:
        # 字段类型检查
        if not isinstance(poc.vulID, str):
            logger.error("The vulID attribute in '%s' should be str.", poc_name)
            return False
        if not isinstance(poc.version, str):
            logger.error("The version attribute in '%s' should be str.", poc_name)
            return False
        if not isinstance(poc.author, list):
            logger.error("The author attribute in '%s' should be list.", poc_name)
            return False
        if not isinstance(poc.vulDate, str):
            logger.error("The vulDate attribute in '%s' should be str.", poc_name)
            return False
        if not isinstance(poc.createDate, str):
            logger.error("The createDate attribute in '%s' should be str.", poc_name)
            return False
        if not isinstance(poc.updateDate, str):
            logger.error("The updateDate attribute in '%s' should be str.", poc_name)
            return False
        if not isinstance(poc.name, str):
            logger.error("The name attribute in '%s' should be str.", poc_name)
            return False
        if not isinstance(poc.CVE, str):
            logger.error("The CVE attribute in '%s' should be str.", poc_name)
            return False
        if not isinstance(poc.CNVD, str):
            logger.error("The CNVD attribute in '%s' should be str.", poc_name)
            return False
        if not isinstance(poc.severity, str):
            logger.error("The severity attribute in '%s' should be str.", poc_name)
            return False
        if not isinstance(poc.reqAuth, bool):
            logger.error("The reqAuth attribute in '%s' should be boolen.", poc_name)
            return False
        if not isinstance(poc.appName, str):
            logger.error("The appName attribute in '%s' should be str.", poc_name)
            return False
        if not isinstance(poc.fingerprintNames, list):
            logger.error("The fingerprintNames attribute in '%s' should be list.", poc_name)
            return False
        if not isinstance(poc.app_main_port, int):
            logger.error("The app_main_port attribute in '%s' should be int.", poc_name)
            return False
        if not isinstance(poc.appVersion, str):
            logger.error("The appVersion attribute in '%s' should be str.", poc_name)
            return False
        if not isinstance(poc.appPowerLink, str):
            logger.error("The appPowerLink attribute in '%s' should be str.", poc_name)
            return False
        if not isinstance(poc.references, list):
            logger.error("The references attribute in '%s' should be list.", poc_name)
            return False
        if not isinstance(poc.desc, str):
            logger.error("The desc attribute in '%s' should be str.", poc_name)
            return False
        if not isinstance(poc.suggest, str):
            logger.error("The suggest attribute in '%s' should be str.", poc_name)
            return False
        if not isinstance(poc.hasExp, bool):
            logger.error("The hasExp attribute in '%s' should be boolen.", poc_name)
            return False
        if not isinstance(poc.targets, str) and not isinstance(poc.targets, list):
            logger.error("The targets attribute in '%s' should be str.", poc_name)
            return False
        if not isinstance(poc.suricata_rules, str):
            logger.error("The suricata_rules attribute in '%s' should be str.", poc_name)
            return False

        # 字段值检查
        if poc.appName not in VALID_APP_NAMES and poc.appName.lower() not in VALID_APP_NAMES and not _ignore:
            logger.error("appName(%s) in '%s' is not valid, please add it to config.json.", poc.appName, poc_name)

            # 新的app_name
            new_app_names = [f"{poc.appName}"]
            print(new_app_names)

            # 读取已有的JSON文件
            with open(f"{current_path}/config_list.json", 'r') as f:
                data = json.load(f)

            print(data)

            # 追加新的app_name到列表中
            data['app_name'].extend(new_app_names)

            # 写回到文件
            with open(f"{current_path}/config_list.json", 'w') as f:
                json.dump(data, f, indent=4)
            print("写入成功")

            return False
        if hasattr(poc, 'fingerprintNames'):
            for finger in poc.fingerprintNames:
                if finger not in VALID_APP_NAMES and finger.lower() not in VALID_APP_NAMES and not _ignore:
                    logger.error("fingerprintName(%s) in '%s' is not valid, please add it to config.json.", finger, poc_name)
                    return False
        if poc.severity not in VALID_SEVERITIES:
            logger.error("severity(%s) in '%s' is not valid.", poc.severity, name)
            return False
        # if poc.name.split("_")[0] != poc.appName:
        #     logger.error("The attribute name should start with appName")
            return False
        if not good_type(poc.vulType):
            logger.error("The attribute vulType is not valid")
            return False
        if not good_category(poc.category):
            logger.error("The attribute category is not valid")
            return False

    except Exception as e:
            logger.error("{} {} {}".format(poc.vulID, poc.name, e))
            return False
    return True


def check_fingers(_dir, _file):
    passed = []
    failed = []

    if not _dir:
        return passed, failed

    if platform.system() == "Windows":
        cmd = f"{current_path}/fingertest.exe -dir {_dir} -urlfile {current_path}/urls.txt"
    else:
        cmd = f"{current_path}/./fingertest_mac --dir {_dir} -urlfile {current_path}/urls.txt"
    print(cmd)
    proc = Popen(cmd, stdin=None, stdout=PIPE, stderr=PIPE, shell=True)
    outinfo, errinfo = proc.communicate()

    if proc.returncode != 0:
        print(f"Error occurred: {errinfo.decode('utf-8')}")
    else:
        print(outinfo.decode('utf-8'))

    for line in outinfo.splitlines():
        line = line.decode()
        if "Finger Test Failed" in line:
            logger.error(line)
            failed.append(line.replace("Finger Test Failed:", ""))
        elif "Finger Test Passed:" in line:
            logger.info(line)
            passed.append(line.replace("Finger Test Passed:", ""))
        else:
            logger.info(line)

    for line in errinfo.splitlines():
        logger.info(line.decode())

    return passed, failed

def main(_dir, _file, _ignore):
    poc_files = ast_pocs(_dir, _file)
    fingers = ast_fingers(_dir, _file)

    load_pocsuite({'poc': poc_files})

    txtlines = ""
    
    count = 0
    good = 0
    failed = 0
    for name, poc in kb.registered_pocs.items():
        count += 1
        if not validate_config(name, poc, _ignore):
            failed += 1
            continue
        good += 1

    create_urls()
    passed_fingers, failed_fingers = check_fingers(_dir, _file)


    print("\n")
    logger.info("="*50)
    logger.info("total poc:  {}".format(count))
    logger.info("passed poc: {}".format(good))
    logger.info("failed poc: {}".format(failed))
    logger.info("-"*50)
    logger.info("total finger:  {}".format(len(fingers)))
    logger.info("passed finger: {}".format(len(passed_fingers)))
    logger.info("failed finger: {}".format(len(failed_fingers)))
    logger.info("="*50)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="ast poc config check", formatter_class=RawTextHelpFormatter)
    parser.add_argument("--dir", dest="dir", help=u"poc files dir")
    parser.add_argument("--file", dest="file", help=u"poc file")
    parser.add_argument("--ignore_checklist", dest="ignore", default=False, help=u"ignore checklist")
    args = parser.parse_args()
    _dir = args.dir
    _file = args.file
    _ignore = args.ignore
    main(_dir, _file, _ignore)
