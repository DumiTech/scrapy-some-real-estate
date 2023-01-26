from pprint import pprint
from scrapy.exporters import CsvItemExporter

import scrapy


class QuotesSpider(scrapy.Spider):
    name = "im_spider"

    start_urls = [
        'https://www.imobiliare.ro/vanzare-apartamente/bucuresti?pagina=1/',
    ]

    # define the fields that will be exported to the CSV file
    fields_to_export = ['title', 'type', 'location', 'rooms', 'square_meters', 'floor', 'setup', 'price', 'price_extension']

    def __init__(self):
        self.csvfile = open("output.csv", 'w')
        self.exporter = CsvItemExporter(self.csvfile, fields_to_export=self.fields_to_export)
        self.exporter.start_exporting()

    def parse(self, response):
        fail_count = 0
        for quote in response.css('div.col_descriere'):
            try:
                item = {
                    'title': quote.css('h2.titlu-anunt span::text')[1].getall(),
                    'type': quote.css('h2.titlu-anunt span::text')[0].getall(),
                    'location': quote.css('p.location_txt span::text').get(),
                    'rooms': quote.css('div.caracteristica span span strong::text')[0].getall(),
                    'square_meters': quote.css('div.caracteristica span span strong::text')[1].getall(),
                    'floor': quote.css('div.caracteristica span span strong::text')[2].getall(),
                    'setup': quote.css('div.caracteristica span span strong::text')[3].getall(),
                    'price': quote.css('span.pret-mare::text').getall(),
                    'price_extension': quote.css('span.tva-luna::text').getall(),
                }
                item['location'] = item['location'].strip()
                pprint(item)
                self.exporter.export_item(item)
            except:
                fail_count += 1
                print("+ 1 fail..")

        print("Number of fails: ", fail_count)

    def closed(self, reason):
        self.exporter.finish_exporting()
        self.csvfile.close()
