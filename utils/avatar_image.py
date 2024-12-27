from PIL import Image
import requests
from io import BytesIO
import os

def load_avatar(image_source):
    """
    Carrega uma imagem de avatar a partir de um caminho local ou URL.

    :param image_source: String contendo o caminho local ou URL da imagem
    :return: Objeto PIL.Image ou None se a imagem não puder ser carregada
    """
    try:
        if image_source.startswith(("http://", "https://")):
            # Se for uma URL
            response = requests.get(image_source)
            img = Image.open(BytesIO(response.content))
        else:
            # Se for um caminho local
            if os.path.exists(image_source):
                img = Image.open(image_source)
            else:
                raise FileNotFoundError(
                    f"Arquivo não encontrado: {image_source}")

        # Redimensiona a imagem para um tamanho padrão (opcional)
        img = img.resize((128, 128))
        return img
    except Exception as e:
        print(f"Não foi possível carregar a imagem do avatar: {e}")
        return None
