from alanbasepy import *
import os
from PIL import Image
import numpy as np
np.set_printoptions(threshold=np.inf) #设置打印不省略

def PIL_crop(path, savepath, x1, x2, y1, y2):
    img=Image.open(path)

    #图片剪切crop(x,y,x1,y1)
    im=img.crop((x1, y1, x2, y2))
    
    #保存剪切出来的图片
    im.save(savepath)

def deletephoto(path):
    if fileExists(path):
        delPathAllFile(path)
        os.rmdir(path)

class photo:
    def __init__(self):
        self.piecesize = 2048
        self.filesize = self.piecesize
        self.fillvalue = '0x00'
        self.fillflag = True
        self.reversal = True
        self.arraynmae = 'gImage_1'
        return

    def open(self, file):
        self.filename = file
        (filepath, tempfilename) = os.path.split(self.filename)# 分离路径和文件名
        (filename_noext, extension) = os.path.splitext(tempfilename)#分离文件名和后缀
        self.Gary_name = filepath +"/" + filename_noext
        self.image = Image.open(self.filename)
        self.image_array = np.array(self.image)
        self.length = self.image.size[0]
        self.height = self.image.size[1]
        self.image_resize = self.image

    def imagechange(self):
        if len(self.image_array.shape) == 2: # 8bit
            self.image_gray = self.image_resize
            self.image_gray_array = np.array(self.image_gray)
        else:
            self.image_gray = self.image_resize.convert('L')
            self.image_gray_array = np.array(self.image_gray)
        # if len(self.image_array.shape) == 3:
        #     if self.image_array.shape[2] == 2: # 16bit
        #         self.image_gray = self.image.convert('L')
        #         self.image_array = np.array(self.image_gray)
        #     elif self.image_array.shape[2] == 3: # 24bit
        #         self.image_gray = self.image.convert('L')
        #         self.image_array = np.array(self.image_gray)

    def resizeimg(self, flag):
        if flag:
            self.height = int(self.image.size[1] * self.length / self.image.size[0])
            self.image_resize = self.image.resize((self.length, self.height))
        else:
            self.length = int(self.image.size[0] * self.height / self.image.size[1])
            self.image_resize = self.image.resize((self.length, self.height))
        self.filesize = self.piecesize
        if len(self.image_array.shape) == 2: # 8bit
            self.image_gray = self.image_resize
            self.image_gray_array = np.array(self.image_gray)
            print(self.image_array)
        else:
            self.image_gray = self.image_resize.convert('L')
            self.image_gray_array = np.array(self.image_gray)
            # print(np.array(self.image_resize))

    def save_gray(self):
        self.num = self.image_gray.size[0] * self.image_gray.size[1]

        self.array_bytes = []
        self.array_bytes_column = []

        s = 0
        for i in self.image_gray_array:
            array = []
            m = 0
            for j in i:
                stri = hex(self.image_gray_array[s][m])
                stri = stri[2:].zfill(2)
                stri = f'0x{stri}'
                array.append(stri)

                if s == 0:
                    self.array_bytes_column.append([])
                self.array_bytes_column[m].append(stri)

                m += 1
            s += 1
            self.array_bytes.append(array)
        if self.reversal:
            self.__generate(self.array_bytes_column)
        else:
            self.__generate(self.array_bytes)

    def __generate(self, Gray_bytes):
        content = str(Gray_bytes)
        content = content.replace('\'', '')
        content = content.replace('], [', ',\n')
        content = content.replace('[', '')
        content = content.replace(']', '')

        if self.fillflag:
            print(self.num)
            while self.num > self.filesize:
                self.filesize += self.piecesize
            filllength = self.filesize - self.num
            self.num = self.filesize

        if self.reversal:
            linelength = self.image_gray.size[1]
        else:
            linelength = self.image_gray.size[0]

        string = f'const unsigned char {self.arraynmae}[{self.num}] = '
        string += "{\n"

        self.data = content
        if self.fillflag:
            self.fill_string = ','
            nextlength = filllength
            while nextlength > 0:
                self.fill_string += '\n'
                for i in range(linelength):
                    nextlength -= 1
                    if i != 0:
                        self.fill_string += f' '
                    self.fill_string += f'{self.fillvalue},'
                    if nextlength == 0:
                        break
            self.data += self.fill_string

        string += self.data
        string += "\n};"
        self.grayfile = string

    def outosavefile(self):
        self.save_gray()
        writeFile(self.Gary_name + '_Gray.c', 'w+', self.grayfile, end='')
        print("已生成文件")

    def savefile(self, name):
        self.save_gray()
        writeFile(name, 'w+', self.grayfile, end='')
        print("已生成文件")
        # self.image.save(self.NEWPHOTOPATH)
        # print("已生成灰度图片")
