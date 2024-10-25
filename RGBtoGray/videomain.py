import os, signal
import tkinter as tk
from PIL import ImageTk
from tkinter import ttk
from photo import photo
from video import video
from tkinter import filedialog

Text_x_Place = 10
Stn_x_Place = 30
Cek_x_Place = 20
Lab_x_Place = 50

Stn_Gray_Place = 170
Stn_save2_Place = 200
Stn_save_Place = 230

def del_fun(component):
    component.destroy()

def hide_fun(component):
    component.place(x=-1000, y=-1000)

root = tk.Tk()  # 这个库里面有Tk()这个方法，这个方法的作用就是创建一个窗口
root.title('视频转数组工具')
root.geometry("720x500+300+80")  # (宽度x高度)+(x轴+y轴)

btnopen = tk.Button(root, text="打开视频", width=8, height=1, font=("黑体", 8), bg='#D8C8CE', fg="black")# 创建按钮，并且将按钮放到窗口里面
btnopen.place(x=Stn_x_Place, y=30)
btnstart = tk.Button(root, text="开始处理", width=8, height=1, font=("黑体", 8), bg='#D8C8CE', fg="black")# 创建按钮，并且将按钮放到窗口里面
btnstart.place(x=Stn_x_Place, y=Stn_Gray_Place)
btnsave = tk.Button(root, text="自动保存", width=8, height=1, font=("黑体", 8), bg='#D8C8CE', fg="black")# 创建按钮，并且将按钮放到窗口里面
hide_fun(btnsave)
btnsave2 = tk.Button(root, text="另存为", width=8, height=1, font=("黑体", 8), bg='#D8C8CE', fg="black")# 创建按钮，并且将按钮放到窗口里面
hide_fun(btnsave2)
length = tk.Entry(root, width=8)
length.place(x=Lab_x_Place, y=100)
height = tk.Entry(root, width=8)
height.place(x=Lab_x_Place, y=130)

text1 = tk.Text(root, height=1, width=14, relief="flat", fg="black", cursor="arrow")
text1.place(x=Text_x_Place, y=80)
text1.insert('0.0', 'pixel size')

fill = tk.StringVar()
fillone = tk.Checkbutton(root, text="填充", variable=fill, onvalue="填充",offvalue="不填充")
fill.set("填充")
fillone.place(x=Cek_x_Place, y=300)

fill_value = tk.Entry(root, width=8)
fill_value.place(x=Lab_x_Place, y=330)

com = ttk.Combobox(root, width=6)     #创建下拉菜单
com.place(x=Lab_x_Place, y=360)
com["value"] = ("128", "256", "1024", "2048", "4096")    #给下拉菜单设定值
com.current(3)     #设定下拉菜单的默认值为第3个

reversal = tk.StringVar()
reversalone = tk.Checkbutton(root, text="行列反转", variable=reversal, onvalue="反转",offvalue="不反转")
reversal.set("反转")
reversalone.place(x=Cek_x_Place, y=280)
 
fr1 = tk.Frame(root,width=600,height=500)# 创建一个容器
fr1.configure(background='#F1EDED')
fr1.place(x=120, y=0)

dio = video()

# 创建Label对象，并将图片对象传递给它
label = tk.Label(fr1)
# 显示Label对象
label.place(x=0, y=0)

length_var = tk.StringVar()
length_var.set('')
length.config(textvariable=length_var)
height_var = tk.StringVar()
height_var.set('')
height.config(textvariable=height_var)
fill_var = tk.StringVar()
fill_var.set("0x00")
fill_value.config(textvariable=fill_var)

text2 = tk.Text(root, height=1, width=14, relief="flat", fg="black", cursor="arrow")
text2.place(x=Text_x_Place, y=390)
text2.insert('0.0', '')

text3 = tk.Text(root, height=1, width=14, relief="flat", fg="black", cursor="arrow")
text3.place(x=Text_x_Place, y=420)
text3.insert('0.0', '')

Pianyi = 3

text_l = tk.Text(root, height=1, width=4, relief="flat", fg="black", cursor="arrow")
text_l.place(x=Text_x_Place, y=100+Pianyi)
text_l.insert('0.0', '长：')

text_h = tk.Text(root, height=1, width=4, relief="flat", fg="black", cursor="arrow")
text_h.place(x=Text_x_Place, y=130+Pianyi)
text_h.insert('0.0', '宽：')

text_s = tk.Text(root, height=1, width=4, relief="flat", fg="black", cursor="arrow")
text_s.place(x=Text_x_Place, y=330+Pianyi)
text_s.insert('0.0', '补充字节：')

text_r = tk.Text(root, height=1, width=4, relief="flat", fg="black", cursor="arrow")
text_r.place(x=Text_x_Place, y=360+Pianyi)
text_r.insert('0.0', '片容量：')

