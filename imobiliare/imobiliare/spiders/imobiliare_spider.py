import time
from pprint import pprint

import scrapy
from csv import writer


class QuotesSpider(scrapy.Spider):
    name = "im_spider"
    file_name = f"{time.time()}_output.csv"

    start_urls = [
        'https://www.imobiliare.ro/vanzare-apartamente/bucuresti?pagina=1/',
    ]


    def parse(self, response):
        fail_count = 0
        with open('imobiliare/reports/{file_name}_imobiliare.csv'.format(file_name=self.file_name), 'a',
                  encoding='utf-8', newline='') as f:
            thewriter = writer(f)
            header = ["Title", "Location", "Rooms", "Square meters", "Floor", "Setup", "Price [K]", "Currency & VAT"]
            thewriter.writerow(header)

            for quote in response.css('div.col_descriere'):
                try:
                    title = quote.css('h2.titlu-anunt span::text')[1].extract()
                    location = quote.css('p.location_txt span::text').get()
                    rooms = quote.css('div.caracteristica span span strong::text')[0].extract()
                    square_meters = quote.css('div.caracteristica span span strong::text')[1].get()
                    floor = quote.css('div.caracteristica span span strong::text')[2].extract()
                    setup = quote.css('div.caracteristica span span strong::text')[3].extract()
                    price = quote.css('span.pret-mare::text').get()
                    price_extension = quote.css('span.tva-luna::text').get()

                    title = title.strip()
                    location = location.strip()

                    if "TVA" in price_extension:
                        price_extension = "E + TVA"
                    else:
                        price_extension = "E"

                    if "o" in rooms:
                        rooms = "1"

                    fetched_data = [title, location, rooms, square_meters, floor, setup, price, price_extension]
                    pprint(fetched_data)
                    thewriter.writerow(fetched_data)
                except:
                    fail_count += 1
                    print("+ 1 fail..")

        print("Number of fails: ", fail_count)
