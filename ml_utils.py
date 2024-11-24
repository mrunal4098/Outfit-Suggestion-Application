# wardrobe/ml_utils.py

import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import img_to_array, load_img
from sklearn.preprocessing import LabelEncoder
import pandas as pd
import os


# Path to the saved model and CSV file
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
saved_model_path = os.path.join(base_dir, 'saved_models', 'saved_model2.h5')
csv_file_path = os.path.join(base_dir, 'saved_models', 'final_csv.csv')
images_folder = os.path.join(base_dir, 'saved_models', 'images_hs')

# Load the trained model
model = tf.keras.models.load_model(saved_model_path)

# Load the CSV file
df = pd.read_csv(csv_file_path)

# Preprocess an image for testing
def preprocess_image(image_path, img_height=540, img_width=720):
    image = load_img(image_path, target_size=(img_height, img_width))
    image = img_to_array(image)
    image = image / 255.0
    image = np.expand_dims(image, axis=0)
    return image

# Load image paths and labels for encoding
def load_image_paths_and_labels(images_folder, df):
    image_paths = []
    labels = []
    for idx, row in df.iterrows():
        image_path = os.path.join(images_folder, f"{row['id']}.jpg")
        if os.path.exists(image_path):
            image_paths.append(image_path)
            labels.append(row[['articleType', 'baseColour', 'season', 'usage']].values)  # Include 'usage' here
    return image_paths, np.array(labels)

# Load image paths and labels
image_paths, labels = load_image_paths_and_labels(images_folder, df)

# Encode the labels
label_encoders = [LabelEncoder() for _ in range(labels.shape[1])]
for i in range(labels.shape[1]):
    label_encoders[i].fit(labels[:, i])

# Predict the categories for a given image
def predict_image(image_path):
    image = preprocess_image(image_path)
    predictions = model.predict(image)
    decoded_predictions = []
    for i, prediction in enumerate(predictions):
        # Decode prediction for each label using the corresponding encoder
        decoded_label = label_encoders[i].inverse_transform([np.argmax(prediction)])
        decoded_predictions.append(decoded_label[0])
    return decoded_predictions, predictions
