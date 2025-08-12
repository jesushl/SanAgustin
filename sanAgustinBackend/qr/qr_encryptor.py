# qr_utils.py

import json
import qrcode
from cryptography.fernet import Fernet
from PIL import Image
from pyzbar.pyzbar import decode
import os
"""
Requires install libzbar0

"""




# For local test, change this to your own path
from dotenv import load_dotenv
load_dotenv()
######################################3


def get_key_from_env() -> bytes:
    key = os.getenv("QR_SECRET_KEY")
    if not key:
        raise ValueError("QR_SECRET_KEY no está definida en las variables de entorno.")
    return key.encode()

class QREncryptor:
    def __init__(self):
        key = get_key_from_env()
        self.fernet = Fernet(key)

    def generate_qr(self, data: dict, output_file: str = "qr.png"):
        
        json_data = json.dumps(data)
        encrypted_data = self.fernet.encrypt(json_data.encode())

        img = qrcode.make(encrypted_data.decode())
        img.save(output_file)
        return output_file



class QRDecryptor:
    def __init__(self):
        key = get_key_from_env()
        self.fernet = Fernet(key)

    def read_qr_image(self, image_path: str) -> str:
        image = Image.open(image_path)
        decoded_objects = decode(image)

        if not decoded_objects:
            raise ValueError("No se encontró ningún código QR en la imagen")

        return decoded_objects[0].data.decode()

    def decrypt_qr_data(self, encrypted_data: str):
        decrypted_data = self.fernet.decrypt(encrypted_data.encode())
        return json.loads(decrypted_data)

    def read_and_decrypt(self, image_path: str):
        encrypted_data = self.read_qr_image(image_path)
        return self.decrypt_qr_data(encrypted_data)


if __name__ == "__main__":
    encryptor = QREncryptor()
    encryptor.generate_qr("B-204", "Est-27", "qr_b204.png")

    # Leer y desencriptar
    decryptor = QRDecryptor()
    data = decryptor.read_and_decrypt("qr_b204.png")
    print("Contenido desencriptado:", data)