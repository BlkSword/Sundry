import requests
from bs4 import BeautifulSoup
import lxml
import re
# RSS源的URL
url = 'https://www.huawei.com/cn/rss-feeds/psirt/rss'

response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'lxml-xml')
    
    items = soup.find_all('item')

    # 创建一个文件以写入数据
    with open("华为.txt", "w", encoding="utf-8") as file:
        for item in items:
            title = item.find('title').get_text(strip=True)
            # 修改标题，移除"安全通告"
            title = title.replace('安全通告 - ''涉及 华为', '')
            link = item.find('link').get_text(strip=True) if item.find('link') else '链接未提供'
            category = item.find('category').get_text(strip=True) if item.find('category') else ' '
            description = item.find('description').get_text(strip=True) if item.find('description') else '未知'
            pubDate = item.find('pubDate').get_text(strip=True)

            description = re.sub(r'(作者|译者).*?\n', '', description)
            title = title.replace(":", "")
            link = link.replace(":", "")
            category = category.replace(":", "")
            description = description.replace(":", "")
            pubDate = pubDate.replace(":", "")

            # 删除已有的协议部分并自动补齐缺少的冒号
            if not re.match(r'https?://', link):
                link = re.sub(r'//', '', link)  # 删除已有的 http(s)://
                link = f"http://{link}"  # 补全为 http://

            # 写入文件
            file.write(f"标题：{title}\n")
            file.write(f"链接：{link}\n")
            file.write(f"类型：{category}\n")
            file.write(f"内容：{description}\n")
            file.write(f"发布日期：{pubDate}\n\n")
    print("数据已成功写入到 华为.txt 文件。")
else:
    print("获取网页失败，状态码:", response.status_code)