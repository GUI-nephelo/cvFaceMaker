import face_recognition as fr
import cv2
import numpy as np
import matplotlib.pyplot as plt
from time import sleep
from time import time
import myCvlib
import math

#base function
def getMark(path):
    img = fr.load_image_file(path)
    marks=fr.face_landmarks(img)
    return marks

def lines(img,pts,color,circle=False,thickness = None, lineType = None, shift = None):
    for i in range(len(pts)):
        cv2.line(img,pts[i],pts[(0 if i+1 >= len(pts) else i+1) if circle else (i+1 if i+1<len(pts) else i)],color,thickness=thickness,lineType=lineType,shift=shift)


#face operate
def blink(imgPath):
    img = cv2.imread(imgPath)
    marks = getMark(imgPath)[0]

    right_eye_area = np.array(marks["left_eye"])
    left_eye_area = np.array(marks["right_eye"])
    ec = img[marks["nose_tip"][2]]

    # prepare mask
    mask = np.zeros(img.shape, dtype=np.uint8) * 255
    cv2.fillPoly(mask, [right_eye_area, left_eye_area], (255, 0, 255))
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 3))
    # masking
    mask = cv2.dilate(mask, kernel, iterations=3)
    mask = cv2.split(mask)[0]
    fg = np.zeros_like(img)
    fg[:, :, 0] = ec[0]
    fg[:, :, 1] = ec[1]
    fg[:, :, 2] = ec[2]
    lines(fg, np.array(marks["right_eye"][3:] + marks["right_eye"][0:1]) + np.array((0, 3)), (0, 0, 0), thickness=3)
    lines(fg, np.array(marks["left_eye"][3:] + marks["left_eye"][0:1]) + np.array((0, 3)), (0, 0, 0), thickness=3)
    fg = cv2.blur(fg, (9, 7))
    eyeslip_img = cv2.copyTo(fg, mask)
    none_eyeslip_img = cv2.copyTo(img, cv2.bitwise_not(mask))
    img = cv2.add(eyeslip_img, none_eyeslip_img)
    #img = cv2.morphologyEx(img, cv2.MORPH_ELLIPSE, kernel)
    return img

def mouthOpen(imgPath):
    img = cv2.imread(imgPath)
    marks = getMark(imgPath)[0]
    H, W, D = img.shape

    top_lip_area = np.array(marks["top_lip"])
    bottom_lip_area = np.array(marks["bottom_lip"])

    jaw_area = np.int32(marks["bottom_lip"][6:] + marks["bottom_lip"][0:1] + marks["chin"][11:4:-1])
    img0 = img.copy()
    img1 = cv2.fillPoly(img0, [jaw_area], (0, 0, 0))
    mask = cv2.inRange(img0, np.array([0, 0, 0]), np.array([0, 0, 0]))

    img0_ = cv2.copyTo(img, mask)

    x1, y1 = bottom_lip_area[3][0], bottom_lip_area[3][1]
    x2, y2 = top_lip_area[3][0], top_lip_area[3][1]
    x3, y3 = marks["chin"][8]
    """
    e in [1,+]
    """
    def slider_event(e):
        a = e
        img2 = myCvlib.localTranslationWarp(img0_, x2, y2, x1, y1, (y3 - y1) / a)
        img0 = img1 + img2
        mask = cv2.inRange(img0, np.array([0, 0, 0]), np.array([0, 0, 0]))
        zero = np.zeros_like(img0)
        zero[:, :, 0] = 10
        zero[:, :, 1] = 10
        zero[:, :, 2] = 90
        # 牙齿
        cv2.fillPoly(zero, [top_lip_area + np.array([0, 3])], (202, 259, 250))
        zero = cv2.erode(zero, cv2.getStructuringElement(cv2.MORPH_RECT, (5, 3)), )
        cv2.fillPoly(zero, [bottom_lip_area + np.array([0, 10])], (182, 239, 230))
        # 牙缝
        for i in range(2, 5):
            cv2.line(zero, top_lip_area[12 - i] + np.array([0, 3]), top_lip_area[i] + np.array([0, 3]), (0, 0, 0))
            cv2.line(zero, bottom_lip_area[12 - i] + np.array([0, 10]), bottom_lip_area[i] + np.array([0, 10]),
                     (0, 0, 0))
        img0 = img0 + cv2.copyTo(zero, mask)
        return img0
    return slider_event

#inter-operate
def operate():
    a = mouthOpen(imgPath)
    mouth = a(1)
    eye = blink(imgPath)
    common = cv2.imread(imgPath)
    cv2.imshow("as", common)
    while 1:
        k = cv2.waitKey(0)
        print(k)
        if k == ord("c"):
            cv2.imshow("as", common)
        if k == ord("e"):
            cv2.imshow("as", eye)
        if k == ord("m"):
            cv2.imshow("as", mouth)
        if k == ord("q") or k == -1:
            break

imgPath='21110112101465.JPG'


if __name__=="__main__":
    a = cv2.imread(imgPath)
    marks = getMark(imgPath)[0]

    chin_area = np.array(marks["chin"])
    print(chin_area[0:17:16])
    c = (chin_area[0]/2+chin_area[16]/2).astype(np.int32)
    cv2.circle(a,c,43,(0,0,0))
    axes=(chin_area[16]-chin_area[0])[0]
    cv2.ellipse(a,c,,math.pi/2,math.pi/2,math.pi/2,(0,0,0))



    for j in marks:
        for _,i in enumerate(marks[j]):
            cv2.putText(a,str(_),i,cv2.FONT_HERSHEY_PLAIN,1,(0,0,0))
            cv2.circle(a,i,3,(0,0,0))

    cv2.imshow("as",a)
    cv2.waitKey(0)