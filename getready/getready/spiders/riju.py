import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        urls = [
	        'http://zhuixinfan.com/main.php'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for quote in response.css('table.top-list-data'):
                yield {
                    'time': quote.css('caption::text').extract_first(),
                    'hot-product': quote.css('td.td2 a.f1::text').extract(),
                    'product': quote.css('td.td2').xpath('.//a[2]//text()').extract(),
	                'link':quote.css('td.td2').xpath('.//a[2]/@href').extract(),
                }
 
