import tkinter as tk
from tkinter import ttk
import tkinter.scrolledtext as scrolledtext
import tkinter.font as font
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from dateutil.parser import parse
import uuid

# 获取今天的日期
today = datetime.now()

# 计算三个月前的日期
three_months_ago = today - relativedelta(months=3)

# 格式化日期为 YYYY-MM-DD 格式
formatted_today = today.strftime('%Y-%m-%d')
formatted_three_months_ago = three_months_ago.strftime('%Y-%m-%d')

def read_news_entries(file_path):
    entries = []
    current_entry = {}

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if line == '':
                if current_entry and '发布日期' in current_entry:
                    # 生成一个 UUID 并添加到字典中
                    current_entry['uuid'] = str(uuid.uuid4())
                    # 过滤掉不在三个月范围内的条目
                    if formatted_three_months_ago <= current_entry['发布日期'] <= formatted_today:
                        entries.append(current_entry)
                    current_entry = {}
            else:
                parts = line.split("：", 1)
                if len(parts) == 2:
                    key, value = parts
                    if key == "发布日期":
                        try:
                            value = parse(value).strftime('%Y-%m-%d')
                        except ValueError:
                            print(f"警告：无法解析日期 '{value}'，跳过此条目.")
                            current_entry = {}
                    current_entry[key] = value
    
    if current_entry and '发布日期' in current_entry and formatted_three_months_ago <= current_entry['发布日期'] <= formatted_today:
        current_entry['uuid'] = str(uuid.uuid4())
        entries.append(current_entry)
    
    return entries

def display_news_entries(entries):
    root = tk.Tk()
    root.title("新闻条目")

    # 创建 Treeview 和滚动条
    tree = ttk.Treeview(root, columns=("标题", "类型", "内容", "发布日期"), show="headings")
    tree.heading("标题", text="标题", command=lambda: sort_tree(tree, "标题", False))
    tree.heading("类型", text="类型", command=lambda: sort_tree(tree, "类型", False))
    tree.heading("内容", text="内容", command=lambda: sort_tree(tree, "内容", False))
    tree.heading("发布日期", text="发布日期", command=lambda: sort_tree(tree, "发布日期", False))

    scrollbar = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)

    # 将滚动条和 Treeview 放置在窗口中
    tree.pack(side="left", fill=tk.BOTH, expand=True)
    scrollbar.pack(side="right", fill=tk.Y)

    # 添加条目到 Treeview
    for entry in entries:
        if all(key in entry for key in ["标题", "类型", "内容", "发布日期", "uuid"]):
            tree.insert("", "end", values=(entry["标题"], entry["类型"], entry["内容"], entry["发布日期"]), tags=(entry['uuid'],))

    # 当双击条目时显示详细信息
    def show_details(event):
        selected_item = tree.selection()[0]
        uuid_tag = tree.item(selected_item)['tags'][0]
        entry = next((e for e in entries if e['uuid'] == uuid_tag), None)
        if entry:
            details_text.delete(1.0, tk.END)
            for i, col in enumerate(tree['columns']):
                details_text.insert(tk.END, f"{col}: {entry[col]}\n")
            # 显示链接信息
            details_text.insert(tk.END, f"链接: {entry['链接']}\n")

    tree.bind("<Double-1>", show_details)

    # 创建一个 ScrolledText 控件来显示详细信息，并设置字体和字号
    details_font = font.Font(family="楷体", size=15)  # 创建Font对象
    details_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=details_font)  # 将Font对象应用到ScrolledText
    details_text.pack(side="bottom", fill=tk.BOTH, expand=True)

    root.mainloop()

def sort_tree(tree, column_name, reverse):
    l = [(tree.set(k, column_name), k) for k in tree.get_children('')]
    l.sort(reverse=reverse)

    # rearrange items in sorted positions
    for index, (val, k) in enumerate(l):
        tree.move(k, '', index)

    # reverse sort next time
    tree.heading(column_name, command=lambda: sort_tree(tree, column_name, not reverse))


if __name__ == "__main__":
    news_entries = read_news_entries("每日快讯.txt")
    display_news_entries(news_entries)