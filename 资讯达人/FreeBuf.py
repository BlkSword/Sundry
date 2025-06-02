import requests
from bs4 import BeautifulSoup
import re
import lxml
# 假设这是你要抓取的RSS Feed的URL
url = 'https://www.freebuf.com/feed'

response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'lxml-xml')

    channel = soup.find('channel')
    title = channel.find('title').text
    link = channel.find('link').text
    description = channel.find('description').text
    pub_date = channel.find('pubDate').text

    items = channel.find_all('item')

    with open('FreeBuf.txt', 'w', encoding='utf-8') as file:

        # 写入每篇文章的信息
        for item in items:
            item_title = item.find('title').text if item.find('title') else 'N/A'
            item_link = item.find('link').text if item.find('link') else 'N/A'
            item_description = item.find('description').text if item.find('description') else 'N/A'
            item_category = item.find('category').text if item.find('category') else 'N/A'
            item_pub_date = item.find('pubDate').text if item.find('pubDate') else 'N/A'

            description = re.sub(r'(作者|译者).*?\n', '', description)
            item_title = item_title.replace(":", "")
            item_link = item_link.replace("", "")
            item_category = item_category.replace(":", "")
            item_description = item_description.replace(":", "")
            item_pub_date = item_pub_date.replace(":", "")

            file.write(f"标题：{item_title}\n")
            file.write(f"链接：{item_link}\n")
            file.write(f"类型：{item_category}\n")
            file.write(f"内容：{item_description}\n")
            file.write(f"发布日期：{item_pub_date}\n\n")

        print("已成功打印")
else:
    print("请求失败，状态码:", response.status_code)