import requests
import re
import lxml
from bs4 import BeautifulSoup

# 请确保这里有一个有效的RSS或XML源的URL
url = 'https://paper.seebug.org/rss/'

response = requests.get(url)

# 检查请求是否成功
if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'lxml-xml')

    items = soup.find_all('item')

    # 创建一个文件以写入数据
    with open("嘶吼.txt", "w", encoding="utf-8") as file:
        for item in items:
            title = item.find('title').get_text(strip=True)
            link = item.find('link').get_text(strip=True) if item.find('link') else '链接未提供'
            description = item.find('description').get_text(strip=True) if item.find('description') else '未知'
            source = item.find('source').get_text(strip=True) if item.find('source') else '未知'
            author = item.find('author').get_text(strip=True) if item.find('author') else '未知'
            pubDate = item.find('pubDate').get_text(strip=True)

            description = re.sub(r'(作者|译者).*?\n', '', description)
            title = title.replace(":", "")
            link = link.replace(":", "")
            author = author.replace(":", "")
            description = description.replace(":", "")
            pubDate = pubDate.replace(":", "")

            if not re.match(r'https?://', link):
                link = re.sub(r'^https?//', '', link)  # 删除已有的 http(s)://
                link = f"http://{link}"  # 补全为 http://

            # 写入文件
            file.write(f"标题：{title}\n")
            file.write(f"链接：{link}\n")
            file.write(f"类型：{author}\n")
            file.write(f"内容：{description}\n")
            file.write(f"发布日期：{pubDate}\n\n")

    print("数据已成功写入到 嘶吼.txt 文件。")
else:
    print("获取网页失败，状态码:", response.status_code)