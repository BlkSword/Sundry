import re

# 假设entry是从某个XML解析得到的元素对象
# 这里我们模拟一个entry对象，实际使用时请替换为真实的entry对象
from xml.etree import ElementTree as ET

xml_data = '''
<entry>
    <title>示例标题</title>
    <link>http://example.com/link</link>
    <description>这是描述信息。</description>
    <source>来源信息</source>
    <category>分类信息</category>
    <author>作者信息</author>
    <pubDate>发布日期信息</pubDate>
    <guid>https://www.anquanke.com/post/id/303208</guid>
</entry>
'''

root = ET.fromstring(xml_data)
entry = root

title = entry.find('title').get_text(strip=True) if entry.find('title') else '未知'
link = entry.find('guid').get_text(strip=True) if entry.find('guid') else '链接未提供'
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

print(f"Title: {title}")
print(f"Link: {link}")
print(f"Description: {description}")
print(f"Source: {source}")
print(f"Category: {category}")
print(f"Author: {author}")
print(f"PubDate: {pubDate}")
print(f"Summary Text: {summary_text}")
print(f"Categories: {categories}")
print(f"Updated: {updated}")



