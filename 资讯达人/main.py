import tkinter as tk
import subprocess
from tkinter import messagebox

def run_script(script_name):
    process = subprocess.Popen(['python', script_name],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               universal_newlines=True)
    stdout, stderr = process.communicate()
    if stdout:
        text_widget.insert(tk.END, stdout)
    if stderr:
        text_widget.insert(tk.END, stderr)
    text_widget.see(tk.END) # 自动滚动到底部

def run_script1():
    run_script('D:\project\chengx\资讯达人\执行.py')
    messagebox.showinfo("提示", "雷达捕获完毕")

def run_script2():
    run_script('D:\project\chengx\资讯达人\展示.py')

# 创建主窗口
root = tk.Tk()
root.title("每日资讯")

# 创建一个文本框用于显示输出
text_widget = tk.Text(root, wrap='word', width=70, height=30)
text_widget.pack(padx=10, pady=10)

# 创建按钮A和按钮B
button_a = tk.Button(root, text="打开雷达", command=run_script1)
button_a.pack(side='left', padx=10, pady=10)

button_b = tk.Button(root, text="看看结果", command=run_script2)
button_b.pack(side='right', padx=10, pady=10)

# 运行主循环
root.mainloop()
