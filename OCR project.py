import zipfile
from zipfile import ZipFile 
import math
from PIL import Image , ImageOps, ImageDraw
import pytesseract
import cv2 as cv
import numpy as np
#from IPython.display import Image


# loading the face detection classifier
face_cascade = cv.CascadeClassifier('readonly/haarcascade_frontalface_default.xml')

#file_name = "readonly/images.zip"
file_name = "readonly/images.zip"

dic = {}
with ZipFile(file_name, 'r') as zip: 
    for entry in zip.infolist():
        with zip.open(entry) as news_paper:
            image = Image.open(news_paper).convert('RGB')
            dic[entry.filename] = {'image':image}

for one_image in dic.keys():
    text = pytesseract.image_to_string(dic[one_image]['image'])
    dic[one_image]['text'] = text
    
print(dic.keys())

for i in dic.keys():
    image = np.array(dic[i]['image']) 
    image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    bounding_boxes = face_cascade.detectMultiScale(image, 1.5, 5)
    dic[i]['photos'] = []
    for x,y,w,h in bounding_boxes:
        face = dic[i]['image'].crop((x,y,x+w,y+h))
        dic[i]['photos'].append(face)


for i in dic.keys():
    for p in dic[i]['photos']:
        p.thumbnail((100,100),Image.ANTIALIAS)

def search(keyword):
    for i in dic:
        if keyword in dic[i]['text']:
            if(len(dic[i]['photos']) != 0):
                print("Result found in file {}".format(i))
                h = math.ceil(len(dic[i]['photos'])/5)
                contact_sheet=Image.new('RGB',(500, 100*h))
                x_new = 0
                y_new = 0
                for img in dic[i]['photos']:
                    contact_sheet.paste(img, (x_new, y_new))
                    if x_new + 100 == contact_sheet.width:
                        x_new = 0
                        y_new += 100
                    else:
                        x_new += 100
                        
                display(contact_sheet)
            else:
                print("Result found in file {} \nBut there were no faces in that file\n\n".format(i))
    return
