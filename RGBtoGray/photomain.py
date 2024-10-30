import os, signal
import tkinter as tk
from PIL import ImageTk
from tkinter import ttk
from photo import photo
from tkinter import filedialog
from arraytobin import arraytobin

Stn_Gray_Place = 170
Stn_save2_Place = 200
Stn_save_Place = 230

def del_fun(component):
    component.destroy()

def hide_fun(component):
    component.place(x=-1000, y=-1000)

root = tk.Tk()  # 这个库里面有Tk()这个方法，这个方法的作用就是创建一个窗口
root.title('图片转数组工具')
root.geometry("700x500+300+80")  # (宽度x高度)+(x轴+y轴)

btnopen = tk.Button(root, text="打开图片", width=8, height=1, font=("黑体", 8), bg='#D8C8CE', fg="black")# 创建按钮，并且将按钮放到窗口里面
btnopen.place(x=10, y=30)
btnstart = tk.Button(root, text="灰度化", width=8, height=1, font=("黑体", 8), bg='#D8C8CE', fg="black")# 创建按钮，并且将按钮放到窗口里面
btnstart.place(x=10, y=Stn_Gray_Place)
btnsave = tk.Button(root, text="自动保存", width=8, height=1, font=("黑体", 8), bg='#D8C8CE', fg="black")# 创建按钮，并且将按钮放到窗口里面
hide_fun(btnsave)
btnsave2 = tk.Button(root, text="另存为", width=8, height=1, font=("黑体", 8), bg='#D8C8CE', fg="black")# 创建按钮，并且将按钮放到窗口里面
hide_fun(btnsave2)
length = tk.Entry(root, width=8)
length.place(x=10, y=100)
height = tk.Entry(root, width=8)
height.place(x=10, y=130)

text1 = tk.Text(root, height=1, width=8, relief="flat", fg="black", cursor="arrow")
text1.place(x=10, y=70)
text1.insert('0.0', 'size:')

fill = tk.StringVar()
fillone = tk.Checkbutton(root, text="填充", variable=fill, onvalue="填充",offvalue="不填充")
fill.set("填充")
fillone.place(x=10, y=310)

fill_value = tk.Entry(root, width=8)
fill_value.place(x=10, y=330)

com = ttk.Combobox(root, width=6)     #创建下拉菜单
com.place(x=10, y=360)
com["value"] = ("128", "256", "1024", "2048", "4096")    #给下拉菜单设定值
com.current(3)     #设定下拉菜单的默认值为第3个

reversal = tk.StringVar()
reversalone = tk.Checkbutton(root, text="行列反转", variable=reversal, onvalue="反转",offvalue="不反转")
reversal.set("反转")
reversalone.place(x=10, y=290)
 
fr1 = tk.Frame(root,width=620,height=500)# 创建一个容器
fr1.configure(background='#F1EDED')
fr1.place(x=80, y=0)

img = photo()
bin = arraytobin()

# 创建Label对象，并将图片对象传递给它
label = tk.Label(fr1)
# 显示Label对象
label.place(x=0, y=0)
label_gray = tk.Label(fr1)
hide_fun(label_gray)

length_var = tk.StringVar()
length_var.set('')
length.config(textvariable=length_var)
height_var = tk.StringVar()
height_var.set('')
height.config(textvariable=height_var)
fill_var = tk.StringVar()
fill_var.set(img.fillvalue)
fill_value.config(textvariable=fill_var)

gray_flag = False

def open(e):
    global file
    global image
    file = filedialog.askopenfilename() # 只打开能选择单个文件
    img.open(file)
    image = ImageTk.PhotoImage(img.image)
    label.configure(image = image)
    hide_fun(label_gray)
    btnstart.place(x=10, y=Stn_Gray_Place)
    hide_fun(btnsave)
    hide_fun(btnsave2)
    length_var.set(img.length)
    length.config(textvariable=length_var)
    height_var.set(img.height)
    height.config(textvariable=height_var)

def start(e):
    global image_gray
    global gray_flag
    gray_flag = True
    img.imagechange()
    image_gray = ImageTk.PhotoImage(img.image_gray)
    label_gray.place(x=0, y=img.height)
    # 创建Label对象，并将图片对象传递给它
    label_gray.configure(image = image_gray)
    # 显示Label对象
    btnsave.place(x=10, y=Stn_save_Place)
    btnsave2.place(x=10, y=Stn_save2_Place)
    hide_fun(btnstart)

def pre_save():
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

def save(e):
    pre_save()
    img.outosavefile()
    bin.pocess(img.Gary_name + '_Gray.c')

def save2(e):
    pre_save()
    files = [('Text Document', '*.c'), ('All Files', '*.*')] # 文件过滤器
    filenewpath = filedialog.asksaveasfilename(filetypes=files, defaultextension='.c')  # 设置保存文件，并返回文件名，指定文件名后缀为.c
    if filenewpath.strip() != '':
        img.savefile(filenewpath)
        bin.pocess(filenewpath)
    else:
        print("do not save file")

def length_update(e):
    global image
    global image_gray
    if length.get() == '':
        return
    if length.get().isdigit() == False:
        length.delete(0, 'end')
        return
    img.length = int(length.get())
    text1.delete('1.0', tk.END)
    try:
        img.resizeimg(True)
        text1.insert('0.0', 'size:')
        text1.configure(fg="black")
    except:
        text1.insert('0.0', 'error')
        text1.configure(fg="red")
    height_var.set(img.height)
    height.config(textvariable=height_var)
    image = ImageTk.PhotoImage(img.image_resize)
    label.configure(image = image)
    if gray_flag:
        image_gray = ImageTk.PhotoImage(img.image_gray)
        label_gray.place(x=0, y=img.height)
        label_gray.configure(image = image_gray)

def height_update(e):
    global image
    global image_gray
    if height.get() == '':
        return
    if height.get().isdigit() == False:
        height.delete(0, 'end')
        return
    img.height = int(height.get())
    text1.delete('1.0', tk.END)
    try:
        img.resizeimg(False)
        text1.insert('0.0', 'size:')
        text1.configure(fg="black")
    except:
        text1.insert('0.0', 'error')
        text1.configure(fg="red")
    length_var.set(img.length)
    length.config(textvariable=length_var)
    image = ImageTk.PhotoImage(img.image_resize)
    label.configure(image = image)
    if gray_flag:
        image_gray = ImageTk.PhotoImage(img.image_gray)
        label_gray.place(x=0, y=img.height)
        label_gray.configure(image = image_gray)

def xFunc(e):
    print(com.get())            #获取选中的值方法1

def exit_all():
    del_fun(root)
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
