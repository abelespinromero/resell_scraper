import requests
import os
import pandas as pd

class ImageDownloader:
    def __init__(self, save_dir):
        self.save_dir = save_dir

    def download_images(self, df):
        image_filepaths = []

        for index, row in df.iterrows():
            image_url = row['image_url']
            item_id = str(index)  # Puedes usar el índice como ID único para nombrar las imágenes
            self.download_image(image_url, item_id, image_filepaths)

        df["image_filepath"] = image_filepaths
        df.to_csv("image_downloader/vinted_p2.csv")
    def download_image(self, url, item_id, image_filepaths):

        try:
            response = requests.get(url)
            if response.status_code == 200:
                file_name = f"{item_id}.jpeg"
                # Guarda la imagen en el directorio especificado
                file_path = os.path.join(self.save_dir, file_name)
                with open(file_path, 'wb') as f:
                    f.write(response.content)
                image_filepaths.append(file_path)
                print(f"Imagen descargada y guardada como {file_name}")
            else:
                image_filepaths.append(None)
                print(f"Error al descargar la imagen {url}")
        except Exception as e:
            image_filepaths.append(None)
            print(f"Error al descargar la imagen {url}: {str(e)}")

        

# Ejemplo de uso
if __name__ == "__main__":
    
    df = pd.read_csv("resell_spider/data/vinted.csv")
    df = df.head(3)

    # Directorio donde se guardarán las imágenes descargadas
    save_directory = 'image_downloader/product_images'

    # Crea el directorio si no existe
    os.makedirs(save_directory, exist_ok=True)

    # Crea una instancia de ImageDownloader
    image_downloader = ImageDownloader(save_directory)

    # Descarga las imágenes del DataFrame
    image_downloader.download_images(df)
