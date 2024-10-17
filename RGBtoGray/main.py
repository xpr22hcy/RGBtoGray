from alanbasepy import *
import os
from PIL import Image
import numpy as np
np.set_printoptions(threshold=np.inf) #设置打印不省略

FILENAME = 'array_bytes.c'
NEWPHOTONAME = 'Gray_'

Cfg = AlanCfg('./')
if 'True' == Cfg.getConfStr('photo', 'UseTkWindow', 'True'):
    # 使用 Tk 窗口获取文件路径及文件名
    filename = tkGetOpenfileFullName()

(filepath, tempfilename) = os.path.split(filename)# 分离路径和文件名
(filename_noext, extension) = os.path.splitext(tempfilename)#分离文件名和后缀
generatefilepath = "./" + filename_noext +"/"
NEWPHOTOPATH = generatefilepath + NEWPHOTONAME + tempfilename

image = Image.open(filename)
image_array = np.array(image)
if len(image_array.shape) == 3:
    if image_array.shape[2] == 2: # 16bit
        image = image.convert('L')
        image_array = np.array(image)
    elif image_array.shape[2] == 3: # 24bit
        image = image.convert('L')
        image_array = np.array(image)

num = image_array.shape[0] * image_array.shape[1]

array_bytes = []
array_bytes_column = []

s = 0
for i in image_array:
    array = []
    m = 0
    for j in i:
        stri = hex(image_array[s][m])
        stri = stri[2:].zfill(2)
        stri = f'0x{stri}'
        array.append(stri)

        if s == 0:
            array_bytes_column.append([])
        array_bytes_column[m].append(stri)

        m += 1
    s += 1
    array_bytes.append(array)

content = str(array_bytes)
content = content.replace('\'', '')
content = content.replace('], [', ',\n')
content = content.replace('[', '')
content = content.replace(']', '')

string = f'const unsigned char gImage_[{num}] = '
string += "{\n"
string += content
string += "\n};"

content = str(array_bytes_column)
content = content.replace('\'', '')
content = content.replace('], [', ',\n')
content = content.replace('[', '')
content = content.replace(']', '')

string += f'\n\n/* 在原数组的基础上行与列交换过的数组 */ '
string += f'\nconst unsigned char gImage_column[{num}] = '
string += "{\n"
string += content
string += "\n};"

mkUserDir(generatefilepath)
delPathAllFile(generatefilepath)
writeFile(generatefilepath + FILENAME, 'w+', string, end='')
print("已生成测试步骤文件")

image.save(NEWPHOTOPATH)
print("已生成灰度图片")
