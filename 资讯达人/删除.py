import os
import glob

def delete_txt_files(directory):
    # 使用glob模块匹配所有的.txt文件
    txt_files = glob.glob(os.path.join(directory, '*.txt'))
    
    # 遍历找到的所有.txt文件并删除它们
    for file in txt_files:
        try:
            os.remove(file)
            print(f"Deleted: {file}")
        except Exception as e:
            print(f"Failed to delete {file}. Error: {e}")

# 指定你想要删除.txt文件的目录
directory_to_clean = 'D:\project\chengx\资讯达人'

# 调用函数
delete_txt_files(directory_to_clean)