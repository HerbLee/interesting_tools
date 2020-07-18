# @time     : 2020/7/13 23:28
# @author  : HerbLee
# @file    : opencv_haar.py


import cv2
import os


class CvFaceImg:

    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier("./haarcascade_frontalface_default.xml")

    def get_face_rect(self, faces):
        max_measure = 0
        max_item = ()
        for item in faces:
            x, y, w, h = item
            if w * h > max_measure:
                max_measure = w * h
                max_item = item
        return max_item

    def new_pic(self, img, faces):
        pc = self.get_face_rect(faces)
        o_h, o_w, _ = img.shape
        target_w = o_w if o_h > o_w else o_h
        target = "v" if o_h > o_w else "h"

        x, y, w, h = pc
        c_x, c_y = int((x * 2 + w) / 2), int((y * 2 + h) / 2)

        x0, y0, x1, y1 = 0, 0, 0, 0

        if target == 'v':
            x0 = 0
            x1 = o_w
            if o_h - c_y > int(target_w / 2) and c_y > int(target_w / 2):
                y0 = c_y - int(target_w / 2)
                y1 = c_y + int(target_w / 2)
            elif o_h - c_y <= int(target_w / 2):
                y1 = o_h
                y0 = int(o_h - target_w)

            elif c_y <= int(target_w / 2):
                y0 = 0
                y1 = target_w

        else:
            y0 = 0
            y1 = o_h

            if o_w - c_x > int(target_w / 2) and c_x > int(target_w / 2):
                x0 = c_x - int(target_w / 2)
                x1 = c_x + int(target_w / 2)
            elif o_w - c_x <= int(target_w / 2):
                x1 = o_w
                x0 = int(o_w - target_w)
            elif c_x <= int(target_w / 2):
                x0 = 0
                x1 = target_w

        return x0, y0, x1, y1

    def detect_face(self, pic_path):
        img = cv2.imread(pic_path)

        faces = self.face_cascade.detectMultiScale(img, 1.3, 5)
        if len(faces) > 0:
            x0, y0, x1, y1 = self.new_pic(img, faces)
            return img[y0:y1, x0:x1]
        else:
            h, w, _ = img.shape
            t_size = h if w > h else w
            return img[0:t_size, 0:t_size]

    def run(self, folder):
        assert os.path.exists(folder), "文件夹不存在"
        if not os.path.exists("./temp"):
            os.makedirs("./temp")
        for files in os.listdir(folder):
            img = self.detect_face(os.path.join(folder, files))
            print("处理{}".format(files))
            cv2.imwrite("./temp/{}".format(files), img)
        print("处理完成")

if __name__ == '__main__':
    cf = CvFaceImg()
    cf.run("./data")
