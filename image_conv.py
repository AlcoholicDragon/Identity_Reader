from PIL import Image
import os
from pdf2image import convert_from_path

path_to_file = "C:/Work/MHA_Internship/project/Sample"
path_to_img = "C:/Work/MHA_Internship/project/Sample_imgs"

def pti_fold():
    path_to_file = "C:\Work\MHA_Internship\project\Sample"

    for fileName in os.listdir(path_to_file):

        fileInpPath = os.path.join(path_to_file,fileName)

        image = convert_from_path(fileInpPath, poppler_path="C:/Mine/ehqwfihwihwqeiufuiefuhwficuh/Release-23.05.0-0/poppler-23.05.0/Library/bin")

        image[0].save(path_to_img+"/"+fileName[:len(fileName)-4]+".jpg",'JPEG')

def clear_fold():
    path_to_image = "C:/Work/MHA_Internship/project/Sample_imgs"
    
    for filename in os.listdir(path_to_image):
        os.remove(os.path.join(path_to_image,filename))
