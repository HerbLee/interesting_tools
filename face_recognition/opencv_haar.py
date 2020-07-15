# @time     : 2020/7/13 23:28
# @author  : HerbLee
# @file    : opencv_haar.py


import cv2
import os


def show(img):
    cv2.imshow("123", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def compute_center(w, h, faces):
    max_measure = 0
    for item in faces:
        x, y, w, h = item
        if w * h > max_measure:
            max_measure = w * h




def detect_face(pic_path):
    face_cascade = cv2.CascadeClassifier("./haarcascade_frontalface_default.xml")
    img = cv2.imread(pic_path)
    faces = face_cascade.detectMultiScale(img, 1.3, 5)
    compute_center(faces)
    # for (x, y, w, h) in faces:
    #     img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
    # show(img)


if __name__ == '__main__':
    # folder = "D:\Projects\data\沈月\护士造型写真图片"
    # folder = os.path.join(folder, "0.jpg")
    # print(folder)
    detect_face("./0.jpg")
