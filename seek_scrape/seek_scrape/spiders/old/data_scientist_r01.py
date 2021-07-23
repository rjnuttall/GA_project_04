import scrapy
from urllib.parse import urljoin

#data = []

class SeekSpider(scrapy.Spider):
    name = "data_scientist_r01"
    allowed_domains = ["seek.com.au"]
    start_urls = ['https://www.seek.com.au/data-scientist-jobs']
    
    def parse(self, response):
        urls = response.xpath('//a[@class="_2S5REPk"]/@href').extract()
        
        for url in urls:
            
            next_url = urljoin('https://www.seek.com.au', url)

            yield scrapy.Request(url = next_url, callback =self.parse_details)

        next_page = response.xpath('//a[@data-automation="page-next"]/@href').extract()[0]
        #print('***********\n\n', next_page,  '\n\n**********')
        if next_page is not None:
            next_page = urljoin('https://www.seek.com.au', next_page)

            #print('***********\n\n', next_page,  '\n\n**********')
            print("\n\n\nHERE\n\n\n")

            yield scrapy.Request(url = next_page, callback = self.parse)



    def parse_details(self, response):
        try:
            job_title = response.xpath('//div[@class="FYwKg _6Gmbl_4"]/h1/text()').extract()
        except:
            job_title = None
        try:
            company = response.xpath('//span[@data-automation="advertiser-name"]//text()').extract()
        except:
            company = None
        try:
            locale = response.xpath('//div[@class="FYwKg PrHFr _1EtT-_4"]/text()').extract()
            location_1 = locale[0]
            location_2 = locale[1]
            sector_1 = locale[2]
            sector_2 = locale[3]
            f_p_time = locale[-1]
            if len(locale) == 6:
                salary = locale[-2]
            else:
                salary = None
        except:
            location_1 = None
            location_2 = None
            sector_1 = None
            sector_2 = None
            f_p_time = None

        try:
            desc = response.xpath('//div[@data-automation="jobAdDetails"]//text()').extract()
        except:
            desc = None

        yield {
            'job_title': job_title,
            'company': company,
            'location_1': location_1,
            'location_2': location_2,
            'sector_1': sector_1,
            'sector_2': sector_2,
            'f_p_time': f_p_time,
            'salary': salary,
            'desc': desc,
            'url': response.request.url
            }
