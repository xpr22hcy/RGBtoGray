import os, signal
import tkinter as tk
from PIL import ImageTk
from tkinter import ttk
from photo import photo
from video import video
from tkinter import filedialog
from arraytobin import arraytobin

Text_x_Place = 10
Stn_x_Place = 30
Cek_x_Place = 20
Lab_x_Place = 50

Frame_x_Place = 120

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
hide_fun(btnstart)
btnsave = tk.Button(root, text="自动保存", width=8, height=1, font=("黑体", 8), bg='#D8C8CE', fg="black")# 创建按钮，并且将按钮放到窗口里面
hide_fun(btnsave)
btnsave2 = tk.Button(root, text="另存为", width=8, height=1, font=("黑体", 8), bg='#D8C8CE', fg="black")# 创建按钮，并且将按钮放到窗口里面
hide_fun(btnsave2)
btncut = tk.Button(root, text="准备剪切", width=8, height=1, font=("黑体", 8), bg='#D8C8CE', fg="black")# 创建按钮，并且将按钮放到窗口里面
hide_fun(btncut)
length = tk.Entry(root, width=8)
length.place(x=Lab_x_Place, y=100)
height = tk.Entry(root, width=8)
height.place(x=Lab_x_Place, y=130)

text1 = tk.Text(root, height=1, width=14, relief="flat", fg="black", cursor="arrow")
text1.place(x=Text_x_Place, y=80)
text1.insert('0.0', 'pixel size')
text1.configure(state=tk.DISABLED)

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
 
fr1 = tk.Frame(root,width=1800,height=900)# 创建一个容器
fr1.configure(background='#F1EDED')
fr1.place(x=Frame_x_Place, y=0)

# 创建Label对象，并将图片对象传递给它
label = tk.Label(fr1)
# 显示Label对象
hide_fun(label)

vertical = tk.Frame(fr1, bg="red", height=1, width=1)
vertical2 = tk.Frame(fr1, bg="red", height=1, width=1)
horizontal = tk.Frame(fr1, bg="red", height=1, width=1)
horizontal2 = tk.Frame(fr1, bg="red", height=1, width=1)
hide_fun(vertical)
hide_fun(vertical2)
hide_fun(horizontal)
hide_fun(horizontal2)

dio = video()
g_img = photo()
bin = arraytobin()

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
text2.configure(state=tk.DISABLED)

text3 = tk.Text(root, height=1, width=14, relief="flat", fg="black", cursor="arrow")
text3.place(x=Text_x_Place, y=420)
text3.insert('0.0', '')
text3.configure(state=tk.DISABLED)

Pianyi = 3

text_l = tk.Text(root, height=1, width=4, relief="flat", fg="black", cursor="arrow")
text_l.place(x=Text_x_Place, y=100+Pianyi)
text_l.insert('0.0', '长：')
text_l.configure(state=tk.DISABLED)

text_h = tk.Text(root, height=1, width=4, relief="flat", fg="black", cursor="arrow")
text_h.place(x=Text_x_Place, y=130+Pianyi)
text_h.insert('0.0', '宽：')
text_h.configure(state=tk.DISABLED)

text_s = tk.Text(root, height=1, width=4, relief="flat", fg="black", cursor="arrow")
text_s.place(x=Text_x_Place, y=330+Pianyi)
text_s.insert('0.0', '填充字节：')
text_s.configure(state=tk.DISABLED)

text_r = tk.Text(root, height=1, width=4, relief="flat", fg="black", cursor="arrow")
text_r.place(x=Text_x_Place, y=360+Pianyi)
text_r.insert('0.0', '片容量：')
text_r.configure(state=tk.DISABLED)

X1 = 0
Y1 = 0
X2 = 0
Y2 = 0
cut_flag = False

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
    outputstring += img.data
    outputstring += '\n\n'

def open(e):
    global videofile
    global g_img
    global image1
    global X1
    global Y1
    global X2
    global Y2
    global cut_flag
    X1 = 0
    Y1 = 0
    X2 = 0
    Y2 = 0
    cut_flag = False
    videofile = filedialog.askopenfilename() # 只打开能选择单个文件
    dio.open(videofile)
    dio.process()
    image = dio.getphotoname()
    g_img.open(image)
    image1 = ImageTk.PhotoImage(g_img.image)
    label.configure(image = image1)
    label.place(x=0, y=0)

    text2.configure(state=tk.NORMAL)
    text2.delete('1.0', tk.END)
    text2.insert('0.0', f'帧率:{dio.fps}')
    text2.configure(state=tk.DISABLED)
    text3.configure(state=tk.NORMAL)
    text3.delete('1.0', tk.END)
    text3.insert('0.0', f'帧数:{dio.frames}')
    text3.configure(state=tk.DISABLED)

    btnstart.place(x=Stn_x_Place, y=Stn_Gray_Place)
    btncut.place(x=Stn_x_Place, y=Stn_save2_Place)
    hide_fun(btnsave)
    hide_fun(btnsave2)
    length_var.set(g_img.length)
    length.config(textvariable=length_var)
    height_var.set(g_img.height)
    height.config(textvariable=height_var)
    btncut.configure(text='准备剪切')
    btncut.update()

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
    outputstring += g_img.data
    outputstring += '\n\n'

    num = 1
    image2 = dio.getphotoname()
    while image2 != None:
        photo_process(image2)
        image2 = dio.getphotoname()
        num += 1

    startstring = f'const unsigned char gImage[{num*g_img.num}] = '
    startstring += "{\n"
    outputstring = startstring + outputstring
    outputstring += "};"
    
    btnsave.place(x=10, y=Stn_save_Place)
    btnsave2.place(x=10, y=Stn_save2_Place)
    hide_fun(btnstart)
    hide_fun(btncut)

