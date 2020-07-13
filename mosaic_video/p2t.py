# @time     : 2020/7/8 23:12
# @author  : HerbLee
# @file    : p2t.py
import cv2
import os
import numpy as np
import shutil
from moviepy.editor import *

"""
视频转换为txt视频
文件所需要的cv2 和 moviepy
    
    python 版本3.x
    需要额外安装
    pip install opencv-python
    pip install moviepy
"""


class Video2Txt:

    def __init__(self, video_path, temp_path="./temp", out_video_path="./out.mp4"):
        self.video_path = video_path
        self.temp_path = temp_path
        self.pic_temp = os.path.join(temp_path, "pic")
        self.out_video_path = out_video_path
        self.out_video_temp_path = out_video_path.replace(".mp4", "-temp.mp4")
        self.txt_pic_temp = os.path.join(temp_path, "tp")
        self.fps = 25
        self.v_width = 400
        self.v_height = 400

        self.g_scale_1 = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
        self.g_scale_2 = "@%#*+=-:. "

        if not os.path.exists(self.pic_temp):
            os.makedirs(self.pic_temp)
        elif len(os.listdir(self.pic_temp)) > 0:
            shutil.rmtree(self.pic_temp)
            os.makedirs(self.pic_temp)

        if not os.path.exists(self.txt_pic_temp):
            os.makedirs(self.txt_pic_temp)
        elif len(os.listdir(self.txt_pic_temp)) > 0:
            shutil.rmtree(self.txt_pic_temp)
            os.makedirs(self.txt_pic_temp)

    def split_video(self):
        """
        分割视频
        :return:
        """
        print("=====> 开始分析图片...")
        cap = cv2.VideoCapture(self.video_path)
        self.fps = cap.get(cv2.CAP_PROP_FPS)
        self.v_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.v_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        is_opend = cap.isOpened()
        i = 0
        while is_opend:
            i += 1
            flag, frame = cap.read()
            file_name = os.path.join(self.pic_temp, "{}.jpg".format(i))
            print("=====> 保存图片{}".format(file_name))
            if flag:
                cv2.imwrite(file_name, frame)
                cv2.waitKey(1)
            else:
                break
        cap.release()
        print("=====> 图片分析结束...")

    def get_average_l(self, image):
        """
        获取区域内高亮
        :param image:
        :return:
        """
        w, h = image.shape
        return np.average(image.reshape(w * h))

    def covert_image_to_ascii(self, file_name, cols, scale=1):
        """
        图片转换成字符
        :param file_name:
        :param cols:
        :param scale:
        :return: [[],[]]
        """
        img = cv2.imread(file_name, False)
        H, W = img.shape
        if W > H:
            cols = 100
        w = int(W / cols)
        h = int(w / scale)
        rows = int(H / h)

        aimg = []
        for j in range(rows):
            y1 = int(j * h)
            y2 = int((j + 1) * h)
            # print("y1, {} y2 {}".format(y1,y2))
            if j == rows - 1:
                y2 = H
            aimg.append("")
            for i in range(cols):
                x1 = int(i * w)
                x2 = int((i + 1) * w)
                # print("x1, {} x2 {}".format(x1,x2))
                if i == cols - 1:
                    x2 = W
                img_temp = img[y1:y2, x1:x2]

                avg = int(self.get_average_l(img_temp))
                # g_sval = self.g_scale_1[int((avg * 69) / 255)]
                g_sval = self.g_scale_2[int((avg * 9) / 255)]
                aimg[j] += g_sval
        return aimg, rows, cols

    def pic_2_txt(self):
        """
        转换图片
        :return:
        """
        print("=====> 开始转换图片...")
        for item in os.listdir(self.pic_temp):
            img_file = os.path.join(self.pic_temp, item)

            out_file = os.path.join(self.txt_pic_temp, item.split(".")[0] + ".jpg")

            self.pic_2_t(img_file, out_file)

        print("=====> 图片转换结束...")

    def pic_2_t(self, img_file, out_file):
        print("=====> 转换图片{}".format(img_file))

        p_dict, r, c = self.covert_image_to_ascii(img_file, 50)
        img1 = np.ones((r * 10, c * 10), dtype=np.uint8) * 255

        height, width = img1.shape
        for x in range(0, width, 10):
            for y in range(0, height, 10):
                # print(x, y)
                z = p_dict[int(y / 10)][int(x / 10)]
                img1 = cv2.putText(img1, z, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0))

        cv2.imwrite(out_file, img1)

    def pic_2_video(self):
        """
        合成视频
        :param name:
        :return:
        """
        print("=====> 开始合成视频...")
        fourcc = cv2.VideoWriter_fourcc("m", "p", "4", "v")
        temp = cv2.imread(os.path.join(self.txt_pic_temp, os.listdir(self.txt_pic_temp)[0]), False)
        video_write = cv2.VideoWriter(filename=self.out_video_temp_path, fourcc=fourcc, fps=self.fps,
                                      frameSize=(temp.shape[1], temp.shape[0]))
        for item in range(len(os.listdir(self.txt_pic_temp))):
            print("=====> 读取{}".format(item))
            img = cv2.imread(os.path.join(self.txt_pic_temp, str(item + 1) + ".jpg"))
            cv2.waitKey(60)
            video_write.write(img)
        video_write.release()
        print("=====> 视频合成结束...")

    def get_audio(self):
        video = VideoFileClip(self.video_path)
        audio = video.audio
        return audio

    def _destroy(self):
        os.remove(self.out_video_temp_path)

    def merge_av(self):
        audio = self.get_audio()
        vp2 = VideoFileClip(self.out_video_temp_path)
        vp3 = vp2.set_audio(audio)
        vp3.write_videofile(self.out_video_path)


    def run(self):
        self.split_video()
        self.pic_2_txt()
        self.pic_2_video()
        self.merge_av()
        self._destroy()


if __name__ == '__main__':
    folder_path = os.getcwd()
    vt = Video2Txt("{}/demo.mp4".format(folder_path), "{}/temp".format(folder_path), "{}/demo1.mp4".format(folder_path))
    vt.run()
