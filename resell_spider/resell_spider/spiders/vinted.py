import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import urllib.parse
import csv
import json
import re


class VintedSpider(scrapy.Spider):
    name = 'vinted'
    start_urls = ['https://www.vinted.es']
 
    def __init__(self, *args, **kwargs):
        super(VintedSpider, self).__init__(*args, **kwargs)
        self.csv_file = open('vinted.csv', 'w', newline='', encoding='utf-8')
        self.csv_writer = csv.writer(self.csv_file)
        self.csv_writer.writerow(['keyword', 'title', 'price', 'image_url', 'item_url'])  # Encabezados
        self.page = 1  # Inicializa la página en 1
        self.continue_crawling = True  # Variable para controlar si continuar o no


    def start_requests(self):
        keywords = ["reloj maserati"]  # Agrega más palabras clave aquí

        for keyword in keywords:
            url = f'https://www.vinted.es/catalog?search_text={urllib.parse.quote_plus(keyword)}'
            yield scrapy.Request(url, self.parse, meta={'keyword': keyword})

    def get_next_page_url(self, keyword):
        # Construye la URL con el número de página actual
        return f'https://www.vinted.es/catalog?search_text={urllib.parse.quote_plus(keyword)}&page={self.page}'

    def parse(self, response):
        keyword = response.meta.get('keyword')  # Obtén el keyword de la meta información

        if response.status == 404:
            self.continua_crawling = False
            return
        
        # Convertir la cadena JSON de productos en un diccionario
        response_text = response.text

        match = re.search(r',\s*"byId"', response_text)

        if match:
            start_index = match.start() + 1  # Obtener el índice de inicio
            end_index = response_text.find(':"search"}}', start_index) + len(':"search"}}')

            if end_index > start_index:
                # Extraer la subcadena que contiene "byId"
                json_text = response_text[start_index:end_index]

                # Agregar "{}" al final para que sea un JSON válido
                json_text = "{" + json_text + "}"

                # Parsear la subcadena como JSON
                data = json.loads(json_text)
        
        # Extraer información de los elementos
        for item_id, item_data in data["byId"].items():
            title = item_data["title"]
            price = item_data["price"]["amount"]
            image_url = item_data["photo"]["url"]
            item_url = item_data["url"]

            row = [keyword, title, price, image_url, item_url]

            
            self.csv_writer.writerow(row)


        # Incrementa el número de página para la siguiente iteración
        self.page += 1

        # Obtén la URL de la siguiente página
        next_page_url = self.get_next_page_url(keyword)

        # Haz una solicitud a la siguiente página si existe
        if next_page_url:
            yield scrapy.Request(next_page_url, self.parse, meta={'keyword': keyword})



        def close_spider(self, spider):
            self.csv_file.close()




if __name__ == '__main__':
    process = CrawlerProcess(get_project_settings())
    process.crawl(VintedSpider)  # Reemplaza esto con el nombre de tu araña
    process.start()
