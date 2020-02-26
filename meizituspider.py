import requests
from bs4 import BeautifulSoup
import lxml
import os
import time
import tkinter as tk
from tkinter.filedialog import askdirectory


headers = {'Referer':'https://www.mzitu.com','User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3679.0 Safari/537.36'}

# 构造每一页的链接
def create_page_url_list(start_page, end_page, path):

    url_list = []
    for i in range(int(start_page), int(end_page)+1):
        url_list.append("https://www.mzitu.com/page/{}/".format(i))
    # 调用 get_chapter_url爬取
    for url in url_list:
        get_chapter_url(str(url), path)
    

# 获取图片总页数
def get_max_page():

    url = "https://www.mzitu.com/"
    response = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(response.content, "lxml")
    # 获取图片总页数
    max_page = soup.select("body > div.main > div.main-content > nav > div > a:nth-child(6)")[0].contents[0]
    return max_page


# 获取每一页个专题的链接
def get_chapter_url(page_url, path):

    chapter_url = page_url
    response = requests.get(url=chapter_url, headers=headers)
    soup = BeautifulSoup(response.content, "lxml")
    # 获取专题链接暂存在字典中
    res_dict = {}
    res = soup.find_all("div", class_="main-content")[0].find_all("div", class_="postlist")[0].find_all("a", target="_blank")
    for i in range(1, len(res), 2):
        url = res[i].get("href")
        title = res[i].contents[0]
        res_dict[url] = title

    download_image(res_dict, path)


# 获取每个专题的所有图片链接并下载
def download_image(url_dict, path):

    for url, title in url_dict.items():
        # 根据标题创建文件夹用于保存文件
        title = str(title)
        
        path = "{0}/{1}".format(path, title)
        print(path)

        if not os.path.exists(path):
            os.makedirs(path)

    
        # 分析每个图片的下载地址并下载图片
        response = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(response.content, "lxml")
        # 获取每个专题的图片数量
        max_content_page = int(soup.select("body > div.main > div.content > div.pagenavi > a:nth-child(7) > span")[0].contents[0])
        # 构造每一个图片页的URL
        for page in range(1, max_content_page+1):
            img_url = url + '/' + str(page)
            # 获取每张图片的下载地址并下载图片
            result = requests.get(url=img_url, headers=headers)
            soup = BeautifulSoup(result.content, "lxml")
            download_url = soup.find_all('img',alt="{}".format(title))[0].get("src")
            image = requests.get(url=download_url, headers=headers)
            # 保存图片
            with open("{0}/{1}.jpg".format(path, page), 'wb') as fp:
                fp.write(image.content)
                time.sleep(1)
    
path_chosen = os.getcwd()

# 定制图形界面
def main():
    top = tk.Tk()
    top.title("妹子图专用爬虫")
    top.geometry("400x300")
    # 提示用户输入要爬取的页码范围

    # 调用get_max_page获取当前最大页码
    cur_max_page = get_max_page()
    label1 = tk.Label(top,text = "请输入要爬取的页码：", font = ("宋体", 18))
    label1.grid(row=0,sticky = tk.W)
    label2 = tk.Label(top, text="（提示：当前共有{}页）".format(cur_max_page))
    label2.grid(row=1, sticky = tk.W)

    label3 = tk.Label(top,text = "请输入起始页码：", font = ("宋体", 14))
    label3.grid(row=2,sticky = tk.W)
    v1 = tk.IntVar()
    page_area1 = tk.Entry(top,textvariable=v1)
    v1.set(1)
    page_area1.grid(row = 3, sticky = tk.W)


    label4 = tk.Label(top,text = "请输入结束页码：", font = ("宋体", 14))
    label4.grid(row=4,sticky = tk.W)
    v2 = tk.IntVar()
    page_area2 = tk.Entry(top, textvariable=v2)
    v2.set(1)
    page_area2.grid(row = 6, sticky = tk.W)



    # 选择路径函数
    def selectPath():
        global path_chosen
        path_ = askdirectory(title = "请选择保存路径")
        label5 = tk.Label(top,text = "保存路径：{}".format(path_), font = ("宋体", 12))
        label5.grid(row=8,sticky = tk.W)
        path_chosen = path_


    print(path_chosen)
    
    # 选择路径按钮
    button0 = tk.Button(top, text="选择保存路径", font=("宋体", 18), command=selectPath)
    button0.grid(row = 7,sticky = tk.W)


    # 开始按钮
    button1 = tk.Button(top, text="Start", font=("宋体", 18), command=lambda : create_page_url_list(page_area1.get(), page_area2.get(), path_chosen))
    button1.grid(row = 9,sticky = tk.W)

    top.mainloop()


if __name__ == "__main__":
    main()