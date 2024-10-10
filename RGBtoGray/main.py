import cv2
from alanbasepy import *
import os
# import numpy as np
# np.set_printoptions(threshold=np.inf) #设置打印不省略

FILENAME = 'array_bytes.c'
NEWPHOTONAME = 'Gray_'

Cfg = AlanCfg('./')
if 'True' == Cfg.getConfStr('photo', 'UseTkWindow', 'True'):
    # 使用 Tk 窗口获取文件路径及文件名
    filename = tkGetOpenfileFullName()

(filepath, tempfilename) = os.path.split(filename)# 分离路径和文件名
(filename_noext, extension) = os.path.splitext(tempfilename)#分离文件名和后缀
generatefilepath = "./" + filename_noext +"/"
print(generatefilepath)
NEWPHOTOPATH = generatefilepath + NEWPHOTONAME + tempfilename

#1、读取图像，并把图像转换为灰度图像并显示
img = cv2.imread(filename)  #读取图片
im_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)   #转换了灰度化

cv2.imshow("test_imread", im_gray)
cv2.waitKey()

array_bytes = [[]]

num = 0
s = 0
for i in im_gray:
    array = []
    m = 0
    for j in i:
        num += 1
        stri = hex(im_gray[s][m])
        stri = stri[2:].zfill(2)
        stri = f'0x{stri}'
        array.append(stri)
        m += 1
    s += 1
    array_bytes.append(array)

content = str(array_bytes)
content = content.replace('[[], [', '')
content = content.replace('\'', '')
content = content.replace('], [', ',\n')
content = content.replace('[', '')
content = content.replace(']', '')

# content = str(im_gray)
# content = ','.join(content.split())
# content = content.replace('[,', '')
# content = content.replace('],', ',\n')
# content = content.replace('[', '')
# content = content.replace(']', '')

string = f'const unsigned char gImage_[{num}] = '
string += "{\n"
string += content
string += "\n};"

mkUserDir(generatefilepath)
delPathAllFile(generatefilepath)
writeFile(generatefilepath + FILENAME, 'w+', string, end='')
print("已生成测试步骤文件")

cv2.imwrite(NEWPHOTOPATH, im_gray)
