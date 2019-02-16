# -*- coding: UTF-8 -*-
import scrapy
import sys
from urllib import unquote
reload(sys)
sys.setdefaultencoding('utf8')


class QuotesSpider(scrapy.Spider):
    name = "dm"

    def start_requests(self):
        cookies = {
            '__cfduid':'dd1a4eddeae140aef1f7ae1330bfab0181550292492',
            'Hm_lvt_34ddf5508b3473910e07042977d3f7f8':'1550291433',
            'Hm_lpvt_34ddf5508b3473910e07042977d3f7f8':'1550292495',
            'user_script_url':'%2F%2Fcdn.acgscript.com%2Fscript%2Fmiobt%2F4.js%3F3',
            'user_script_rev':'20181120.2'
        }
        urls = [
	        'http://www.comicat.org/'
             # 'http://zhuixinfan.com/main.php?mod=viewresource&sid=9981'
        ]
        for url in urls:
            yield scrapy.Request(url=url,cookies=cookies,callback=self.parse)

    def parse(self, response):
        base_url = 'http://www.comicat.org/{0}'
        for quote in  response.xpath('.//tr'):
            if str(quote.css('a::text').extract_first()).encode('utf-8').find("今天") > -1:
                for nt in quote.xpath('.//td[2]/a/@href').extract():
                    yield scrapy.Request(base_url.format(nt), dont_filter=True,callback=self.parse_page)



    def parse_page(self,response):
        base_url = 'http://www.comicat.org/{0}'
        #for inn in response.xpath('.//tr[1]/td[3]/a/@href').extract():
        for bt in response.xpath('.//tr[1]/td[3]'):
            yield{
                "bt": "magnet:?xt=urn:btih:"+bt.xpath('.//a/@href').extract()[0].encode('utf-8').replace('show-','').replace('.html','')+'&tr=http://open.acgtracker.com:1096/announce',
                "title": unquote(response.url.replace('http://www.comicat.org/search.php?keyword=',''))
            }
            #print str(bt.xpath('.//a/@href').extract()[0]).resplace('show-','').resplace('.html','')
            #print bt.xpath('.//a/text()').extract(),bt.xpath('.//a/@href').extract()
            #yield scrapy.Request(base_url.format(inn), dont_filter=True,cookies=cookies, callback=self.parse_bt)
		#yield{
        #   'bt': response.xpath('//dd[@class="a1"]/text()').extract()[1],
        #   'title' : response.xpath('//h2[@class="it"]/span/text()').extract_first()
        #}
        
         
