from tkinter import filedialog
from tkinter import *
from tkinter import ttk
from tkinter import messagebox as msg
from tkinter import scrolledtext
import sys
from icon import Icon
import os
import base64
import intelhex
import webbrowser


def resource_path(relative_path):
    '''返回资源绝对路径。'''
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller会创建临时文件夹temp
        # 并把路径存储在_MEIPASS中
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath('.')
    return os.path.join(base_path, relative_path)


def open_website(event):
    webbrowser.open("http://www.coltsmart.com", new=0)


def browse_input_button(path):
    filename = filedialog.askopenfilename(filetypes=[('HEX', '.hex')])
    print(filename)
    path.set(filename)
    return filename


def browse_output_button(path):
    filename = filedialog.askdirectory()
    print(filename)
    path.set(filename)
    return filename


def file_merge(file1, file2, output):
    output += '/Merge.hex'
    #output = os.path.join(output, '/Merge.hex')
    #output.replace('\\', '/')
    print(output)
    overlap = 'replace'
    res = intelhex.IntelHex()
    ih = intelhex.IntelHex(file1)
    try:
        res.merge(ih, overlap)
    except intelhex.AddressOverlapError:
        e = sys.exc_info()[1]  # current exception
        sys.stderr.write('Merging: ' + fname + "\n")
        sys.stderr.write(str(e) + "\n")
        return 1
    ih = intelhex.IntelHex(file2)
    try:
        res.merge(ih, overlap)
    except intelhex.AddressOverlapError:
        e = sys.exc_info()[1]  # current exception
        sys.stderr.write('Merging: ' + fname + "\n")
        sys.stderr.write(str(e) + "\n")
        return 1
    res.write_hex_file(output, False)

class window(Tk):
    def __init__(self):
        super().__init__()
        self.title("鸣驹智能Intel HEX文件合并工具")
        self.resizable(width=False, height=False)
        self.geometry()

        if sys.platform.startswith("win32"):
            self.logo = PhotoImage(file=resource_path(r'logo\logo_blue.png'))  # file：t图片路径
        elif sys.platform.startswith('darwin'):
            self.logo = PhotoImage(file=resource_path(r'logo/logo_blue.png'))  # file：t图片路径
        elif sys.platform.startswith('linux'):
            self.logo = PhotoImage(file=resource_path(r'logo/logo_blue.png'))  # file：t图片路径
        else:
            self.logo = PhotoImage(file=resource_path(r'logo/logo_blue.png'))  # file：t图片路径
        self.imgLabel = Label(self, image=self.logo, justify=LEFT, compound=LEFT, bg='grey')  # 把图片整合到标签类中
        self.imgLabel.pack(side=TOP, fill=BOTH, expand=NO, anchor=N, padx=6, pady=6)
        self.imgLabel.bind("<Button-1>", open_website)
        self.Line1 = Frame(self)
        self.Line1.pack(side=TOP, fill=BOTH, expand=NO, anchor=N, padx=6, pady=3)
        self.Line2 = Frame(self)
        self.Line2.pack(side=TOP, fill=BOTH, expand=NO, anchor=N, padx=6, pady=3)
        self.Line3 = Frame(self)
        self.Line3.pack(side=TOP, fill=BOTH, expand=NO, anchor=N, padx=6, pady=3)
        self.Line4 = Frame(self)
        self.Line4.pack(side=TOP, fill=BOTH, expand=NO, anchor=N, padx=6, pady=3)

        #self.LableFile1 = Label(self.Line1, width=10, text="请选择文件1", anchor=W)
        #self.LableFile1.pack(side=LEFT, fill=X, expand=YES, anchor=W, padx=1, pady=1)
        self.File1Var = StringVar(self.Line1, value='')
        self.File1 = Entry(self.Line1, textvariable=self.File1Var, state='normal', width=30)
        self.File1.pack(side=LEFT, fill=X, expand=YES, anchor=W, padx=1, pady=1)
        self.buttonfile1 = Button(self.Line1, text="请选择文件1", command=lambda: browse_input_button(self.File1Var))
        self.buttonfile1.pack(side=LEFT, fill=X, expand=YES, anchor=W, padx=1, pady=1)

        # self.LableFile2 = Label(self.Line2, width=10, text="请选择文件2", anchor=W)
        # self.LableFile2.pack(side=LEFT, fill=X, expand=YES, anchor=W, padx=1, pady=1)
        self.File2Var = StringVar(self.Line2, value='')
        self.File2 = Entry(self.Line2, textvariable=self.File2Var, state='normal', width=30)
        self.File2.pack(side=LEFT, fill=X, expand=YES, anchor=W, padx=1, pady=1)
        self.buttonfile2 = Button(self.Line2, text="请选择文件2", command=lambda: browse_input_button(self.File2Var))
        self.buttonfile2.pack(side=LEFT, fill=X, expand=YES, anchor=W, padx=1, pady=1)

        # self.LableFileOutput = Label(self.Line3, width=10, text="文件输出路径", anchor=W)
        # self.LableFileOutput.pack(side=LEFT, fill=X, expand=YES, anchor=W, padx=1, pady=1)
        self.FileOutputVar = StringVar(self.Line3, value='')
        self.FileOutput = Entry(self.Line3, textvariable=self.FileOutputVar, state='normal', width=30)
        self.FileOutput.pack(side=LEFT, fill=X, expand=YES, anchor=W, padx=1, pady=1)
        self.buttonfileOutput = Button(self.Line3, text="文件输出路径", command=lambda: browse_output_button(self.FileOutputVar))
        self.buttonfileOutput.pack(side=LEFT, fill=X, expand=YES, anchor=W, padx=1, pady=1)

        self.buttonfileMerge = Button(self.Line4, text="合并", command=lambda: file_merge(self.File1Var.get(), self.File2Var.get(), self.FileOutputVar.get()))
        self.buttonfileMerge.pack(side=LEFT, fill=X, expand=YES, anchor=W, padx=1, pady=1)


if __name__ == '__main__':
    mainwindow = window()
    with open('tmp.ico', 'wb') as tmp:
        tmp.write(base64.b64decode(Icon().img))
        tmp.close()
    mainwindow.iconbitmap('tmp.ico')
    os.remove('tmp.ico')
    mainwindow.mainloop()