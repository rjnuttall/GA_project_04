'''
DSI14 - Project 4
Scrapy spider to scrap DATA SCIENTIST roles from Seek -- v03
'''

import scrapy
from urllib.parse import urljoin

class SeekSpider(scrapy.Spider):
    name = "data_scientist"             #Spider name
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
        breakdown = response.xpath('//div[@class="FYwKg _3VxpE_4"]//text()').extract()
        # assign the major/minor location info to vars
        location_1, location_2 = breakdown[0], breakdown[1]
        # assign the job sector info
        sector_1, sector_2 = breakdown[-2], breakdown[-1]
        
        # grab the detail work type and salary info
        job_details = response.xpath('//div[@data-automation="job-detail-work-type"]//text()').extract()
        if len(job_details) == 2:
            salary = job_details[0]         #.replace('$','')
            work_type = job_details[1]
        elif job_details[0] in ['Full Time', 'Part Time', 'Casual/Vacation', 'Contract/Temp']:
            salary = None
            work_type = job_details[0]
        else:
            salary = job_details[0]
            work_type = None
        # assign all job description data in raw scrapped format -- will clean later
        desc = response.xpath('//div[@data-automation="jobAdDetails"]//text()').extract()

        # output the data to a dict for json capture
        yield {
            'search': 'Data Scientist',
            'job_title': job_title,
            'company': company,
            'location_1': location_1,
            'location_2': location_2,
            'sector_1': sector_1,
            'sector_2': sector_2,
            'work_type': work_type,
            'salary': salary,
            'desc': desc,
            'url': response.request.url
            }
