# -*- coding: UTF-8 -*-
import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        urls = [
	        'http://zhuixinfan.com/main.php'
             # 'http://zhuixinfan.com/main.php?mod=viewresource&sid=9981'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        base_url = 'http://zhuixinfan.com/{0}'
        for quote in response.css('table.top-list-data'):
             if quote.css('caption::text').extract_first().encode('utf-8').find("今日") > -1:
                if len(quote.css('td.td2').xpath('.//a[2]/@href').extract()) >0:
                    for nt in quote.css('td.td2').xpath('.//a[2]/@href').extract():
                        yield scrapy.Request(base_url.format(nt), dont_filter=True, callback=self.parse_page)

    def parse_page(self,response):
		yield{
           'bt': response.xpath('//dd[@class="a1"]/text()').extract()[1],
           'title' : response.xpath('//h2[@class="it"]/span/text()').extract_first()
        }
