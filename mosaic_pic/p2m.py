"""
Created on 2020-07-12 01:48
@author : herb
"""

import cv2
import math
import numpy as np
import os
import random


"""

02:40
03:10
pip install opencv-python
pip install numpy
"""

class picMosaic:

    def __init__(self, pic_path, dir_path, nums=40, min_size=64):
        self.pic_path = pic_path
        self.dir_path = dir_path
        self.nums = nums
        self.temp_img_path = "./data/temp.jpg"
        self.match_res = "./data/match.txt"
        self.h_num = 0
        self.w_num = 0
        self.o_size = 0
        self.min_size = min_size
        self.out_img_path = "./out.jpg"
        self._flush_data()

    def _flush_data(self):
        self.print("初始化data文件夹")
        if os.path.exists("./data"):
            for item in os.listdir("./data"):
                os.remove(os.path.join("./data", item))
        else:
            os.makedirs("./data")

    @staticmethod
    def get_color_dict():
        return {
            "0": [np.array([0, 0, 0]), np.array([180, 255, 46])],  # black
            "1": [np.array([0, 0, 46]), np.array([180, 43, 220])],  # gray
            "2": [np.array([0, 0, 221]), np.array([180, 30, 255])],  # white
            "3": [np.array([156, 43, 46]), np.array([180, 255, 255])],  # red 1
            "4": [np.array([0, 43, 46]), np.array([10, 255, 255])],  # red 2
            "5": [np.array([11, 43, 46]), np.array([25, 255, 255])],  # orange
            "6": [np.array([26, 43, 46]), np.array([34, 255, 255])],  # yellow
            "7": [np.array([35, 43, 46]), np.array([77, 255, 255])],  # green
            "8": [np.array([78, 43, 46]), np.array([99, 255, 255])],  # cyan
            "9": [np.array([100, 43, 46]), np.array([124, 255, 255])],  # blue
            "10": [np.array([125, 43, 46]), np.array([155, 255, 255])],  # purple
        }

    def col_distance_lab(self, rgb_1, rgb_2):
        """
        计算颜色距离
        :param rgb_1: (r,g,b)
        :param rgb_2: (r,g,b)
        :return: 距离值
        """
        R_1, G_1, B_1 = rgb_1
        R_2, G_2, B_2 = rgb_2
        rmean = (R_1 + R_2) / 2
        R = R_1 - R_2
        G = G_1 - G_2
        B = B_1 - B_2
        return math.sqrt((2 + rmean / 256) * (R ** 2) + 4 * (G ** 2) + (2 + (255 - rmean) / 256) * (B ** 2))

    def get_color(self, img):
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        maxsum = -100
        color = None
        color_dict = self.get_color_dict()
        for d in color_dict:
            mask = cv2.inRange(hsv, color_dict[d][0], color_dict[d][1])
            binary = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY)[1]
            binary = cv2.dilate(binary, None, iterations=2)
            cnts, hiera = cv2.findContours(binary.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            sum = 0
            for c in cnts:
                sum += cv2.contourArea(c)
            if sum > maxsum:
                maxsum = sum
                color = d

        return color, maxsum

    def get_pic_color(self):
        self.print("开始分割原图")
        img = cv2.imread(self.pic_path)
        h, w, _ = img.shape
        nums = self.nums
        c_w = int(w / nums)
        c_h = int(h / c_w)

        while c_w * nums < w:
            nums += 1
        n_w = c_w * nums
        while c_h * c_w < h:
            c_h += 1
        n_h = c_h * c_w
        n_size = c_w
        img = img[:n_h, :n_w]
        res_list = []
        res_list.append([str(n_h), str(n_w), str(n_size), str(nums), str(c_h)])
        self.h_num = c_h
        self.w_num = nums
        self.o_size = n_size
        self.print("原图分割为{} X {} 张图片".format(nums, c_h))

        for y in range(0, n_h, n_size):
            for x in range(0, n_w, n_size):
                n_img = img[y:y + n_size, x:x + n_size]
                c_n, maxsum = self.get_color(n_img)
                res_list.append([str(int(y / n_size)), str(int(x / n_size)), str(c_n), str(maxsum)])

        c_dict = dict()
        for idx in range(1, len(res_list)):
            y, x, c_n, maxsum = res_list[idx]
            c_dict.setdefault(c_n, [])
            c_dict[c_n].append([y, x, maxsum])

        for k, v in c_dict.items():
            self.print("开始写入文件 s_{}.txt".format(k))
            with open("./data/s_{}.txt".format(k), 'w') as f:
                for item in v:
                    f.write("{}\n".format(",".join(item)))

    def read_all_pic(self):
        self.print("开始提取文件夹图片")
        res_list = []
        for item in os.listdir(self.dir_path):
            img = cv2.imread(os.path.join(self.dir_path, item))
            img = cv2.resize(img, (self.o_size, self.o_size))
            c_n, maxsum = self.get_color(img)
            res_list.append([str(c_n), str(maxsum), str(item)])

        c_dict = dict()
        for idx in range(len(res_list)):
            c_n, maxsum, path = res_list[idx]
            c_dict.setdefault(c_n, [])
            c_dict[c_n].append([maxsum, path])

        for k, v in c_dict.items():
            self.print("开始写入文件 a_{}.txt".format(k))
            with open("./data/a_{}.txt".format(k), 'w') as f:
                for item in v:
                    f.write("{}\n".format(",".join(item)))

    def match_pic(self):
        self.print("开始根据颜色匹配图片")
        mc_d = {}
        for item in os.listdir("./data"):
            if item.startswith("s_"):
                if item.replace("s_", "a_") in os.listdir("./data"):
                    mc_d[item] = item.replace("s_", "a_")

        res_list = []

        for k, v in mc_d.items():
            s_list = []
            a_list = []
            with open("./data/{}".format(k), 'r') as f:
                s_list = [item for item in f.readlines()]
            with open("./data/{}".format(v), 'r') as f:
                a_list = [item for item in f.readlines()]

            for item in s_list:
                its = random.choice(a_list)
                y, x, _ = tuple(item.split(","))
                _, path = tuple(its.split(","))
                res_list.append([y, x, path.replace("\n", "")])
        self.print("开始写入匹配参数")
        with open(self.match_res, "w") as f:
            for item in res_list:
                f.write("{}\n".format(",".join(item)))

    def draw_img(self):
        self.print("开始绘制新图片")
        w = self.w_num
        h = self.h_num
        nums = self.min_size
        n_img = np.zeros([h * nums, w * nums, 3], dtype=np.uint8)
        t_list = []
        with open(self.match_res, 'r') as f:
            t_list = [item for item in f.readlines()]

        for item in t_list:
            y, x, path = tuple(item.split(","))
            y = int(y)
            x = int(x)
            path = path.replace("\n", "")
            t_img = cv2.imread("{}/{}".format(self.dir_path, path))
            t_img = cv2.resize(t_img, (nums, nums))
            n_img[y * nums:(y + 1) * nums, x * nums:(x + 1) * nums] = t_img

        cv2.imwrite(self.temp_img_path, n_img)

    def add_pic(self):
        self.print("开始合并图片")
        w = self.w_num
        h = self.h_num
        nums = self.min_size
        o_nums = self.o_size

        img1 = cv2.imread(self.pic_path)
        img1 = img1[:h * o_nums, :w * o_nums]
        img1 = cv2.resize(img1, (w * nums, h * nums))
        img2 = cv2.imread(self.temp_img_path)
        img_mix = cv2.addWeighted(img1, 0.6, img2, 0.4, 0)
        cv2.imwrite(self.out_img_path, img_mix)

    def run(self):
        self.get_pic_color()
        self.read_all_pic()
        self.match_pic()
        self.draw_img()
        self.add_pic()
        self.print("操作成功,请查看文件{}".format(self.out_img_path))

    def print(self, s):
        print("log ===> {} ...".format(s))


if __name__ == '__main__':
    pm = picMosaic("/home/herb/code/data/female/李沁/105.jpg", "/home/herb/code/data/female_face2/李沁")
    pm.run()