def photo_process(i_img):
    global outputstring
    img = photo()
    img.open(i_img)
    img.imagechange()
    img.arraynmae = f'gImage_{dio.newcount}'
    img.length = int(length.get())
    img.resizeimg(True)
    img.piecesize = int(com.get())
    fillstr = fill.get()
    img.fillvalue = fill_value.get()
    if fillstr == '填充':
        img.fillflag = True
    else:
        img.fillflag = False
    reversalonestr = reversal.get()
    if reversalonestr == '反转':
        img.reversal = True
    else:
        img.reversal = False
    img.save_gray()
    outputstring += img.grayfile
    outputstring += '\n'

def open(e):
    global videofile
    global g_img
    global image1
    videofile = filedialog.askopenfilename() # 只打开能选择单个文件
    dio.open(videofile)
    dio.process()
    image = dio.getphotoname()
    g_img = photo()
    g_img.open(image)
    image1 = ImageTk.PhotoImage(g_img.image)
    label.configure(image = image1)

    text2.delete('1.0', tk.END)
    text2.insert('0.0', f'帧率:{dio.fps}')
    text3.delete('1.0', tk.END)
    text3.insert('0.0', f'帧数:{dio.frames}')

    btnstart.place(x=10, y=Stn_Gray_Place)
    hide_fun(btnsave)
    hide_fun(btnsave2)
    length_var.set(g_img.length)
    length.config(textvariable=length_var)
    height_var.set(g_img.height)
    height.config(textvariable=height_var)

def start(e):
    global outputstring
    outputstring = ''
    g_img.imagechange()
    g_img.piecesize = int(com.get())
    fillstr = fill.get()
    g_img.fillvalue = fill_value.get()
    if fillstr == '填充':
        g_img.fillflag = True
    else:
        g_img.fillflag = False
    reversalonestr = reversal.get()
    if reversalonestr == '反转':
        g_img.reversal = True
    else:
        g_img.reversal = False
    g_img.save_gray()
    outputstring += g_img.grayfile
    outputstring += '\n'

    image2 = dio.getphotoname()
    while image2 != None:
        photo_process(image2)
        image2 = dio.getphotoname()

    btnsave.place(x=10, y=Stn_save_Place)
    btnsave2.place(x=10, y=Stn_save2_Place)
    hide_fun(btnstart)

def save(e):
    dio.outosavefile(outputstring)

def save2(e):
    files = [('Text Document', '*.c'), ('All Files', '*.*')] # 文件过滤器
    filenewpath = filedialog.asksaveasfilename(filetypes=files, defaultextension='.c')  # 设置保存文件，并返回文件名，指定文件名后缀为.c
    if filenewpath.strip() != '':
        dio.savefile(filenewpath, outputstring)
    else:
        print("do not save file")

def length_update(e):
    global image
    if length.get() == '':
        return
    if length.get().isdigit() == False:
        length.delete(0, 'end')
        return
    g_img.length = int(length.get())
    text1.delete('1.0', tk.END)
    try:
        g_img.resizeimg(True)
        text1.insert('0.0', 'size:')
        text1.configure(fg="black")
    except:
        text1.insert('0.0', 'error')
        text1.configure(fg="red")
    height_var.set(g_img.height)
    height.config(textvariable=height_var)
    image = ImageTk.PhotoImage(g_img.image_resize)
    label.configure(image = image)

    btnstart.place(x=10, y=Stn_Gray_Place)
    hide_fun(btnsave)
    hide_fun(btnsave2)

def height_update(e):
    global image
    if height.get() == '':
        return
    if height.get().isdigit() == False:
        height.delete(0, 'end')
        return
    g_img.height = int(height.get())
    text1.delete('1.0', tk.END)
    try:
        g_img.resizeimg(False)
        text1.insert('0.0', 'size:')
        text1.configure(fg="black")
    except:
        text1.insert('0.0', 'error')
        text1.configure(fg="red")
    length_var.set(g_img.length)
    length.config(textvariable=length_var)
    image = ImageTk.PhotoImage(g_img.image_resize)
    label.configure(image = image)

    btnstart.place(x=10, y=Stn_Gray_Place)
    hide_fun(btnsave)
    hide_fun(btnsave2)

def xFunc(e):
    print(com.get())            #获取选中的值方法1

def exit_all():
    del_fun(root)
    dio.deletephoto()
    pid = os.getpid() # 获取当前进程的PID
    os.kill(pid, signal.SIGTERM) # 主动结束指定ID的程序运行

btnopen.bind("<Button-1>", open)
btnstart.bind("<Button-1>", start)  # 将按钮和方法进行绑定，也就是创建了一个事件
btnsave.bind("<Button-1>", save)  # 将按钮和方法进行绑定，也就是创建了一个事件
btnsave2.bind("<Button-1>", save2)  # 将按钮和方法进行绑定，也就是创建了一个事件
length.bind("<KeyRelease>", length_update)
height.bind("<KeyRelease>", height_update)
com.bind("<<ComboboxSelected>>", xFunc)     # #给下拉菜单绑定事件

root.protocol("WM_DELETE_WINDOW", exit_all)

root.mainloop()  # 让窗口一直显示，循环
