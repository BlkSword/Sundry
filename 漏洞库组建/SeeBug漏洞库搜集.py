import requests  # 导入用于发送HTTP请求的模块
import time  # 导入用于控制请求间隔的模块
from bs4 import  BeautifulSoup  # 导入用于解析HTML文档的模块

def fetch_and_parse_html(url):
    try:
        # 发送HTTP请求
        response = requests.get(url)
        # 检查响应的状态码是否为200（成功）
        response.raise_for_status()  # 如果状态码不是200，则抛出异常
    except requests.RequestException as e:
        print(f"请求错误: {e}")  # 打印请求错误信息
        return None
    
    # 使用BeautifulSoup解析HTML
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 初始化变量，用于存储漏洞信息
    submit_date = '未知'
    severity = '未知'
    category = '未知'
    cvenumber = '未知'
    component = '未知'
    source_link = '未知'
    
    # 提取所需信息，并添加保护措施以防元素不存在
    dt_submit_date = soup.find('dt', string='提交时间：')  # 查找标签
    if dt_submit_date:
        submit_date = dt_submit_date.find_next_sibling('dd').get_text(strip=True)   #strip=True 参数表示当获取 <dd> 标签内的文本时，会自动去除文本两端的空白字符
    
    severity_element = soup.find('div', attrs={'data-original-title': True})  # 查找具有特定属性的标签
    if severity_element:
        # 获取该标签的'data-original-title'属性值
        severity = severity_element['data-original-title']  # 获取属性值
    
    dt_category = soup.find('dt', string='漏洞类别：')  # 查找标签
    if dt_category:
        category_element = dt_category.find_next_sibling('dd').find('a')  # 查找链接标签
        if category_element:
            category = category_element.get_text()  # 获取链接文本
    
    dt_cvenumber = soup.find('dt', string='CVE-ID：')  # 查找标签
    if dt_cvenumber:
        cvenumber_element = dt_cvenumber.find_next_sibling('dd').find('a')  # 查找链接标签
        if cvenumber_element:
            cvenumber = cvenumber_element.get_text()  # 获取链接文本
    
    source_h3 = soup.find('h3', string='来源')  # 查找标题标签
    if source_h3:
        source_div = source_h3.find_next_sibling('div')  # 查找下一个div标签
        if source_div:
            # 查找具有特定id（j-md-source）的<div>标签
            source_link_container = source_div.find('div', id='j-md-source')  # 查找具有特定id的div标签
            if source_link_container:
                source_link_element = source_link_container.find('a')  # 查找链接标签
                if source_link_element:
                    source_link = source_link_element['href']  # 获取链接地址
    
    dt_component = soup.find('dt', string='影响组件：')  # 查找标签
    if dt_component:
        component_element = dt_component.find_next_sibling('dd').find('a')  # 查找链接标签
        if component_element:
            component = component_element.get_text()  # 获取链接文本
    
    # 创建字典存储信息
    info = {
        "提交时间": submit_date,
        "漏洞等级": severity,
        "漏洞类别": category,
        "CVE-ID": cvenumber,
        "影响组件": component,
        "来源": source_link,
        "网址": "https://www.seebug.org/vuldb/ssvid-{number}"
    }
    
    return info  # 返回信息字典

def save_info_to_file(info, filename):
    try:
        with open(filename, 'w', encoding='utf-8') as file:  # 以写模式打开文件
            for key, value in info.items():  # 遍历字典
                file.write(f"{key}: {value}\n")  # 写入信息
        print(f"已保存信息到 {filename}")  # 打印保存信息
    except IOError as e:
        print(f"无法写入文件 {filename}: {e}")  # 打印错误信息

def main():
    base_url = "https://www.seebug.org/vuldb/ssvid-{number}"  # 基础URL格式化字符串
    for number in range(99878, 99644, -1):  # 循环遍历编号
        url = base_url.format(number=number)  # 构建完整URL
        print(f"正在处理 {url}")  # 打印处理中的URL
        info = fetch_and_parse_html(url)  # 获取并解析HTML
        if info:  # 如果获取的信息有效
            filename = f"{number}.txt"  # 设置文件名
            save_info_to_file(info, filename)  # 保存信息到文件
        time.sleep(0.5)  # 暂停0.5秒避免请求过于频繁

if __name__ == "__main__":
    main()  # 执行主函数