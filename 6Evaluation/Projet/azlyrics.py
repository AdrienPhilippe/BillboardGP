import scrapy


class AzlyricsSpider(scrapy.Spider):
    name = 'azlyrics'
    allowed_domains = ['https://search.azlyrics.com/search.php?']
    start_urls = ['http://https://search.azlyrics.com/search.php?/']

    def parse(self, response):
        pass
