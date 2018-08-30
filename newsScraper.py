import scrapy

class BlogSpider(scrapy.Spider):
    name = 'blogspider'
    start_urls = ['https://blog.scrapinghub.com','https://www.vox.com/',
    'https://fivethirtyeight.com/','https://slate.com/','https://www1.nyc.gov/',
    'https://www.post-gazette.com/']

    def parse(self, response):
        #headlines on fivethirtyeight
        for title in response.css("div.hentry"):
            yield {'title': title.css('a ::text').extract_first()}

        #headlines on slate.com
        for title in response.css("div.story-teaser__teaser"):
            yield {'title': title.css('h3 ::text').extract_first()}

        #for handling nyc govt
        for title in response.css("h2.hero-title"):
            yield {'title': title.css('a ::text').extract_first()}

        #for handling pittsburgh post-gazette headlines
        for title in response.css("div.pgevoke-textpack-item-text"):
            yield {'title': title.css('span ::text').extract_first()}
