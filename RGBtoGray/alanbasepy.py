# !/usr/bin/python
# -*- coding: utf-8 -*-
# alan's py func lib
# author:   alan
# firstDate:2021.07
# lastDate: 2022.05.07

try:
    import re
    import requests
except:
    print('module not found')

def justGetFileName(filepath, removesuffix=True): 
    """移除文件目录及文件后置，仅保留文件名并全部转为小写"""
    if removesuffix == True:
        re.sub(r'.*/', '', filepath)
    return re.sub(r'\..*', '', ).lower()

def stopWork(stopworktimetimestamp=1640966400):
    """检查是否到达设定的程序失效时间"""
    nowtimetimestamp = int(time.time())
    if nowtimetimestamp >= stopworktimetimestamp:
        printAndLog("\n" + str(nowtimetimestamp) + ": 程序已失效")
        return True
    else:
        return False

def throwAnException():
    """抛出异常"""
    int('abc')

def isAnInteger(num):
    """判定参数是否为整型数据"""
    try:
        int(num)
        return True
    except:
        return False
def listStr2Int(lst):
    return [int(i) for i in lst if i.isdigit()]

# # 时间格式化文本
import time
def getTimestamp(lenth):
    """获取时间戳"""
    now = time.time()
    if lenth == 13:
        return round(now*1000) # round函数会对数据进行四舍五入https://www.runoob.com/w3cnote/python-round-func-note.html
    else:
        return now

def timestamp2StrfTime(timestamp, dateinterval='/', interval=' ', timeinterval=':'): # 首先需要将时间戳转换成localtime，再转换成时间的具体格式
    """将时间戳转化为格式化时间"""
    time_local = time.localtime(timestamp)
    return time.strftime('%Y'+dateinterval+'%m'+dateinterval+'%d'+interval+'%H'+timeinterval+'%M'+timeinterval+'%S', time_local)

def getStrfTime(dateinterval='-', interval=' ', timeinterval='.'):
    """获取格式化时间"""
    return(time.strftime('%Y'+dateinterval+'%m'+dateinterval+'%d'+interval+'%H'+timeinterval+'%M'+timeinterval+'%S'))

# # 控制台操作
import os
import sys
def systemPause():
    """pause"""
    os.system("pause")

def clear():
    """对控制台输出进行清屏操作"""
    os.system('cls')

def typeWriter(words, intervalduration=0.013, end='\n'):
    """以打字机效果输出文本到控制台"""
    words = str(words)
    for char in words:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(intervalduration)
    sys.stdout.write(end)
    time.sleep(intervalduration)

# # 文件读写与文件夹
def mkUserDir(filepath):
    """创建用户文件夹目录"""
    if os.path.exists(filepath) != True:
        os.mkdir(filepath)

def fileExists(filename):
    """判定路径或文件是否存在"""
    if os.path.exists(filename):
        return True
    else:
        return False

def delPathAllFile(path):
    """删除指定路径下的所有文件"""
    dellist = getAllFileList(path)
    for filepath in dellist:
        if os.path.isfile(filepath):
            os.remove(filepath)

def writeFile(filepath, mode, str, encoding="utf8", end='\n'):
    """文件写入"""
    try:
        f = open(filepath, mode, encoding=encoding)
        f.write(str + end)
        f.close()
    except Exception as e:
        print(repr(e), "\n参数不合法或文件已被占用，打开失败，请稍后重试")
        return False
    return True

def checkFileTypeInList(filename, filetypelist):
    """检查文件是否为指定类型的文件"""
    if filetypelist == None:
        return False
    for filetype in filetypelist:
        if filename.lower().endswith(filetype):
            return filetype
    return False

def getAllFileList(filepath):
    """获取指定文件夹及其子文件夹下的所有文件目录"""
    fileList = []
    for root, dirs, files in os.walk(filepath):
        fileList += [os.path.join(root, name) for name in files]
    return fileList

