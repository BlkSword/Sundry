import requests
import re
import lxml
from bs4 import BeautifulSoup

# 请确保这里有一个有效的RSS或XML源的URL
url = 'https://www.seebug.org/rss/new/'

response = requests.get(url)

# 检查请求是否成功
if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'lxml-xml')

    items = soup.find_all('item')

    # 创建一个文件以写入数据
    with open("Seebug.txt", "w", encoding="utf-8") as file:
        for item in items:
            title = item.find('title').get_text(strip=True)
            link = item.find('link').get_text(strip=True) if item.find('link') else '链接未提供'
            description = item.find('description').get_text(strip=True) if item.find('description') else '未知'
            level = item.find('level').get_text(strip=True) if item.find('level') else '未知'
            source = item.find('source').get_text(strip=True) if item.find('source') else '未知'
            category = item.find('category').get_text(strip=True) if item.find('category') else '未知'
            updated_date = item.find('updated_date').get_text(strip=True) if item.find('updated_date') else '发布日期未提供'


            description = re.sub(r'(作者|译者).*?\n', '', description)
            title = title.replace(":", "")
            link = link.replace("", "")
            category = category.replace(":", "")
            description = description.replace(":", "")
            updated_date = updated_date.replace(":", "")

            # 写入文件
            file.write(f"标题：{title}\n")
            file.write(f"链接：{link}\n")
            file.write(f"类型：{category}\n")
            file.write(f"内容：{description}\n")
            file.write(f"发布日期：{updated_date}\n\n")

    print("数据已成功写入到 Seebug.txt 文件。")
else:
    print("获取网页失败，状态码:", response.status_code)