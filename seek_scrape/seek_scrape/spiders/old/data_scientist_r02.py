'''
DSI14 - Project 4
Scrapy spider to scrap DATA SCIENTIST roles from Seek
'''

import scrapy
from urllib.parse import urljoin

class SeekSpider(scrapy.Spider):
    name = "data_scientist_r02"             #Spider name
    allowed_domains = ["seek.com.au"]       # ??

    # seed with the Seek landing site for DATA SCIENTIST jobs - NB will need to mod if looking for dif roles
    start_urls = ['https://www.seek.com.au/data-scientist-jobs']
    
    def parse(self, response):
        
        #grab list of all job ad links from search page
        urls = response.xpath('//a[@class="_2S5REPk"]/@href').extract()
        
        #loop through list of links and visit each to grab the details
        for url in urls:
            # join the partial url with the domain to ensure correct operation
            next_url = urljoin('https://www.seek.com.au', url)
            yield scrapy.Request(url = next_url, callback =self.parse_details)

        # grab the link for the next page
        next_page = response.xpath('//a[@data-automation="page-next"]/@href').extract()[0]

        # if 'next page' link present, go to and rinse and repeat
        if next_page is not None:
            # join next page link with Domain to ensure correct operation
            next_page = urljoin('https://www.seek.com.au', next_page)
            yield scrapy.Request(url = next_page, callback = self.parse)

    def parse_details(self, response):
        # grab and assign the job title
        job_title = response.xpath('//div[@class="FYwKg _6Gmbl_4"]/h1/text()').extract()[0]
        # grab and assign the company name
        company = response.xpath('//span[@data-automation="advertiser-name"]//text()').extract()[0]
        # grab the breakdown of location and job sector info plus salary stuff
        breakdown = response.xpath('//div[@class="FYwKg PrHFr _1EtT-_4"]/text()').extract()
        # assign the major/minor location info to vars
        location_1, location_2 = breakdown[0], breakdown[1]
        # assign the job sector info
        sector_1, sector_2 = breakdown[2], breakdown[3]
        # assign the FT/PT info - always last item in the 'breakdown' list
        f_p_time = breakdown[-1]
        # assign the salary info, IF present -- chk presence by length of list
        if len(breakdown) == 6:
            salary = breakdown[-2]
        else:
            salary = None
        # assign all job description data in raw scrapped format -- will clean later
        desc = response.xpath('//div[@data-automation="jobAdDetails"]//text()').extract()

        # output the data to a dict for json capture
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
