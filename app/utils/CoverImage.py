import os
import base64   
from datetime import datetime

def ConverBase64ToImage(base64Image):
    if base64Image: 
        return f"data:image/png;base64,{base64.b64encode(base64Image).decode('utf-8')}"
    else:
        return None

def DecodeBase64(base64Image):
    if base64Image: 
        avatar = base64Image.split(",")[1]
        avatar = base64.b64decode(avatar)
        return avatar
    else:
        return None

def ConverBase64ToPath(base64_image):
    image_storage_path = 'C:/food'

    if base64_image:
        image_data = base64.b64decode(base64_image)
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        image_path = os.path.join(image_storage_path, f"{timestamp}.png")
        with open(image_path, 'wb') as image_file:
            image_file.write(image_data)
        return image_path.replace("\\", "/")
def ConverImageToBase64(image_path):
    if image_path:
        with open(image_path, "rb") as image_file:
            # Read the binary data of the image
            image_binary = image_file.read()

            # Encode the binary data as Base64
            image_base64 = base64.b64encode(image_binary).decode('utf-8')

        return f"data:image/png;base64,{image_base64}"