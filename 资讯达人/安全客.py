import requests
import re
import lxml
from bs4 import BeautifulSoup

# 请确保这里有一个有效的RSS或XML源的URL   
url = 'https://api.anquanke.com/data/v1/rss'

response = requests.get(url)

# 检查请求是否成功
if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'lxml-xml')

    items = soup.find_all('item')

    # 创建一个文件以写入数据
    with open("安全客.txt", "w", encoding="utf-8") as file:
        for item in items:
            title = item.find('title').get_text(strip=True)
            guid = item.find('guid').get_text(strip=True) if item.find('guid') else '链接未提供'
            author = item.find('author').get_text(strip=True) if item.find('author') else '未知'
            source = item.find('source').get_text(strip=True) if item.find('source') else '未知'
            pubDate = item.find('pubDate').get_text(strip=True)

            source = re.sub(r'(作者|译者).*?\n', '', source)
            title = title.replace(":", "")
            guid = guid.replace("", "")
            source = source.replace(":", "")
            #description = description.replace(":", "")
            pubDate = pubDate.replace(":", "")

            # 写入文件
            file.write(f"标题：{title}\n")
            file.write(f"链接：{guid}\n")
            file.write(f"类型：{author}\n")
            file.write(f"内容：{source}\n")
            file.write(f"发布日期：{pubDate}\n\n")

    print("数据已成功写入到 安全客.txt 文件。")
else:
    print("获取网页失败，状态码:", response.status_code)