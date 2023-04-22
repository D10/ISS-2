import face_recognition as fr


def get_encoded_face(img_path):
    img = fr.load_image_file(img_path)
    img_encodings = fr.face_encodings(img)

    return img_encodings
