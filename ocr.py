import cv2
import numpy as np
import pytesseract

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
#preprocess
def process(image_path):
    img = cv2.imread(image_path)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    img_bin = cv2.Canny(img_gray,50,110)
    dil_kernel = np.ones((3,3), np.uint8)
    result=cv2.dilate(img_bin,dil_kernel,iterations=1)

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Get binary-mask
    msk = cv2.inRange(hsv, np.array([0, 0, 175]), np.array([179, 255, 255]))

    krn = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 3))
    dlt = cv2.dilate(msk, krn, iterations=1)
    thr = 255 - cv2.bitwise_and(dlt, msk)

    #findContours
    imgcopy = img.copy()
    cnts = cv2.findContours(result, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        area = cv2.contourArea(c)
        if area < 1000:
            cv2.drawContours(imgcopy, cnts, -1, (0, 0, 255), 3)
    #detected box
    img1 = np.zeros(result.shape)
    edges = cv2.Canny(img, 50, 110)

    src = cv2.dilate(edges,dil_kernel,iterations=1)

    iteration=1
    for _ in range(iteration):
        lines = cv2.HoughLinesP(image=src, rho=1, theta=np.pi / 180,threshold=100, lines=np.array([]),minLineLength=20, maxLineGap=100)
        a, b, c = lines.shape
        for i in range(a):
            x1, y1, x2, y2 = lines[i][0][0], lines[i][0][1], lines[i][0][2], lines[i][0][3]
            cv2.line(img1, (x1, y1), (x2, y2),255, 1, cv2.LINE_AA)
            src = cv2.convertScaleAbs(img1)


    imgX = cv2.GaussianBlur(img1, (1, 1), 0)
    kernelx = cv2.getStructuringElement(cv2.MORPH_RECT, (1, imgX.shape[0] // 30))
    imgY = cv2.Sobel(img1, cv2.CV_64F, 1, 0)
    imgY = cv2.convertScaleAbs(imgY)
    cv2.normalize(imgY, imgY, 0, 255, cv2.NORM_MINMAX)
    imgY = cv2.morphologyEx(imgY, cv2.MORPH_CLOSE, kernelx, iterations=1)


    imgY2 = cv2.GaussianBlur(img1, (1, 1), 0)
    kernely = cv2.getStructuringElement(cv2.MORPH_RECT, (imgY2.shape[1] // 30, 1))
    imgX2 = cv2.Sobel(img1, cv2.CV_64F, 0, 1)
    imgX2 = cv2.convertScaleAbs(imgX2)
    cv2.normalize(imgX2, imgX2, 0, 255, cv2.NORM_MINMAX)
    imgX2 = cv2.morphologyEx(imgX2, cv2.MORPH_CLOSE, kernely, iterations=1)

    img_bin_final= cv2.bitwise_or(imgX2,imgY)
    final_kernel = np.ones((3,3), np.uint8)
    img_bin_final=cv2.dilate(img_bin_final,final_kernel,iterations=1)

    ret, labels, stats,centroids = cv2.connectedComponentsWithStats(~img_bin_final, connectivity=8, ltype=cv2.CV_32S)



    result = ''
    for x,y,w,h,area in stats[1:]:
    #     cv2.putText(image,'box',(x-10,y-10),cv2.FONT_HERSHEY_SIMPLEX, 1.0,(0,255,0), 2)
        if area>100:
            cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
            cropped = img[y:y + h, x:x + w]
            txt = pytesseract.image_to_string(cropped, config="--psm 6 -c page_separator=''")
        
            numeric_string = "".join(filter(str.isdigit, txt))
            if numeric_string == '':
                numeric_string = '0'
            result = result + numeric_string + " "
    return result

print(process('Sudoku.png'))