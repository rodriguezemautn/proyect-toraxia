from PIL import Image
import numpy as np
import io
from django.core.files.base import ContentFile
from datetime import datetime

def anonymize_image(image):
    # Convertir la imagen a un array de numpy
    img = Image.open(image)
    img_array = np.array(img)

    # Implementar aquí la lógica de anonimización
    # Por ejemplo, podemos borrar una región específica de la imagen
    height, width = img_array.shape[:2]
    img_array[0:height//10, 0:width] = 0  # Borra la parte superior de la imagen

    # Convertir de vuelta a una imagen PIL
    anonymized_img = Image.fromarray(img_array)

    # Convertir la imagen PIL a un archivo que Django pueda guardar
    buffer = io.BytesIO()
    anonymized_img.save(buffer, format='PNG')
    return ContentFile(buffer.getvalue(), name=f'anonymized_{datetime.now().timestamp()}.png')

def send_to_central_server(anonymized_image):
    # Implementar aquí la lógica para enviar la imagen al servidor central
    # Por ahora, simplemente simularemos que se ha enviado
    return True
