import tensorflow as tf
import numpy as np
import PIL.Image as Image
import os
from urllib import request
import uuid

RECOGNIZER_MODEL = os.getenv('RECOGNIZER_MODEL')
UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER')


IMAGE_SHAPE = (224, 224)
model = tf.keras.models.load_model(RECOGNIZER_MODEL)
normalization_layer = tf.keras.layers.Rescaling(1./255)
class_names = np.array(
    ['маргаритка', 'одуванчик', 'розы', 'подсолнухи', 'тюльпаны'])


def get_path_for_saving():
    local_file = f'{uuid.uuid4()}.jpg'
    full_path = os.path.join(UPLOAD_FOLDER, local_file)
    return full_path


def save_tmp_photo(remote_url):
    full_path = get_path_for_saving()
    request.urlretrieve(remote_url, full_path)
    return full_path


def remove_tmp_photo(full_path):
    os.remove(full_path)


def recognize_flower(full_path):
    uploaded_image = Image.open(full_path).resize(IMAGE_SHAPE)
    normalized_uploaded_image = normalization_layer(uploaded_image)

    img_array = tf.keras.utils.img_to_array(normalized_uploaded_image)
    img_array = tf.expand_dims(img_array, 0)

    result_batch = model.predict(img_array)
    result_batch_id = tf.math.argmax(result_batch, axis=-1)

    prediction = class_names[tuple(result_batch_id)]
    return prediction
