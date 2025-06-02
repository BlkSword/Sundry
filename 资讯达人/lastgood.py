import subprocess     # 用于调用外部命令或运行其他Python脚本
import os             # 提供与操作系统交互的功能，如检查文件是否存在
import time           # 提供时间相关功能，如暂停执行
from concurrent.futures import ThreadPoolExecutor  # 提供线程池执行器，用于并发执行任务
import requests
import re
from bs4 import BeautifulSoup
import chardet
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def fetch_and_write_rss(url, filename):
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'lxml-xml')
        
        if filename == "腾讯玄武.txt":
            entries = soup.find_all('entry')
        else:
            channel = soup.find('channel')
            items = channel.find_all('item') if channel else []

        with open(filename, "w", encoding="utf-8") as file:
            for entry in entries if filename == "腾讯玄武.txt" else items:
                title = entry.find('title').get_text(strip=True)
                
                if filename == "腾讯玄武.txt":
                    link = entry.find('link')['href'] if entry.find('link') else '链接未提供'
                    
                    # 获取summary标签内的内容
                    summary = entry.find('summary')
                    if summary:
                        # 使用BeautifulSoup解析summary，移除所有HTML标签
                        summary_text = BeautifulSoup(summary.get_text(), 'html.parser').get_text(strip=True)
                    
                    categories = [cat['term'] for cat in entry.find_all('category')]
                    updated = entry.find('updated').get_text(strip=True)
                    source = ''  # 腾讯玄武没有source字段
                    author = ''  # 初始化author为空字符串
                elif filename == "Seebug Paper.txt":
                    guid = entry.find('guid').get_text(strip=True) if entry.find('guid') else '链接未提供'
                    description = entry.find('description').get_text(strip=True) if entry.find('description') else '未知'
                    source = entry.find('source').get_text(strip=True) if entry.find('source') else '未知'
                    category = entry.find('category').get_text(strip=True) if entry.find('category') else '未知'
                    pubDate = entry.find('pubDate').get_text(strip=True)

                    link = guid
                    summary_text = description
                    categories = [category] if category else []
                    updated = pubDate
                    author = ''  # 初始化author为空字符串
                elif filename == "Seebug.txt":
                    link = entry.find('link').get_text(strip=True) if entry.find('link') else '链接未提供'
                    description = entry.find('description').get_text(strip=True) if entry.find('description') else '未知'
                    level = entry.find('level').get_text(strip=True) if entry.find('level') else '未知'
                    source = entry.find('source').get_text(strip=True) if entry.find('source') else '未知'
                    category = entry.find('category').get_text(strip=True) if entry.find('category') else '未知'
                    updated_date = entry.find('updated_date').get_text(strip=True) if entry.find('updated_date') else '发布日期未提供'

                    summary_text = description
                    categories = [category] if category else []
                    updated = updated_date
                    author = ''  # 初始化author为空字符串
                else:
                    link = entry.find('link').get_text(strip=True) if entry.find('link') else '链接未提供'
                    description = entry.find('description').get_text(strip=True) if entry.find('description') else '未知'
                    source = entry.find('source').get_text(strip=True) if entry.find('source') else '未知'
                    category = entry.find('category').get_text(strip=True) if entry.find('category') else ''
                    author = entry.find('author').get_text(strip=True) if entry.find('author') else '未知'
                    pubDate = entry.find('pubDate').get_text(strip=True)

                    summary_text = description
                    categories = [category] if category else []
                    updated = pubDate
                    
                # 移除不需要的部分
                summary_text = re.sub(r'(作者|译者).*?：\n', '', summary_text)
                title = title.replace(":", "").replace('安全通告 - 涉及 华为', '')
                link = link.replace(":", "")
                source = source.replace(":", "")
                categories = [cat.replace(":", "") for cat in categories]
                author = author.replace(":", "")
                summary_text = summary_text.replace(":", "")
                updated = updated.replace(":", "")

                # 写入文件
                file.write(f"标题：{title}\n")
                file.write(f"链接：{link}\n")
                file.write(f"类型：{', '.join(categories or [author, source])}\n")
                file.write(f"内容：{summary_text}\n")
                file.write(f"发布日期：{updated}\n\n")

        print(f"数据已成功写入到 {filename} 文件。")
    else:
        print(f"获取网页失败，状态码: {response.status_code}")

# 定义一个函数来运行单个抓取任务，具有重试机制
def run_fetcher(task):
    url, filename = task
    max_retries = 3  # 设置最大重试次数
    retry_delay = 5  # 设置两次尝试之间的延迟时间（秒）

    # 尝试运行抓取任务，直到成功或达到最大重试次数
    for attempt in range(max_retries):
        try:
            print(f"Attempt {attempt + 1}: Fetching and writing RSS from {url} to {filename}...")
            fetch_and_write_rss(url, filename)
            print(f"Fetching and writing RSS from {url} to {filename} completed successfully.")
            return
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"Failed to fetch and write RSS from {url} to {filename}. Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)  # 等待一段时间再重试
            else:
                print(f"Failed to fetch and write RSS from {url} to {filename} after {max_retries} attempts.")

