# @time     : 2020/7/13 22:35
# @author  : HerbLee
# @file    : meizhuo.py


import requests
import re
import os
from pypinyin import pinyin, lazy_pinyin

"""
使用说明
    安装pypinyin包即可
    pip install pypinyin
"""


class MeiZhuo:
    """
    用于下载美桌网图片，目前支持中文名字
    """

    def __init__(self, download_path="./"):
        self.download_path = download_path
        self.url = "http://www.win4000.com/mt/{}.html"

    def html(self, url):
        try:
            r = requests.get(url, timeout=30)
            r.raise_for_status()
            r.encoding = r.apparent_encoding
            return r.text
        except:
            return ""

    def get_page_url(self, html, name):
        # get detail page url
        re_pageUrl = r'href="(.+)">\s*<img src="(.+)" alt="' + name
        return re.findall(re_pageUrl, html)

    def download(self, html, path, name):
        # find all item
        page_url_list = self.get_page_url(html, name)
        # all item name
        titles_list = re.findall(r'alt="' + name + r'(.+)" ', html)
        for (url, pic), title in zip(page_url_list, titles_list):
            tf = os.path.join(path, title)
            if not os.path.exists(tf):
                os.makedirs(tf)
            item_html = self.html(url)
            pic_nums = int(re.findall(r'<em>(.+)</em>）', item_html)[0])
            pic_url = re.findall(r'href="(.+?)" class="">下载图片', item_html)[0]

            for idx in range(pic_nums):
                pic_path = os.path.join(tf, "{}.jpg".format(idx))
                r = requests.get(pic_url)
                with open(pic_path, 'wb') as f:
                    f.write(r.content)

                print('{} - 第{}张下载已完成\n'.format(title, idx + 1))
                next_page_url = re.findall(r'href="(.+?)">下一张', item_html)[0]
                item_html = self.html(next_page_url)
                pic_url = re.findall(r'href="(.+?)" class="">下载图片', item_html)[0]

    def download_pic(self, name):
        p_name = "".join(lazy_pinyin(name))
        target_url = self.url.format(p_name)
        html = self.html(target_url)
        if html == "" or re.findall(r'暂无(.+)!', html):
            print("美桌网没有找到{}的图片".format(name))
            return
        # make sure pic download folder
        download_path = os.path.join(self.download_path, name)
        # if target folder not exists make folder
        if not os.path.exists(download_path):
            os.makedirs(download_path)

        self.download(html, download_path, name)
        try:
            next_page = re.findall(r'next" href="(.+)"', html)[0]
            while next_page:
                html = self.html(next_page)
                self.download(html, download_path, name)
                next_page = re.findall(r'next" href="(.+)"', html)[0]
        except:
            print("download success")


if __name__ == '__main__':
    mz = MeiZhuo()
    mz.download_pic("沈月")
