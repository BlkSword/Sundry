import requests
from bs4 import BeautifulSoup
import html
import re
url = 'https://xlab.tencent.com/cn/atom.xml'

response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'lxml-xml')
    
    entries = soup.find_all('entry')
    
    with open("腾讯玄武.txt", "w", encoding="utf-8") as file:
        for entry in entries:
            title = entry.find('title').get_text(strip=True)
            link = entry.find('link')['href'] if entry.find('link') else '链接未提供'
            
            # 获取summary标签内的内容
            summary = entry.find('summary')
            if summary:
                # 使用BeautifulSoup解析summary，移除所有HTML标签
                summary_text = BeautifulSoup(summary.get_text(), 'html.parser').get_text(strip=True)
            
            categories = [cat['term'] for cat in entry.find_all('category')]
            updated = entry.find('updated').get_text(strip=True)

            summary_text = re.sub(r'(作者|译者).*?：\n', '', summary_text)
            title = title.replace(":", "")
            link = link.replace(":", "")
            summary_text = summary_text.replace(":", "")
            updated = updated.replace(":", "")

            if not re.match(r'https?://', link):
                link = re.sub(r'^https?//', '', link)  # 删除已有的 http(s)://
                link = f"http://{link}"  # 补全为 http://

            # 写入文件
            file.write(f"标题：{title}\n")
            file.write(f"链接：{link}\n")
            file.write(f"类型：{', '.join(categories)}\n")
            file.write(f"内容：{summary_text}\n")  # 注意这里使用summary_text而不是summary
            file.write(f"发布日期：{updated}\n\n")

    print("数据已成功写入到 腾讯玄武.txt 文件。")
else:
    print("获取网页失败，状态码:", response.status_code)