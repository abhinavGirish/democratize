import scrapy

class BlogSpider(scrapy.Spider):
    name = 'blogspider'
    start_urls = ['https://blog.scrapinghub.com','https://www.vox.com/','https://fivethirtyeight.com/']

    def parse(self, response):
        for title in response.css("div.hentry"):
            yield {'title': title.css('a ::text').extract_first()}

            
