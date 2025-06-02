import os
import subprocess

def run_script(script_name):
    """运行指定的Python脚本"""
    subprocess.run(['python', script_name])

def main():
    # 指定你要检查的目录
    directory = 'D:\project\chengx\资讯达人'
    
    # 检查目录中是否有.txt文件
    txt_files = [f for f in os.listdir(directory) if f.endswith('.txt')]
    
    # 如果有.txt文件，先执行1.py
    if txt_files:
        print("正在清理")
        run_script('D:\project\chengx\资讯达人\删除.py')
    

    # 无论是否有.txt文件，都执行2.py
    print("正在生成....")
    run_script('D:\project\chengx\资讯达人\生成.py')

    
    # 最后执行3.py
    print("正在整理....")
    run_script('D:\project\chengx\资讯达人整理.py')

    print("执行完成")

if __name__ == "__main__":
    main()