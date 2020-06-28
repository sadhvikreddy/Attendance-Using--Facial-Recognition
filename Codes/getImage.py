import cv2
import dlib
from shutil import copyfile as cp
import os


def capture():
    camera = cv2.VideoCapture(0)
    ret, image1 = camera.read()
    image = cv2.resize(image1,(640,360))
    cv2.imwrite("file.jpg", image)

    face_detector = dlib.get_frontal_face_detector()

    detected = face_detector(image, 1)
    camera.release()
    if(detected):
        for i, face_rect in enumerate(detected):
            cv2.rectangle(image,(face_rect.left(),face_rect.top()),(face_rect.right(),face_rect.bottom()),(0,0,150),2)

            cv2.imwrite("file1.jpg", image)
            cp('file1.jpg','/Users/sadhvik/Documents/MiniProject/SourceCode/Web/static/InsertImage/file1.jpg')
            os.remove("file1.jpg")
            return True
    else:
        return False
