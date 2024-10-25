from alanbasepy import *
import os
from PIL import Image
import numpy as np
# np.set_printoptions(threshold=np.inf) #设置打印不省略

NEWPHOTONAME = 'Gray_'

class photo:
    def __init__(self, file):
        self.__open(file)

    def reinit(self, file):
        self.__open(file)

    def __open(self, file):
        self.filename = file
        (filepath, tempfilename) = os.path.split(self.filename)# 分离路径和文件名
        (filename_noext, extension) = os.path.splitext(tempfilename)#分离文件名和后缀
        self.generatefilepath = filepath +"/"
        self.generatefilename = NEWPHOTONAME + filename_noext + '.c'
        self.image = Image.open(self.filename)
        self.image_array = np.array(self.image)
        self.length = self.image.size[0]
        self.height = self.image.size[1]
        self.image_resize = self.image
        self.piecesize = 2048
        self.filesize = self.piecesize
        self.fillvalue = '0x00'

    def imagechange(self):
        if len(self.image_array.shape) == 2: # 8bit
            self.image_gray = self.image_resize
            self.image_array = np.array(self.image_gray)
        else:
            self.image_gray = self.image_resize.convert('L')
            self.image_array = np.array(self.image_gray)
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
            self.image_array = np.array(self.image_gray)
        else:
            self.image_gray = self.image_resize.convert('L')
            self.image_array = np.array(self.image_gray)

    def __save_gray(self, fillflag):
        self.num = self.image_gray.size[0] * self.image_gray.size[1]

        self.array_bytes = []
        self.array_bytes_column = []

        s = 0
        for i in self.image_array:
            array = []
            m = 0
            for j in i:
                stri = hex(self.image_array[s][m])
                stri = stri[2:].zfill(2)
                stri = f'0x{stri}'
                array.append(stri)

                if s == 0:
                    self.array_bytes_column.append([])
                self.array_bytes_column[m].append(stri)

                m += 1
            s += 1
            self.array_bytes.append(array)
        self.__generate(fillflag)

    def __generate(self, fillflag):
        content = str(self.array_bytes)
        content = content.replace('\'', '')
        content = content.replace('], [', ',\n')
        content = content.replace('[', '')
        content = content.replace(']', '')

        if fillflag:
            while self.num > self.filesize:
                self.filesize += self.piecesize
            filllength = self.filesize - self.num
            self.num = self.filesize

        string = f'const unsigned char gImage_[{self.num}] = '
        string += "{\n"
        string += content
        if fillflag:
            self.fill_string = ','
            nextlength = filllength
            while nextlength > 0:
                self.fill_string += '\n'
                for i in range(self.image_gray.size[0]):
                    nextlength -= 1
                    if i != 0:
                        self.fill_string += f' '
                    self.fill_string += f'{self.fillvalue},'
            string += self.fill_string
        string += "\n};"

        content = str(self.array_bytes_column)
        content = content.replace('\'', '')
        content = content.replace('], [', ',\n')
        content = content.replace('[', '')
        content = content.replace(']', '')

        string += f'\n\n/* 在原数组的基础上行与列交换过的数组 */ '
        string += f'\nconst unsigned char gImage_column[{self.num}] = '
        string += "{\n"
        string += content
        if fillflag:
            self.fill_string = ','
            nextlength = filllength
            while nextlength > 0:
                self.fill_string += '\n'
                for i in range(self.image_gray.size[1]):
                    nextlength -= 1
                    if i != 0:
                        self.fill_string += f' '
                    self.fill_string += f'{self.fillvalue},'
            string += self.fill_string
        string += "\n};"
        self.grayfile = string

    def outosavefile(self, fillflag):
        self.__save_gray(fillflag)
        writeFile(self.generatefilepath + self.generatefilename, 'w+', self.grayfile, end='')
        print("已生成文件")

    def savefile(self, name, fillflag):
        self.__save_gray(fillflag)
        writeFile(name, 'w+', self.grayfile, end='')
        print("已生成文件")
        # self.image.save(self.NEWPHOTOPATH)
        # print("已生成灰度图片")
