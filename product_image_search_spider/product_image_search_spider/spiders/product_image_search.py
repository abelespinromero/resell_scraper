import scrapy
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess
from selenium.webdriver.common.by import By
import time

class ProductImageSearchSpider(scrapy.Spider):
    name = 'product_image_search'
    start_urls = ['https://www.google.com/']

    custom_headers = {
        'User-Agent': 'Mi Agente de Usuario Personalizado',
        'Referer': 'https://www.google.com',
        'Accept-Language': 'es-ES,es;q=0.9,en-US;q=0.8,en;q=0.7',
    }

    def __init__(self, *args, **kwargs):
        super(ProductImageSearchSpider, self).__init__(*args, **kwargs)
        self.driver = None

    def start_requests(self):
        chrome_options = Options()
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--window-size=1280,720")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36")
        chrome_options.add_argument("--no-sandbox")
        chrome_driver_path = "chromedriver.exe"
        driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=chrome_driver_path)      


        for url in self.start_urls:
            yield SeleniumRequest(
                url=url,
                wait_time=10,
                screenshot=True,
                dont_filter=True,
                headers=self.custom_headers,
                meta={'driver':driver},
                callback=self.parse
            )

    def accept_cookies(self, response):
        try:
            driver = response.meta['driver']

            driver.get(response.url)

            time.sleep(2)  # Espera 2 segundos antes de hacer scroll

            # Hacer scroll gradualmente hacia abajo para mostrar el banner de cookies
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Aceptar cookies haciendo clic en el botón "Aceptar todo"
            aceptar_todo_button = driver.find_element(By.XPATH, '//button[text()="Aceptar todo"]')
            aceptar_todo_button.click()

        except Exception as e:
            self.logger.error(f"Error al aceptar las cookies: {str(e)}")

    def parse(self, response):
        # Inicializar el navegador
        driver = response.meta['driver']
        driver.get(response.url)

        # 1. Aceptar cookies
        self.accept_cookies(response=response)

        # 2. Seleccionar el icono de "Búsqueda por imágenes"
        imagen_button = driver.find_element_by_css_selector('[title="Buscar por imágenes"]')
        imagen_button.click()

        # 3. Seleccionar una foto de tu equipo
        image_path = 'image_downloader/product_images/0.jpeg'  # Ruta a la foto que deseas buscar
        foto_input = driver.find_element_by_css_selector('[type="file"]')
        foto_input.send_keys(image_path)

        # 4. Hacer clic en "Buscar"
        buscar_button = driver.find_element_by_css_selector('[value="Buscar por imagen"]')
        buscar_button.click()

        # Puedes agregar más código aquí para interactuar con los resultados de búsqueda por imagen

    def closed(self, reason):
        if self.driver:
            self.driver.quit()



# Ejemplo de uso
def main():

    settings = get_project_settings()

    process = CrawlerProcess(settings)

    spider_name = "product_image_search"

    process.crawl(spider_name)

    process.start()

if __name__ == '__main__':
    main()

