from __future__ import print_function
import ctypes
import sys
import linecache
import shutil
import os
import time

ip = '172.253.116.90'  # 修改这个地方更改谷歌翻译接口
print('''
源文件名为hosts
目录在C:/Windows/System32/drivers/etc/这个目录下
hosts+时间.bak文件是原始的hosts文件，hosts.bak文件为上次修改的文件
''')


# 查看是否为管理员权限
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


if is_admin():    # 这里放使用admin权限执行代码
    currtime = time.strftime('_%Y-%m-%d', time.localtime(time.time()))
    fileload = 'C:/Windows/System32/drivers/etc/'
    filename = f'{fileload}hosts'
    rename = f'{fileload}hosts{currtime}.bak'
    filename2 = f'{fileload}2.txt'
    if not os.path.exists(f"{fileload}hosts.bak"):
        shutil.copy(filename, rename)

    # 使用utf-8编码进行打开
    FileLength: int = len(open(rf"{filename}", "r", encoding='utf-8').readlines())
    Mak = 0  # 标记之前是否存在规则
    col = -1  # 标记匹配出现的行数
    with open(rf'{filename}', 'r') as f1:
        # 使用utf-8编码进行打开
        with open(rf'{fileload}2.txt', 'w', encoding='utf-8') as f2:
            for i in range(FileLength):
                if i == col:
                    continue
                text = linecache.getline(filename, i + 1)
                textlen = len(text)
                if textlen < 25:
                    # 小于该字符则直接写入
                    f2.write(text)
                else:
                    # 判断是否为写入过字符
                    if text[-27:-1] == 'Translation Browser Plugin':
                        Mak = 1
                        col = i + 1
                        # 写入规则
                        f2.write('# For Translation Browser Plugin\n')
                        f2.write(f'{ip}  translate.googleapis.com\n')
                    elif text[-25:-1] == 'translate.googleapis.com':
                        Mak = 1
                        f2.write('# For Translation Browser Plugin\n')
                        f2.write(f'{ip}  translate.googleapis.com\n')
                    else:
                        f2.write(text)
            if Mak == 0:
                f2.write('\n# For Translation Browser Plugin\n')
                f2.write(f'{ip}  translate.googleapis.com\n')
            f2.close()
        f1.close()
    # 进行重命名
    srcFile = f'{fileload}hosts'
    dstFile = f'{fileload}hosts.bak'
    srcFile2 = f'{fileload}2.txt'
    dstFile2 = f'{fileload}hosts'
    if os.path.exists(f"{fileload}hosts.bak"):
        os.remove(f"{fileload}hosts.bak")
    try:
        os.rename(srcFile, dstFile)
        os.rename(srcFile2, dstFile2)
    except Exception as e:
        print(e)
        print('添加失败\r\n')
    else:
        print('添加成功\r\n')
        print(f'当前添加的字符为：\n\n# For Translation Browser Plugin\n{ip}  translate.googleapis.com\n')
    os.system("pause")
else:
    # 判断python版本
    if sys.version_info[0] == 3:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
    else:  # in python2.x
        ctypes.windll.shell32.ShellExecuteW(None, u"runas", unicode(sys.executable), unicode(__file__), None, 1)