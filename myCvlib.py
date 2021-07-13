import cv2
import matplotlib.pyplot as plt
import numpy as np
import math

def pinch(img,p,a):
    for x in range(img.shape[0]):
        for y in range(img.shape[1]):
            print(img[x,y])


def localTranslationWarp(srcImg, startX, startY, endX, endY, radius):
    ddradius = float(radius * radius)
    copyImg = np.zeros(srcImg.shape, np.uint8)
    copyImg = srcImg.copy()

    # 计算公式中的|m-c|^2
    ddmc = (endX - startX) * (endX - startX) + (endY - startY) * (endY - startY)
    H, W, C = srcImg.shape
    for i in range(W):
        for j in range(H):
            # 计算该点是否在形变圆的范围之内
            # 优化，第一步，直接判断是会在（startX,startY)的矩阵框中
            if math.fabs(i - startX) > radius and math.fabs(j - startY) > radius:
                continue

            distance = (i - startX) * (i - startX) + (j - startY) * (j - startY)

            if (distance < ddradius):
                # 计算出（i,j）坐标的原坐标
                # 计算公式中右边平方号里的部分
                ratio = (ddradius - distance) / (ddradius - distance + ddmc)
                ratio = ratio * ratio

                # 映射原位置
                UX = i - ratio * (endX - startX)
                UY = j - ratio * (endY - startY)

                # 根据双线性插值法得到UX，UY的值
                value = BilinearInsert(srcImg, UX, UY)
                # 改变当前 i ，j的值
                copyImg[j, i] = value

    return copyImg


# 双线性插值法
def BilinearInsert(src, ux, uy):
    w, h, c = src.shape
    if c == 3:
        x1 = int(ux)
        x2 = x1 + 1
        y1 = int(uy)
        y2 = y1 + 1

        part1 = src[y1, x1].astype(np.float) * (float(x2) - ux) * (float(y2) - uy)
        part2 = src[y1, x2].astype(np.float) * (ux - float(x1)) * (float(y2) - uy)
        part3 = src[y2, x1].astype(np.float) * (float(x2) - ux) * (uy - float(y1))
        part4 = src[y2, x2].astype(np.float) * (ux - float(x1)) * (uy - float(y1))

        insertValue = part1 + part2 + part3 + part4

        return insertValue.astype(np.int8)


if __name__ == '__main__':
    a = cv2.imread("21110112100499.JPG")
    a = cv2.cvtColor(a, cv2.COLOR_BGR2RGB)

    h, w, d = a.shape

    plt.subplot(121)
    plt.imshow(a)

    c=np.zeros_like(a,a.dtype)
    """
    for i in range(w-1):
        for j in range(h-1):
            c[j][i]=BilinearInsert(a,i*0.5,j*0.5)
    """
    c = localTranslationWarp(a,0,0,200,400,500)
    cv2.rectangle(c,(0,0),(200,400),(0,0,0))
    cv2.circle(c,(0,0),500,(0,0,0))
    plt.subplot(122)
    plt.imshow(c)

    #plt.subplot(133)
    #plt.imshow(d)
    plt.show()
    #print(pinch(a,(0,0),1))