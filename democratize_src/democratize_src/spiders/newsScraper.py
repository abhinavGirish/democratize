import scrapy
from scrapy.linkextractors import LinkExtractor

class NewsSpider(scrapy.Spider):
    name = 'newsspider'
    start_urls = ['https://blog.scrapinghub.com','https://www.vox.com/',
    'https://fivethirtyeight.com/','https://slate.com/','https://www1.nyc.gov/',
    'https://www.post-gazette.com/','https://www.nytimes.com/','https://www.theguardian.com/us']

    def parse(self, response):
        #headlines on fivethirtyeight
        for title in response.css("div.hentry"):
            yield {'title': title.css('a ::text').extract_first()}
            next_page = title.css('h3 a::attr(href)').extract_first()
            if next_page is not None:
                next_page = response.urljoin(next_page)
                yield scrapy.Request(next_page, callback=self.parseArticleFiveThirtyEight)

        #headlines on slate.com
        for title in response.css("section.story-teaser"):
            yield {'title': title.css('h3 ::text').extract_first()}
            next_page = title.css('section a::attr(href)').extract_first()
            if next_page is not None:
                next_page = response.urljoin(next_page)
                yield scrapy.Request(next_page, callback=self.parseArticleSlate)

        #for handling nyc govt
        for title in response.css("h2.hero-title"):
            yield {'title': title.css('a ::text').extract_first()}
            next_page = title.css('h2 a::attr(href)').extract_first()
            if next_page is not None:
                next_page = response.urljoin(next_page)
                yield scrapy.Request(next_page, callback=self.parseArticleNYCGov)

        #for handling pittsburgh post-gazette headlines
        for title in response.css("div.pgevoke-textpack-item-text"):
            yield {'title': title.css('span ::text').extract_first()}
            '''next_page = title.css('section a::attr(href)').extract_first()
            if next_page is not None:
                next_page = response.urljoin(next_page)
                yield scrapy.Request(next_page, callback=self.parseArticlePPG)'''

        #new york times
        for title in response.css("div.css-6p6lnl"):
            yield {'title': title.css('h2 ::text').extract_first()}

        #theguardian
        for title in response.css("div.fc-item__content"):
            yield {'title': title.css('span.js-headline-text ::text').extract_first()}
            next_page = title.css('h2.fc-item__title a::attr(href)').extract_first()
            #yield {'next_page_guardian': next_page}
            if next_page is not None:
                next_page = response.urljoin(next_page)
                yield scrapy.Request(next_page, callback=self.parseArticleGuardian)

    #parsing fiveThirtyEight
    def parseArticleFiveThirtyEight(self, response):
        for section in response.css("div.entry-content.single-post-content"):
            yield {'article_content_fivethirtyeight': section.css('p ::text').extract_first()}
        #yield {'message':"Just entered an article in fivethirtyeight!"}

    def parseArticleSlate(self, response):
        for section in response.css("div.article__content"):
            yield {'article_content_slate': section.css('p ::text').extract_first()}
        #yield {'message':"Just entered an article in SLATE!"}

    def parseArticleNYCGov(self, response):
        for div in response.css("div.richtext"):
            yield {'article_content_NYCGov': div.css('p ::text').extract_first()}
        #yield {'message':"Just entered an article in SLATE!"}

    def parseArticlePPG(self,response):
        yield {'message':"Just entered an article in PPG"}

    def parseArticleGuardian(self,response):
        for div in response.css("div.uit-container"):
            yield {'article_content_guardian': div.css('p ::text').extract_first()}