def writeline(x1, y1, x2, y2):
    vertical.configure(height=y2 - y1)
    vertical2.configure(height=y2 - y1)
    horizontal.configure(width=x2 - x1)
    horizontal2.configure(width=x2 - x1)
    vertical.place(x=x1+1, y=y1+1)
    horizontal.place(x=x1+1, y=y1+1)
    vertical2.place(x=x2+1, y=y1+1)
    horizontal2.place(x=x1+1, y=y2+1)
    length_var.set(x2 - x1)
    length.config(textvariable=length_var)
    height_var.set(y2 - y1)
    height.config(textvariable=height_var)

def fun1(e):
    global X1
    global Y1
    if e.x >= 0 and e.y >= 0:
        if e.x <= g_img.length and e.y <= g_img.height:
            X1 = e.x
            Y1 = e.y
            writeline(X1, Y1, X2, Y2)

def fun2(e):
    global X2
    global Y2
    if e.x <= 0 and e.y <= 0:
        if e.x >= -g_img.length and e.y >= -g_img.height:
            X2 = e.x + g_img.length
            Y2 = e.y + g_img.height
            writeline(X1, Y1, X2, Y2)

btn1 = tk.Button(root, text="", width=1, height=1, font=("黑体", 8), fg="black")
hide_fun(btn1)
btn1.bind("<B1-Motion>", fun1)
btn2 = tk.Button(root, text="", width=1, height=1, font=("黑体", 8), fg="black")
hide_fun(btn2)
btn2.bind("<B1-Motion>", fun2)

def startcut(e):
    global g_img
    global cut_flag
    global X2
    global Y2
    global image1
    if cut_flag == False:
        cut_flag = True
        X2 = g_img.length
        Y2 = g_img.height
        writeline(X1, Y1, X2, Y2)

        btn1.place(x=Frame_x_Place-16, y=0)
        btn2.place(x=Frame_x_Place+2+X2, y=2+Y2)

        btncut.configure(text='确定剪切')
        btncut.update()
        hide_fun(btnstart)
    else:
        cut_flag = False
        dio.cropimg(X1, Y1, X2, Y2)
        image = dio.getphotoname()
        g_img.open(image)
        image1 = ImageTk.PhotoImage(g_img.image)
        label.configure(image = image1)
        label.place(x=0, y=0)
        length_var.set(g_img.length)
        length.config(textvariable=length_var)
        height_var.set(g_img.height)
        height.config(textvariable=height_var)

        btncut.configure(text='准备剪切')
        btncut.update()
        btnstart.place(x=Stn_x_Place, y=Stn_Gray_Place)
        hide_fun(btn1)
        hide_fun(btn2)
        hide_fun(vertical)
        hide_fun(horizontal)
        hide_fun(vertical2)
        hide_fun(horizontal2)

    return

def save(e):
    dio.outosavefile(outputstring)
    bin.pocess(dio.Array_name + '_Gray.c')
    # dio.restart()

def save2(e):
    files = [('Text Document', '*.c'), ('All Files', '*.*')] # 文件过滤器
    filenewpath = filedialog.asksaveasfilename(filetypes=files, defaultextension='.c')  # 设置保存文件，并返回文件名，指定文件名后缀为.c
    if filenewpath.strip() != '':
        dio.savefile(filenewpath, outputstring)
        bin.pocess(filenewpath)
    else:
        print("do not save file")
    # dio.restart()

def length_update(e):
    global image
    if length.get() == '':
        return
    if length.get().isdigit() == False:
        length.delete(0, 'end')
        return
    g_img.length = int(length.get())
    text1.configure(state=tk.NORMAL)
    text1.delete('1.0', tk.END)
    try:
        g_img.resizeimg(True)
        text1.insert('0.0', 'size:')
        text1.configure(fg="black")
    except:
        text1.insert('0.0', 'error')
        text1.configure(fg="red")
    text1.configure(state=tk.DISABLED)
    height_var.set(g_img.height)
    height.config(textvariable=height_var)
    image = ImageTk.PhotoImage(g_img.image_resize)
    label.configure(image = image)

    btnstart.place(x=Stn_x_Place, y=Stn_Gray_Place)
    btncut.place(x=Stn_x_Place, y=Stn_Gray_Place)
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
    text1.configure(state=tk.NORMAL)
    text1.delete('1.0', tk.END)
    try:
        g_img.resizeimg(False)
        text1.insert('0.0', 'size:')
        text1.configure(fg="black")
    except:
        text1.insert('0.0', 'error')
        text1.configure(fg="red")
    text1.configure(state=tk.DISABLED)
    length_var.set(g_img.length)
    length.config(textvariable=length_var)
    image = ImageTk.PhotoImage(g_img.image_resize)
    label.configure(image = image)

    btnstart.place(x=Stn_x_Place, y=Stn_Gray_Place)
    btncut.place(x=Stn_x_Place, y=Stn_Gray_Place)
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
btncut.bind("<Button-1>", startcut)
length.bind("<KeyRelease>", length_update)
height.bind("<KeyRelease>", height_update)
com.bind("<<ComboboxSelected>>", xFunc)     # #给下拉菜单绑定事件


root.protocol("WM_DELETE_WINDOW", exit_all)

root.mainloop()  # 让窗口一直显示，循环
