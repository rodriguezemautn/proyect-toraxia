import tensorflow as tf
import numpy as np
from PIL import Image
import io

def load_model():
    # Cargar el modelo pre-entrenado (esto es un placeholder, deberías usar tu propio modelo)
    return tf.keras.applications.MobileNetV2(weights='imagenet', include_top=False)

model = load_model()

def preprocess_image(image):
    img = Image.open(io.BytesIO(image.read()))
    img = img.resize((224, 224))
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)
    return tf.keras.applications.mobilenet_v2.preprocess_input(img_array)

def validate_image(image):
    try:
        processed_image = preprocess_image(image)
        predictions = model.predict(processed_image)
        
        # Esta es una lógica simplificada. Deberías ajustarla según tu modelo específico
        is_valid = np.max(predictions) > 0.5
        message = "La imagen es una radiografía válida." if is_valid else "La imagen no parece ser una radiografía válida."
        
        return is_valid, message
    except Exception as e:
        return False, f"Error al procesar la imagen: {str(e)}"
