import subprocess     # 用于调用外部命令或运行其他Python脚本
import os             # 提供与操作系统交互的功能，如检查文件是否存在
import time           # 提供时间相关功能，如暂停执行
from concurrent.futures import ThreadPoolExecutor  # 提供线程池执行器，用于并发执行任务

# 定义一个函数来运行单个爬虫脚本，具有重试机制
def run_spider(script_name):
    max_retries = 3  # 设置最大重试次数
    retry_delay = 5  # 设置两次尝试之间的延迟时间（秒）

    # 尝试运行脚本，直到成功或达到最大重试次数
    for attempt in range(max_retries):
        # 首先检查脚本文件是否存在
        if os.path.exists(script_name):
            print(f"Attempt {attempt + 1}: Running {script_name}...")  # 打印尝试运行的信息
            result = subprocess.run(["python", script_name])  # 使用subprocess运行脚本

            # 如果脚本成功运行（返回码为0），打印成功信息并退出函数
            if result.returncode == 0:
                print(f"{script_name} completed successfully.")
                return
            
            # 如果脚本运行失败但未达到最大重试次数，打印失败信息并等待后重试
            elif attempt < max_retries - 1:
                print(f"{script_name} failed. Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)  # 等待一段时间再重试
                
            # 如果脚本运行失败且已达到最大重试次数，打印最终失败信息
            else:
                print(f"{script_name} failed after {max_retries} attempts.")
                
        # 如果脚本文件不存在，打印警告信息并退出函数
        else:
            print(f"Warning: File {script_name} not found. Skipping.")
            return

# 主函数，定义爬虫脚本的列表并使用线程池执行器并发运行它们
if __name__ == "__main__":
    spiders = [
    "安全客.py",
    "安全牛.py",
    "华为.py",
    "绿盟.py",
    "美团技术.py",
    "嘶吼.py",
    "腾讯玄武.py",
    "FreeBuf.py",
    "SeebugPaper.py",
    "Seebug.py"
]

    
    # 创建一个线程池执行器，用于并发执行任务
    with ThreadPoolExecutor() as executor:
        # 提交每个爬虫脚本的任务到线程池执行器
        futures = [executor.submit(run_spider, script) for script in spiders]

        # 等待所有任务完成并获取结果（这里是为了确保所有任务都完成）
        for future in futures:
            future.result()  # 获取每个Future对象的结果，阻塞直到完成