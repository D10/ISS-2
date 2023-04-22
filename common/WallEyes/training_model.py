import os
import sys
import pickle
import time

import face_recognition as fr
import cv2

from util import get_encoded_face

dataset_video_dir = 'dataset_from_video'


def train_model_by_img(name):

    if not os.path.exists('images/dataset'):
        print('[ERROR] there is no directory dataset')
        sys.exit()

    known_encodings = []
    images = os.listdir('images/dataset')

    print(images)

    for i, image in enumerate(images):
        print(f'[+] processing img {i + 1}/{len(images)}')

        print(get_encoded_face(f'images/dataset/{image}'))
        face_enc = get_encoded_face(f'images/dataset/{image}')[0]

        if not known_encodings:
            known_encodings.append(face_enc)
        else:
            for known_encoding in known_encodings:
                result = fr.compare_faces([face_enc], known_encoding)

                if result[0]:
                    known_encodings.append(face_enc)
                    break
                else:
                    break

    data = {
        "name": name,
        "encodings": known_encodings
    }

    with open(f'db_encodings/{name}_enc.pickle', 'wb') as file:
        file.write(pickle.dumps(data))

    print(f'[INFO] Person {name} successfully added')


def take_screenshot_from_video():
    cap = cv2.VideoCapture(0)  # Здесь воткнуть вебку

    if not os.path.exists(dataset_video_dir):
        os.mkdir(dataset_video_dir)

    while True:
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)

        fps = cap.get(cv2.CAP_PROP_FPS)
        multiplier = fps * 3

        if ret:
            frame_id = int(round(cap.get(1)))
            cv2.imshow("frame", frame)
            k = cv2.waitKey(2)

            if frame_id % multiplier == 0:
                cv2.imwrite(f'{dataset_video_dir}/screen_{time.time()}.png', frame)

            if k == ord(' '):
                cv2.imwrite(f'{dataset_video_dir}/extra_screen_{time.time()}.png', frame)

            if len(os.listdir(dataset_video_dir)) > 30:
                break

        else:
            print('Quit')
            break

    cap.release()
    cv2.destroyAllWindows()


def main():
    train_model_by_img('victoriya')


if __name__ == '__main__':
    main()