def delLastStr(fname, seekstep=-3):
    """删除文件末尾seekstep个字符（windows中每个换行相当于2个字符）"""
    f = open(fname,"rb+")
    f.seek(seekstep ,os.SEEK_END)
    f.truncate()
    f.close()

def getAllFileName(path):
    """获取目录下的所有文件名"""
    filenames = [name for name in os.listdir(path) # os.listdir()方法用于返回指定文件夹包含的文件或文件夹的名字的列表。这个列表以字母顺序，不包括‘.’和‘…’即使其在文件夹中。 https://zhuanlan.zhihu.com/p/105642781
            if os.path.isfile(os.path.join(path, name))]
    return filenames

# # Log文件
LOG_PATH = ".\\Log\\"
LOG_FILENAME = LOG_PATH + "log" + getStrfTime() + ".log"

def printAndLog(str, filename=LOG_FILENAME, end='\n', flush=False, intervalduration=0.03):
    """输出内容并录入文件，打字机效果可选"""
    writeFile(filename, "a+", str, end)
    if flush == True:
        typeWriter(str, intervalduration=intervalduration, end=end)
    else:
        print(str, end=end)

def inputAndLog(str, filename=LOG_FILENAME, end='\n', flush=True, intervalduration=0.03):
    """将输入内容录入文件，打字机效果可选"""
    printAndLog(str, filename=filename, end=end, flush=flush, intervalduration=intervalduration)
    tempstr = input()
    writeFile(filename, "a+", tempstr, end)
    return tempstr

# # windows剪切板操作
try:
    import win32clipboard as w
    import win32con
except:
    print('module not found, "pip install pywin32"')

def getTextWithClipboard():
    """获取剪切板内容"""
    w.OpenClipboard()
    t = w.GetClipboardData(win32con.CF_UNICODETEXT)
    w.CloseClipboard()
    return t

def setTextWithClipboard(aString):
    """写入剪切板内容"""
    w.OpenClipboard()
    w.EmptyClipboard()
    w.SetClipboardData(win32con.CF_UNICODETEXT, aString)
    w.CloseClipboard()

# # 网络数据处理
try:
    import json
except:
    print('module json not found')

def jsonLog(resjson, filename, logconvlist):
    """获取的数据输出为json文件"""
    tempjson = json.dumps(resjson, indent=4, sort_keys=False, ensure_ascii=False)
    if logconvlist == True:
        tempjson = tempjson + ',' # 转化为列表数据
    try:
        f = open(filename, "a+", encoding="utf8")
        print(tempjson, file = f)
        f.close()
    except:
        print("文件已被占用，打开失败，请稍后重试")

# # 配置文件读取
try:
    from configparser import ConfigParser
except:
    print('module json not found')

def readCfg(conf, cfgfilename):
    """将配置文件内容读入内存"""
    if fileExists(cfgfilename) == False:
        print("配置文件不存在，将使用默认配置")
    conf.read(cfgfilename, encoding="UTF-8") # 用config对象读取配置文件
    return conf

class AlanCfg:
    def __init__(self, CFG_FILENAME='./pyconfig.cfg'):
        self.conf = ConfigParser() # 生成config对象
        self.conf = readCfg(self.conf, CFG_FILENAME)

    def getConfStr(self, sections, items, defaultvalue=""):
        """读取配置项"""
        try:
            value = self.conf.get(sections, items)
            return value
        except Exception as e:
            if defaultvalue != "":
                print(repr(e)+", will using default value: "+defaultvalue, flush=False)
            return defaultvalue

# # 获取打开的目录或文件列表
import tkinter as tk
from tkinter import filedialog

def tkGetOpenPath(): 
    """获取打开的目录地址"""
    root = tk.Tk()
    root.withdraw()
    return filedialog.askdirectory() # 选择目录，返回目录名

def tkGetOpenfileFullName():
    """获取指定文件的文件名（包含绝对路径）"""
    root = tk.Tk()
    root.withdraw()
    return filedialog.askopenfilename() # 只打开能选择单个文件

