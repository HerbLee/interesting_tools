# @time     : 2020/7/17 15:22
# @author  : HerbLee
# @file    : demo.py

import cv2
from face_recognition.opencv_haar import detect_face


def get_face(path):
    img = cv2.imread(path)
    pc = detect_face(path)
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

    cv2.circle(img, (c_x, c_y), 4, (255, 0, 0))
    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 1)
    cv2.rectangle(img, (x0, y0), (x1, y1), (0, 0, 255), 1)

    cv2.imshow("1", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    print(target_w)

    return pc


if __name__ == '__main__':
    # img = cv2.imread("./0.jpg")
    # pc = detect_face("./0.jpg")
    pc = get_face("./0.jpg")
    print(pc)