def detect_encoding(file_path):
    rawdata = open(file_path, 'rb').read()
    result = chardet.detect(rawdata)
    return result['encoding']

# 主函数，定义爬虫任务的列表并使用线程池执行器并发运行它们
if __name__ == "__main__":
    # 删除当前目录下所有的txt文件
    for file in os.listdir('.'):
        if file.endswith('.txt'):
            os.remove(os.path.join('.', file))
            print(f"已删除文件: {file}")

    tasks = [
        ("https://api.anquanke.com/data/v1/rss", "安全客.txt"),
        ("https://tech.meituan.com/feed/", "美团技术.txt"),
        ("https://www.huawei.com/cn/rss-feeds/psirt/rss", "华为.txt"),
        ("https://blog.nsfocus.net/feed/", "绿盟.txt"),
        ("https://paper.seebug.org/rss/", "嘶吼.txt"),
        ("https://xlab.tencent.com/cn/atom.xml", "腾讯玄武.txt"),
        ("https://www.freebuf.com/feed", "FreeBuf.txt"),
        ("https://www.seebug.org/rss/new/", "Seebug.txt"),
        ("https://paper.seebug.org/rss/", "Seebug Paper.txt")
    ]
    
    # 创建一个线程池执行器，用于并发执行任务
    with ThreadPoolExecutor() as executor:
        # 提交每个抓取任务到线程池执行器
        futures = [executor.submit(run_fetcher, task) for task in tasks]

        # 等待所有任务完成并获取结果（这里是为了确保所有任务都完成）
        for future in futures:
            future.result()  # 获取每个Future对象的结果，阻塞直到完成
    
    # 定义新闻数据的结构
    news_data = []

    print("正在等待数据回显.......");

    for filename in os.listdir('.'):
        if filename.endswith('.txt'):
            file_path = os.path.join('.', filename)
            print(f"正在读取文件: {filename}")
            
            try:
                # 使用检测到的编码读取文件，以防编码错误
                encoding = detect_encoding(file_path)
                with open(file_path, 'r', encoding=encoding, errors='replace') as file:
                    content = file.read()

                    # 使用正则表达式匹配新闻条目
                    matches = re.findall(r'标题：(.*?)\n链接：(.*?)\n类型：(.*?)\n内容：(.*?)\n发布日期：(.*?)\n', content, re.DOTALL)

                    # 清理HTML标签
                    for i, match in enumerate(matches):
                        title, link, source, content, date = match
                        cleaned_content = BeautifulSoup(content, 'html.parser').get_text()
                        matches[i] = (title, link, source, cleaned_content, date)

                    # 将每篇新闻添加到列表中
                    for match in matches:
                        title, link, source, content, date = match
                        news_data.append({
                            'title': title.strip(),
                            'link': link.strip(),
                            'source': source.strip(),
                            'content': content.strip(),
                            'date': date.strip()
                        })
                    print(f"成功读取并解析 {filename}")

            except UnicodeDecodeError:
                print(f"无法解码文件 {filename}，可能的编码问题。")
            except Exception as e:
                print(f"读取文件 {filename} 出错: {e}")

    print(f"收纳了 {len(news_data)} 篇新闻。")

    # 转换为Pandas DataFrame
    df = pd.DataFrame(news_data)
    print("转换为DataFrame完成，开始计算TF-IDF向量。")

    # 对内容进行TF-IDF向量化
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(df['content'])
    print("TF-IDF向量计算完成，开始计算相似度矩阵。")

    # 计算相似度矩阵
    similarity_matrix = cosine_similarity(tfidf_matrix)
    print("相似度矩阵计算完成，开始查找重复项。")

    # 找到重复项
    threshold = 0.5  # 相似度阈值
    duplicates = set()
    for i in range(len(df)):
        for j in range(i+1, len(df)):
            if similarity_matrix[i][j] > threshold:
                duplicates.add(j)

    # 计算并打印重复项数量
    num_duplicates = len(duplicates)
    print(f"找到了 {num_duplicates} 个重复项。")

    # 移除重复项
    df_cleaned = df.drop(list(duplicates)).reset_index(drop=True)
    print("重复项移除完成，开始保存结果。")

    # 将处理后的新闻保存到一个文本文件
    output_text = ""
    for index, row in df_cleaned.iterrows():
        output_text += f"标题：{row['title']}\n链接：{row['link']}\n类型：{row['source']}\n内容：{row['content']}\n发布日期：{row['date']}\n\n"

    # 写入文件，使用utf-8编码
    output_file_path = '每日快讯.txt'
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        output_file.write(output_text)



