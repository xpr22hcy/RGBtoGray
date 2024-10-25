import cv2
from alanbasepy import *
from PIL import Image

NEWPHOTONAME = 'Gray_'

class video:
    def __init__(self):
        #间隔多少帧取一张图片
        self.skipNum = 0  #注：间隔0帧取一个图；
        self.count = 0
        self.newcount = 0
        self.pathSave = None
        return

    def open(self, file):
        if self.pathSave is not None:
            self.deletephoto(self.pathSave)
        self.filename = file
        (filepath, tempfilename) = os.path.split(self.filename)# 分离路径和文件名
        (filename_noext, extension) = os.path.splitext(tempfilename)#分离文件名和后缀
        # 视屏获取
        self.videoCapture=cv2.VideoCapture(file)
        # 帧率(frames per second)
        self.fps = self.videoCapture.get(cv2.CAP_PROP_FPS)
        # 总帧数(frames)
        self.frames = self.videoCapture.get(cv2.CAP_PROP_FRAME_COUNT)
        print("视频帧率：",self.fps)
        print("视频总帧数：",self.frames)

        #图片存储地址：
        self.pathSave = filepath + f'/rgb_{filename_noext}/'
        self.photoname = filename_noext
        self.generatefilepath = filepath +"/"
        self.generatefilename = NEWPHOTONAME + filename_noext + '.c'

    def process(self):
        delPathAllFile(self.pathSave)
        mkUserDir(self.pathSave)
        count = 0
        while (True):
            ret,frame = self.videoCapture.read()
            if(ret):
                if(count%(self.skipNum+1) == 0):
                    # imgName = "{:.6f}".format(time.time()+1.0*self.skipNum/self.fps-0.001*self.skipNum)
                    imgName = f'{self.photoname}_{format(count+1)}'
                    cv2.imwrite(self.pathSave + imgName + '.bmp', frame)
                count += 1
                cv2.waitKey(1)
            else:
                self.count = count
                print("视屏处理完毕！")
                break
        self.videoCapture.release()

    def getphotoname(self):
        self.newcount += 1
        if self.newcount > self.count:
            return None
        return self.pathSave + f'{self.photoname}_{format(self.count)}.bmp'

    def outosavefile(self, str):
        writeFile(self.generatefilepath + self.generatefilename, 'w+', str, end='')
        print("已生成文件")

    def savefile(self, name, str):
        writeFile(name, 'w+', str, end='')
        print("已生成文件")

    def deletephoto(self):
        if fileExists(self.pathSave):
            delPathAllFile(self.pathSave)
            os.rmdir(self.pathSave)
