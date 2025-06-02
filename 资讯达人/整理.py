import os
import re
import chardet
from bs4 import BeautifulSoup
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def detect_encoding(file_path):
    rawdata = open(file_path, 'rb').read()
    result = chardet.detect(rawdata)
    return result['encoding']

# 定义新闻数据的结构
news_data = []

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
print(f"处理完成，结果已保存至 {output_file_path}。")