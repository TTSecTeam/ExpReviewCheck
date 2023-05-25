工具用途：
1. 对poc中的自定义字段进行验证，包括是否缺少字段、字段类型、字段内容检查；
2. 验证指纹能否匹配（在批量模式下会提取poc中的targets字段作为目标环境进行指纹验证）。

## 批量poc和指纹验证
1. 将poc和指纹按照一下目录结构存放。
```
ast
	LDY-2021-01041184
		Nette.json
		Nette_cve_2020_15227.py
	LDY-2022-00096949
		SDT-CW3B1.json
		Telesquare_SDT-CW3B1_cve_2021_46422.py
```
2. 运行 check.py
```
python .\check.py --dir C:\ast\
```
dir 参数为存放指纹和poc的父路径，使用这种方式，会提取指定路径下所有poc和指纹进行检查

## 验证指定poc
```
python .\check.py --file C:\ast\LDY-2021-01041184\Nette_cve_2020_15227.py
```

## 验证指定指纹
windows:
```
fingercheck.exe -json C:\ast\LDY-2021-01041184\Nette.json -url https://xxxxx
```
linux:
```
fingercheck -json /home/test/ast/LDY-2021-01041184/Nette.json -url https://xxxxx
```

## 工具运行结果
根据日志中的错误提示可见验证失败的poc或指纹文件。
```shell
[11:18:38] [INFO] loading PoC script 'C:\ast\LDY-2021-01041184\Nette_cve_2020_15227.py'
[11:18:38] [INFO] loading PoC script 'C:\ast\LDY-2022-00096949\Telesquare_SDT-CW3B1_cve_2021_46422.py'
[11:18:38] [ERROR] fingerprintName(Nette) in 'pocs_Nette_cve_2020_15227' is not valid, please add it to config.json.
[11:18:38] [ERROR] appName(SDT-CW3B1) in 'pocs_Telesquare_SDT-CW3B1_cve_2021_46422' is not valid, please add it to config.json.
[14:17:00] [ERROR] Finger Test Failed:  C:\ast\LDY-2021-01041184\Nette.json
[14:17:00] [INFO] Finger Test Passed:  C:\ast\LDY-2022-00096949\SDT-CW3B1.json

```
poc、指纹验证结果统计：
```shell
[14:21:11] [INFO] ==================================================
[14:21:11] [INFO] total poc:  1
[14:21:11] [INFO] passed poc: 1
[14:21:11] [INFO] failed poc: 0
[14:21:11] [INFO] --------------------------------------------------
[14:21:11] [INFO] total finger:  0
[14:21:11] [INFO] passed finger: 0
[14:21:11] [INFO] failed finger: 0
[14:21:11] [INFO] ==================================================
```

## 特殊说明

poc中的`appName`和`fingerprintNames`字段值必须在附件config_list.json中（config_list.json中已经存在大量appname，可以从中取值），若不存在需手动添加到改文件中，并再次运行工具进行验证。

