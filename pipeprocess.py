import cv2
import numpy as np

count = 0

def preprocess(minr, maxr, p1, p2):
    print(minr, maxr, p1, p2)
    img = cv2.imread('pipe.jpg')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
##    edge = cv2.Canny(blur, 220, 240)
    ##kernel = np.ones((2,2), np.uint8)
    ##dilation = cv2.dilate(edge,kernel,iterations = 1)
    ##dilation = cv2.morphologyEx(dilation, cv2.MORPH_OPEN, kernel)
    rows = gray.shape[0]
    circles = cv2.HoughCircles(blur, cv2.HOUGH_GRADIENT, 1, rows / 40,
                                   param1=p1, param2=p2,
                               minRadius=minr, maxRadius=maxr)
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
        # circle outline
            center = (i[0], i[1])
            radius = i[2]
            cv2.circle(img, center, radius, (255, 255, 0), 2)
    ##        cv2.imshow("detected", img)
    ##        cv2.waitKey(0)
    ##closing = cv2.morphologyEx(edge, cv2.MORPH_OPEN, kernel)
##    cv2.imshow("gray", gray)
##    print(circles.shape)
    count = circles.shape[1]
##    cv2.imshow("gray->blur", blur)
##    ##cv2.imshow("gray->blur->canny->closed", dilation)
##    cv2.imshow("gray->blur->canny", edge)
    cv2.imshow("detected", img)
    cv2.imwrite("aa.jpg",img)
    return count
##    cv2.waitKey(0)
##    cv2.destroyAllWindows()
