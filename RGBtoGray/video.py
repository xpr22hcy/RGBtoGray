import cv2
from alanbasepy import *
from PIL import Image

class video:
    def __init__(self):
        self.pathSave = None
        return

    def open(self, file):
        #间隔多少帧取一张图片
        self.skipNum = 0  #注：间隔0帧取一个图；
        self.count = 0
        self.newcount = 0
        self.crop_flag = False

        if self.pathSave is not None:
            self.deletephoto()
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
        self.Array_name = filepath + "/" + filename_noext

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
                # cv2.waitKey(1)
            else:
                self.count = count
                print("视屏处理完毕！")
                break
        self.videoCapture.release()

    def restart(self):
        self.newcount = 0

    def getphotoname(self):
        self.newcount += 1
        if self.newcount > self.count:
            return None
        if self.crop_flag == False:
            return self.pathSave + f'{self.photoname}_{format(self.newcount)}.bmp'
        else:
            return self.pathSave + f'Crop_{self.photoname}_{format(self.newcount)}.bmp'

    def cropimg(self, x1, y1, x2, y2):
        self.crop_flag = True
        self.newcount = 0
        for i in range(self.count):
            img = cv2.imread(self.pathSave + f'{self.photoname}_{format(i+1)}.bmp')
            cropped = img[y1:y2, x1:x2]  # 裁剪坐标为[y0:y1, x0:x1]
            cv2.imwrite(self.pathSave + f'Crop_{self.photoname}_{format(i+1)}.bmp', cropped)

    def outosavefile(self, str):
        writeFile(self.Array_name + '_Gray.c', 'w+', str, end='')
        print("已生成文件")

    def savefile(self, name, str):
        writeFile(name, 'w+', str, end='')
        print("已生成文件")

    def deletephoto(self):
        if fileExists(self.pathSave):
            delPathAllFile(self.pathSave)
            os.rmdir(self.pathSave)

# 修改视频帧率为指定帧率，分辨率保持不变
def modify_video_frame_rate(videoPath, destFps):
    dir_name = os.path.dirname(videoPath)
    basename = os.path.basename(videoPath)
    # video_name = basename[:basename.rfind('.')]
    video_name = './jdsfu'
    video_name = video_name + "moify_fps_rate"
    resultVideoPath = f'{dir_name}/{video_name}.mp4'

    videoCapture = cv2.VideoCapture(videoPath)

    fps = videoCapture.get(cv2.CAP_PROP_FPS)
    if fps != destFps:
        frameSize = (int(videoCapture.get(cv2.CAP_PROP_FRAME_WIDTH)), int(videoCapture.get(cv2.CAP_PROP_FRAME_HEIGHT)))

        #这里的VideoWriter_fourcc需要多测试，如果编码器不对则会提示报错，根据报错信息修改编码器即可
        videoWriter = cv2.VideoWriter(resultVideoPath,cv2.VideoWriter_fourcc('m','p','4','v'),destFps,frameSize)

        i = 0
        while True:
            success,frame = videoCapture.read()
            if success:
                i+=1
                print('转换到第%d帧' % i)
                videoWriter.write(frame)
            else:
                print('帧率转换结束')
                break

if __name__ == '__main__':
    videofile = filedialog.askopenfilename()
    modify_video_frame_rate(videofile, 50)

