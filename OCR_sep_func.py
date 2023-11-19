import cv2
import pytesseract
import imutils
from . import image_conv
import os
import numpy as np
import requests

img_path = "C:/Work/MHA_Internship/project/Sample_imgs"
pdf_path = "C:/Work/MHA_Internship/project/Sample"
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def Self_OCR_creation(ImgPath):
    # Resize, grayscale, Otsu's threshold
    image = cv2.imread(ImgPath)
    image = imutils.resize(image, height= 700, width=900)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
    # find otsu's threshold value with OpenCV function
    otsu = cv2.threshold(gray,0,255,cv2.THRESH_TRUNC+cv2.THRESH_OTSU)[1]
    inverted = 255 - otsu
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,3))
    close = cv2.morphologyEx(inverted, cv2.MORPH_CLOSE, kernel, iterations=1)
    
    cnts = cv2.findContours(close, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        area = cv2.contourArea(c)
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.01 * peri, True)
        x,y,w,h = cv2.boundingRect(approx)
        aspect_ratio = w / float(h)
        if (aspect_ratio >= 2.5 or area < 75):
            cv2.drawContours(otsu, [c], -1, (255,255,255), -1)    
    otsu = cv2.pyrUp(otsu)
    d_otsu = cv2.addWeighted(otsu, 2.3, np.zeros(image.shape, image.dtype), 0, 1)
    txt = pytesseract.image_to_string(d_otsu, config='-l eng --psm 1')
    
    return txt

if (os.listdir(img_path) == 0):
    image_conv.pti_fold()
    
elif (len(os.listdir(pdf_path)) > len(os.listdir(img_path))):  
    image_conv.clear_fold()
    image_conv.pti_fold()

def check_func(filename):

    mon_dict = {"01":31,"02":28,"03":31,"04":30,"05":31,"06":30,"07":31,"08":31,"09":30,"10":31,"11":30,"12":31}

    while True:
        
        name = input("\nEnter Your Name here: ")
        DOB = input("\nEnter Your Date of Birth here (DD/MM/YYYY): ")

        name = name.upper()
        
        txt = Self_OCR_creation(os.path.join(img_path,filename)).upper()
        
        if (name != "" or name != " "):
            if ((DOB[3:5] in mon_dict.keys()) and (mon_dict[DOB[3:5]] >= int(DOB[:2]))) or (DOB[3:5] == "XX" and DOB[:2] == "XX"):
                name_lst = name.split()
                
                for i in range(len(name_lst)):
                    if name_lst[i] not in txt:
                        return 0
                
                if DOB not in txt:
                    return 2
                else: 
                    return 1
            else:
                return 2
        else:
            return 0

res = check_func("C:/Work/MHA_Internship/project/Sample_2.png")

"""for i in os.listdir(img_path):
    res = check_func(os.path.join(img_path,i))"""

if (res == 0):
    print("The given name does not match the data given in document. Please recheck the spelling or the submitted document")

elif (res == 1):
    print("All data has been verified. Thank you for your cooperation.")

elif (res == 2):
    print("The given date of birth does not match the data given in document. Please recheck the data given or the submitted document")

#indent the above if-elif-else if you uncomment the for loop
