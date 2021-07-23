import scrapy
from urllib.parse import urljoin

data = []

class SeekSpider(scrapy.Spider):
    name = "data_scientist"
    allowed_domains = ["seek.com.au"]
    start_urls = ['https://www.seek.com.au/data-scientist-jobs']
    
    def parse(self, response):
        urls = response.xpath('//a[@class="_2S5REPk"]/@href').extract()
        
        print("\n********************")
        for url in urls:
            
            #next_url = response.urljoin(url)

            next_url = urljoin('https://www.seek.com.au', url)

            print(next_url)
            yield scrapy.Request(url = next_url, callback =self.parse_details)

        print("\n********************")

        #next_page = response.xpath('//*[@class="fa fa-chevron-rightdd"]/../@href').extract_first()

        #if next_page is not None:
        #    next_page = response.urljoin(next_page)
        #    yield scrapy.Request(next_page, callback = self.parse)

    def parse_details(self, response):
        try:
            row['job_title'] = response.xpath('//div[@class="FYwKg _6Gmbl_4"]/h1/text()').extract()
        except:
            row['job_title'] = None
        try:
            row['company'] = None
        except:
            row['company'] = None
        try:
            locale = response.xpath('//div[@class="FYwKg PrHFr _1EtT-_4"]/text()').extract()
            row['location_1'] = locale[0]
            row['location_2'] = locale[1]
            row['sector_1'] = locale[2]
            row['sector_2'] = locale[3]
        except:
            row['location_1'] = None
            row['location_2'] = None
            row['sector_1'] = None
            row['sector_2'] = None
        try:
            row['f_p_time'] = locale[-1]
        except:
            row['f_p_time'] = None
        try:
            row['salary'] = locale[-2]
        except:
            row['salary'] = None
        try:
            row['desc'] = None
        except:
            row['desc'] = None

        print(row)
        data.append(row)

        yield