def tkGetOpenfilesPath(): 
    """获取（多个）文件的文件名"""
    root = tk.Tk()
    root.withdraw()
    # return filedialog.askopenfilename() # 只打开能选择单个文件
    return filedialog.askopenfilenames() # 同时选取多个文件返回文件路径列表


# # 模拟按键输入
try:
    from pynput.keyboard import Key, Controller
except:
    print('module not found, "pip install pynput"')

class AlanKeyboardCtrl:
    def __init__(self):
        self.k = Controller()

    def keyboardPressKey(self, key, delay=0.3):
        """模拟按键按下Alt+F4"""
        key = key.lower()
        if re.fullmatch(r'[a-z0-9_]{1}', key) != None:
            self.k.press(key)
            self.k.release(key)
        elif 'backspace' == key:
            self.k.press(Key.backspace.value)
            self.k.release(Key.backspace.value)
        elif 'delete' == key:
            self.k.press(Key.delete.value)
            self.k.release(Key.delete.value)
        elif 'ctrl' == key:
            self.k.press(Key.ctrl.value)
            self.k.release(Key.ctrl.value)
        elif 'shift' == key:
            self.k.press(Key.shift.value)
            self.k.release(Key.shift.value)
        elif 'alt' == key:
            self.k.press(Key.alt.value)
            self.k.release(Key.alt.value)
        elif 'enter' == key:
            self.k.press(Key.enter.value)
            self.k.release(Key.enter.value)
        elif 'tab' == key:
            self.k.press(Key.tab.value)
            self.k.release(Key.tab.value)
        elif 'up' == key:
            self.k.press(Key.up.value)
            self.k.release(Key.up.value)
        elif 'down' == key:
            self.k.press(Key.down.value)
            self.k.release(Key.down.value)
        elif 'left' == key:
            self.k.press(Key.left.value)
            self.k.release(Key.left.value)
        elif 'right' == key:
            self.k.press(Key.right.value)
            self.k.release(Key.right.value)
        time.sleep(delay)

    def keyboardCtrlPlus(self, stri):
        """模拟按键按下Ctrl+任意字母"""
        if re.fullmatch(r'[A-Za-z]{1}', stri) == None:
            print(f"value not allow: {stri}")
            return
        stri = stri.lower()
        self.k.press(Key.ctrl.value)
        self.k.press(stri)
        self.k.release(stri)
        self.k.release(Key.ctrl.value)

    def keyboardAltF4(self):
        """模拟按键按下Alt+F4"""
        self.k.press(Key.alt.value)
        self.k.press(Key.f4.value)
        self.k.release(Key.f4.value)
        self.k.release(Key.alt.value)

    def keyboardTypeString(self, stri):
        """按键模拟输入字符"""
        for character in stri:
            self.keyboardPressKey(character, delay=0.1)

    def keyboardClipInput(self, stri, enter=False):
        """利用剪切板输入字符"""
        setTextWithClipboard(stri)
        self.keyboardCtrlPlus('v')
        if True == enter:
            self.k.press(Key.enter.value)
            self.k.release(Key.enter.value)

# # 多线程
import threading

class AlanCallbackThread(threading.Thread):
    def __init__(self, func, args=None):
        super(AlanCallbackThread, self).__init__()
        self.func = func
        self.args = args
        self.result = None

    def run(self):
        if self.args == None:
            self.result = self.func()
        else:
            self.result = self.func(self.args)

    def get_result(self):
        """获取回调返回值"""
        try:
            return self.result
        except Exception:
            return None

    def get_enumerate(self):
        """
        返回线程池中正在运行的线程数量，
        当结果为1时，线程全部结束
        """
        return threading.enumerate()

def waitThreadEnd(tempthread, endnum=1):
    """等待线程全部结束"""
    while True:  
        if len(tempthread.get_enumerate()) == endnum:
            break
