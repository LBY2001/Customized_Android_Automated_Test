import tkinter as tk
import time

from identify import identify_function, launch_apk


# 按动按钮完成功能分析
def button_click():
    identify_function()
    print('提取完成!!\n\n')


def gui():
    # 按钮窗口
    root = tk.Tk()
    root.title("功能提取")
    root.geometry("200x200")
    button = tk.Button(root, text="提取页面功能", command=button_click)
    button.pack()
    root.mainloop()


if __name__ == '__main__':
    gui()
