import time

from imutils.video import VideoStream, FPS
import numpy as np
import argparse
import imutils
import cv2
from telebot import TeleBot
ap = argparse.ArgumentParser()
ap.add_argument('-p', '--prototxt', required=True, help='path to Caffe deploy')
ap.add_argument('-m', '--model', required=True, help='compiled model')
ap.add_argument('-c', '--confidence', type=float, default=0.2, help='minimum probability')
args = vars(ap.parse_args())
def start_stream(bot:TeleBot, message):
    CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat", "chair", "cow",
               "diningtable", "dog", "horse", "motorbike", "person", "pottedplant", "sheep", "sofa", "train", "tvmonitor"]
    COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))
    print('loading model....')
    net = cv2.dnn.readNetFromCaffe(args['prototxt'], args['model'])
    print('start videostream...')
    KNOW_DISTANCE = 30
    KNOW_WIDTH = 14.3
    FONTS = cv2.FONT_HERSHEY_COMPLEX
    # colors

    GREEN = (0, 255, 0)
    RED = (0, 0, 255)
    WHITE = (255, 255, 255)

    face_detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")


    def Focal_length(measured_distance, real_width, width_in_rf_image):
        focal_length = (width_in_rf_image * measured_distance) / real_width
        return focal_length


    def Distance_finder(Focal_length, real_face_width, face_width_in_frame):
        distance = (real_face_width * Focal_length) / face_width_in_frame
        return distance


    def face_data(image):
        face_width = 0
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = face_detector.detectMultiScale(gray_image, 1.3, 5)
        for (x, y, h, w) in faces:
            cv2.rectangle(image, (x, y), (x + w, y + h), WHITE, 1)
            face_width = w
        return face_width


    ref_image = cv2.imread("Ref_image.png")

    ref_image_face_width = face_data(ref_image)
    Focal_length_found = Focal_length(KNOW_DISTANCE, KNOW_WIDTH, ref_image_face_width)
    print(Focal_length_found)
    cv2.imshow("ref_image", ref_image)

    bot.send_message(message.from_user.id,'Start...')
    vs = VideoStream(src=0).start()
    time.sleep(2.0)
    fps = FPS().start()

    while True:
        frame = vs.read()
        frame = imutils.resize(frame, width=700)
        (h, w) = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(frame, (700, 700)), 0.007843, (700, 700), 127.5)

        net.setInput(blob)
        detections = net.forward()
        face_width_in_frame = face_data(frame)
        print(face_width_in_frame)
        if face_width_in_frame != 0:
            Distance = Distance_finder(Focal_length_found, KNOW_WIDTH, face_width_in_frame)
            cv2.putText(frame, f"Distance = {Distance}", (50, 50), FONTS, 0.6, (WHITE), 2)

        cv2.imshow('Frame', frame)
        for i in np.arange(0, detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > args['confidence']:
                idx = int(detections[0, 0, i, 1])
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype('int')
                label = '{}: {:.2f}%'.format(CLASSES[idx], confidence * 100)

                if CLASSES[idx] == 'person':
                    cv2.imwrite('photo.jpg',frame )
                    img = open('photo.jpg', 'rb')
                    bot.send_photo(message.from_user.id, img)
                    img.close()
                    time.sleep(10.0)

                cv2.rectangle(frame, (startX, startY), (endX, endY), COLORS[idx], 2)
                y = startY - 15 if startY - 15 > 15 else startY
                cv2.putText(frame, label, (startX, y), cv2.FONT_HERSHEY_TRIPLEX, 0.5, COLORS[idx], 2)

        cv2.imshow('Frame', frame)
        key = cv2.waitKeyEx(1) & 0xFF

        if key == ord('q'):
            break

        fps.update()

    fps.stop()
    cv2.destroyAllWindows()
    vs.stop()
# for start command
# python VideoAi.py -p MobileNetSSD_deploy.prototxt.txt -m MobileNetSSD_deploy.caffemodel
