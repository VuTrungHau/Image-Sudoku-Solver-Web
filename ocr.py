import cv2
import numpy as np
import pytesseract
from numpy.linalg import norm

def brightness(img):
    if len(img.shape) == 3:
        return np.average(norm(img, axis=2)) / np.sqrt(3)
    else:
        # Grayscale
        return np.average(img)

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

def find_contours(img, original):
    # find contours on thresholded image
    contours, hierachy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    imgcopy = original.copy()
    biggest = np.array([])
    max_area = 0
    for c in contours:
        area = cv2.contourArea(c)
        if area >1000:
            peri = cv2.arcLength(c,True)
            approx = cv2.approxPolyDP(c, 0.015 * peri, True)
            if area > max_area and len(approx) == 4:
                biggest = approx
                max_area = area
    # findCorners
    if len(biggest) > 1:
        points = biggest.reshape(4,2)
        input_points = np.zeros((4,2),dtype="float32")
    
        points_sum = points.sum(axis = 1)
        input_points[0] = points[np.argmin(points_sum)]
        input_points[3] = points[np.argmax(points_sum)]
    
        points_diff = np.diff(points, axis = 1)
        input_points[1] = points[np.argmin(points_diff)]
        input_points[2] = points[np.argmax(points_diff)]
    
        (top_left, top_right, bot_right, bot_left) = input_points
        bottom_width = np.sqrt(((bot_right[0] - bot_left[0])**2)+((bot_right[1]-bot_left[1])**2))
        top_width = np.sqrt(((top_right[0] - top_left[0])**2)+((top_right[1]-top_left[1])**2))
        right_height = np.sqrt(((top_right[0] - bot_right[0])**2)+((top_right[1]-bot_right[1])**2))
        left_height = np.sqrt(((top_left[0] - bot_left[0])**2)+((top_left[1]-bot_left[1])**2))
    
        max_width = max(int(bottom_width),int(top_width))
        max_height = int(max_width)
    
    #warpImg
        mapping = np.array([[0, 0], [max_width,0], [0,max_height], [max_width,max_height]], dtype='float32')
        matrix = cv2.getPerspectiveTransform(input_points, mapping)
        return cv2.warpPerspective(imgcopy,matrix,(max_width,max_height))
    return original
    
def process(img):
    #img = cv2.imread(image_path)
    img = cv2.resize(img, (250, 250)) 
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    img_bin = cv2.Canny(img_gray,0,75)
    dil_kernel = np.ones((3,3), np.uint8)
    img_bin=cv2.dilate(img_bin,dil_kernel,iterations=1)
    #cv2.imshow("h",img_bin)
    
    kernal_v = np.ones((40,1), np.uint8)
    img_bin_v = cv2.morphologyEx(img_bin, cv2.MORPH_OPEN, kernal_v)
    
    
    kernal_h = np.ones((1,40), np.uint8)
    img_bin_h = cv2.morphologyEx(img_bin, cv2.MORPH_OPEN, kernal_h)
    
    
    img_bin_final= cv2.bitwise_or(img_bin_h,img_bin_v)
    final_kernel = np.ones((1,1), np.uint8)
    img_bin_final=cv2.dilate(img_bin_final,final_kernel,iterations=1)
    #cv2.imshow("f",img_bin_final)
    
    
    # ret, labels, stats,centroids = cv2.connectedComponentsWithStats(~img_bin_final, connectivity=8, ltype=cv2.CV_32S)
    
    i=np.array([[2,2,24,24,576]
                ,[31,2,22,24,528]
                ,[58,2,23,24,552]
                ,[86,2,23,24,552]
                ,[114,2,22,24,528]
                ,[141,2,23,24,552]
                ,[169,2,23,24,552]
                ,[197,2,23,24,552]
                ,[225,2,22,24,528]
                ,[2,31,24,22,528]
                ,[31,31,22,22,484]
                ,[58,31,23,22,506]
                ,[86,31,23,22,506]
                ,[114,31,22,22,484]
                ,[141,31,23,22,506]
                ,[169,31,23,22,506]
                ,[197,31,23,22,506]
                ,[225,31,22,22,484]
                ,[2,58,24,23,552]
                ,[31,58,22,23,506]
                ,[58,58,23,23,529]
                ,[86,58,23,23,529]
                ,[114,58,22,23,506]
                ,[141,58,23,23,529]
                ,[169,58,23,23,529]
                ,[197,58,23,23,529]
                ,[225,58,22,23,506]
                ,[2,86,24,23,552]
                ,[31,86,22,23,506]
                ,[58,86,23,23,529]
                ,[86,86,23,23,529]
                ,[114,86,22,23,506]
                ,[141,86,23,23,529]
                ,[169,86,23,23,529]
                ,[197,86,23,23,529]
                ,[225,86,22,23,506]
                ,[2,114,24,22,528]
                ,[31,114,22,22,484]
                ,[58,114,23,22,506]
                ,[86,114,23,22,506]
                ,[114,114,22,22,484]
                ,[141,114,23,22,506]
                ,[169,114,23,22,506]
                ,[197,114,23,22,506]
                ,[225,114,22,22,484]
                ,[2,141,24,23,552]
                ,[31,141,22,23,506]
                ,[58,141,23,23,529]
                ,[86,141,23,23,529]
                ,[114,141,22,23,506]
                ,[141,141,23,23,529]
                ,[169,141,23,23,529]
                ,[197,141,23,23,529]
                ,[225,141,22,23,506]
                ,[2,169,24,23,552]
                ,[31,169,22,23,506]
                ,[58,169,23,23,529]
                ,[86,169,23,23,529]
                ,[114,169,22,23,506]
                ,[141,169,23,23,529]
                ,[169,169,23,23,529]
                ,[197,169,23,23,529]
                ,[225,169,22,23,506]
                ,[2,197,24,23,552]
                ,[31,197,22,23,506]
                ,[58,197,23,23,529]
                ,[86,197,23,23,529]
                ,[114,197,22,23,506]
                ,[141,197,23,23,529]
                ,[169,197,23,23,529]
                ,[197,197,23,23,529]
                ,[225,197,22,23,506]
                ,[2,225,24,22,528]
                ,[31,225,22,22,484]
                ,[58,225,23,22,506]
                ,[86,225,23,22,506]
                ,[114,225,22,22,484]
                ,[141,225,23,22,506]
                ,[169,225,23,22,506]
                ,[197,225,23,22,506]
                ,[225,225,22,22,484]])
    
    result = ''
    for x,y,w,h,area in i:
        if area>110:
            cropped = img[y:y + h, x:x + w]
            cropped = cv2.cvtColor(cropped,cv2.COLOR_BGR2GRAY)
            brn = brightness(cropped)
            if(brn>130):
                brn = 130
            else:
                brn = 55
            ret, cropped = cv2.threshold(cropped,brn,255,cv2.THRESH_BINARY)
            #cv2_imshow(cropped)
            txt = pytesseract.image_to_string(cropped, config="--psm 6 -c tessedit_char_whitelist=0123456789")# page_separator=''")
            #txt = pytesseract.image_to_string(cropped, config="digits")
            
            # print(txt)
            numeric_string = "".join(filter(str.isdigit, txt))
            if numeric_string == '':
                numeric_string = '0'
            if len(numeric_string) > 1:
                numeric_string = numeric_string[-1]
            result = result + numeric_string + " "
    #cv2_imshow(img)
    return result

#print(process('Sudoku.png'))