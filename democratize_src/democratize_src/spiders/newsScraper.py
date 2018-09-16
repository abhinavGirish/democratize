import scrapy
from scrapy.linkextractors import LinkExtractor

class NewsSpider(scrapy.Spider):
    name = 'newsspider'
    start_urls = ['https://blog.scrapinghub.com','https://www.vox.com/',
    'https://fivethirtyeight.com/','https://slate.com/','https://www1.nyc.gov/',
    'https://www.post-gazette.com/','https://www.nytimes.com/']

    def parse(self, response):
        #headlines on fivethirtyeight
        for title in response.css("div.hentry"):
            yield {'title': title.css('a ::text').extract_first()}
            next_page = title.css('h3 a::attr(href)').extract_first()
            if next_page is not None:
                next_page = response.urljoin(next_page)
                yield scrapy.Request(next_page, callback=self.parseArticle)

        #headlines on slate.com
        for title in response.css("div.story-teaser__teaser"):
            yield {'title': title.css('h3 ::text').extract_first()}

        #for handling nyc govt
        for title in response.css("h2.hero-title"):
            yield {'title': title.css('a ::text').extract_first()}

        #for handling pittsburgh post-gazette headlines
        for title in response.css("div.pgevoke-textpack-item-text"):
            yield {'title': title.css('span ::text').extract_first()}

        #new york times
        for title in response.css("div.css-6p6lnl"):
            yield {'title': title.css('h2 ::text').extract_first()}

    #parsing the text of the article
    def parseArticle(self, response):
        for section in response.css("div.entry-content.single-post-content"):
            yield {'article_content': section.css('p ::text').extract_first()}
        #yield {'message':"Just entered an article in fivethirtyeight!"}

