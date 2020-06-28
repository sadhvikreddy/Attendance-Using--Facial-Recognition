import cv2
from SourceCode.Web.Codes import fr
import sqlite3 as db
import json


global know_face_encoding
know_face_encoding = []
global know_face_names
know_face_names = []

conn = db.connect('Database.db')
cur = conn.cursor()

cur.execute("select name,facedata from employee")
data = cur.fetchall()
for i in data:
    a = i[0]
    know_face_names.append(a)
    b = json.loads(i[1])
    know_face_encoding.append(b)


class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        self.name1 = "Unknown"


    def __del__(self):
        self.video.release()

    def get_frame(self):
        self.success, self.image1 = self.video.read()
        self.imag = cv2.resize(self.image1, (640, 360))
        self.process_this_frame = True
        if self.process_this_frame:
            face_locations = fr.face_locations(self.imag)
            face_encodings = fr.face_encodings(self.imag, face_locations)
            face_names = []
            for face_encoding in face_encodings:
                matches = fr.compare_faces(know_face_encoding, face_encoding, 0.40)
                name = "Unknown"
                if True in matches:
                    first_match_index = matches.index(True)
                    name = know_face_names[first_match_index]
                face_names.append(name)
        self.process_this_frame = not self.process_this_frame
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            cv2.rectangle(self.imag, (left, top), (right, bottom), (0, 0, 150), 1)
            cv2.rectangle(self.imag, (left + 5, bottom - 20), (right - 5, bottom - 5), (192, 192, 192), cv2.FILLED)
            font = cv2.FONT_HERSHEY_PLAIN
            cv2.putText(self.imag, name, (left + 6, bottom - 8), font, 1, (10, 10, 10), 1)
            self.name1 = name
        ret, jpeg = cv2.imencode('.jpg', self.imag)
        return jpeg.tobytes(),self.name1
