import requests

def get_and_save_html(url, filename):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    try:
        # 发送HTTP请求
        response = requests.get(url, headers=headers)
        # 检查响应的状态码是否为200（成功）
        response.raise_for_status()
        
        # 将网页内容写入文件
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(response.text)
        print(f"内容已保存至 {filename}")
    except requests.RequestException as e:
        print(f"请求错误: {e}")

def main():
    url = "https://www.exploit-db.com/exploits/52075"
    filename = "exploit_52075.txt"
    get_and_save_html(url, filename)

if __name__ == "__main__":
    main()