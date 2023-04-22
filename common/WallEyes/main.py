import os
import pickle

import face_recognition as fr
import cv2

from util import get_encoded_face


def compare_faces(img1_path: str, img2_path: str):
    img1_encodings = get_encoded_face(img1_path)[0]
    img2_encodings = get_encoded_face(img2_path)[0]

    compare_result = fr.compare_faces([img1_encodings], img2_encodings)

    print(compare_result)


def face_recognizing(cap, dataset):
    ret, frame = cap.read()
    # frame = cv2.flip(frame, 1)

    locations = fr.face_locations(frame)
    encodings = fr.face_encodings(frame, locations)

    for face_encoding, face_location in zip(encodings, locations):
        match = None
        for data in dataset:
            result = fr.compare_faces(data['encodings'], face_encoding)

            if all(result):
                match = data['name']
                print(match)

        # left_top = (face_location[3], face_location[0])
        # right_bottom = (face_location[1], face_location[2])
        # color = (255, 0, 0)
        # cv2.rectangle(frame, left_top, right_bottom, color, 4)
        #
        # left_bottom = (face_location[3], face_location[2])
        # right_bottom = (face_location[1], face_location[2] + 20)
        # cv2.rectangle(frame, left_bottom, right_bottom, color, cv2.FILLED)
        # cv2.putText(
        #     frame,
        #     match,
        #     (face_location[3] + 10, face_location[2] + 15),
        #     cv2.FONT_HERSHEY_SIMPLEX,
        #     1,
        #     (255, 255, 255),
        #     4
        # )


def detect_person_in_video():
    dataset = []
    for data_enc in os.listdir('db_encodings'):
        read_data = pickle.loads(open(f'db_encodings/{data_enc}', 'rb').read())
        dataset.append(read_data)

    cap = cv2.VideoCapture(0)
    cv2.resizeWindow('some', 250, 150)
    while True:
        face_recognizing(cap, dataset)

        # cv2.imshow("WallEyes test prototype", frame)
        # cv2.waitKey(25)


def main():
    detect_person_in_video()


if __name__ == '__main__':
    main()
