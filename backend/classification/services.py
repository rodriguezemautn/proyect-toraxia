import tensorflow as tf
import numpy as np
from PIL import Image
import io

def load_model():
    # Cargar el modelo DenseNet pre-entrenado (esto es un placeholder, deberías usar tu propio modelo)
    return tf.keras.applications.DenseNet121(weights='imagenet', include_top=True)

model = load_model()

def preprocess_image(image):
    img = Image.open(io.BytesIO(image.read()))
    img = img.resize((224, 224))
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)
    return tf.keras.applications.densenet.preprocess_input(img_array)

def classify_image(image):
    try:
        processed_image = preprocess_image(image)
        predictions = model.predict(processed_image)
        
        # Obtener las 5 principales predicciones
        top_5 = tf.keras.applications.densenet.decode_predictions(predictions, top=5)[0]
        
        classification_result = [
            {'label': label, 'probability': float(prob)} 
            for (_, label, prob) in top_5
        ]
        
        confidence_score = float(np.max(predictions))
        
        return classification_result, confidence_score
    except Exception as e:
        return [], 0.0
