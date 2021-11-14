from urllib import parse

import scrapy
from scrapy import Request


class CnblogsSpider(scrapy.Spider):
    name = 'cnblogs'
    allowed_domains = ['news.cnblogs.com']
    start_urls = ['http://news.cnblogs.com/']

    def parse(self, response):
        '''
        1、首先获取列表，然后交给相应的解析方法
        2、获取下一页的url继续
        :param response:
        :return:
        '''
        # li_1 = response.xpath('//div[@id="news_list"]//h2[@class="news_entry"]/a/@href').extract()
        # li_2 = response.css('div#news_list h2 a::attr(href)').extract()

        # post_nodes = response.css('#new_list .new_block')
        # for post_node in post_nodes:
        #     image_url = post_node.css('.entry_summary a img::attr(href)').extract_first("")
        #     post_url = post_node.css('h2 a::attr(href)').extract_first("")  # post_url是一个相对路径
        #     yield Request(url=parse.urljoin(response.url, post_url), meta={"front_image_url": image_url},
        #                   callback=self.parse_detail)

        # 提取下一页并交给scrapy下载
        # next_url = response.css("div.pager a:last-child::text").extract_first("")
        # if next_url == "Next >":
        #     next_url = response.css("div.pager a:last-child::attr(href)").extract_first("") #如果是next的话则拿next的href值
        #     yield Request(url=parse.urljoin(response.url,next_url),callback=self.parse)

        next_url = response.xpath("//a[contains(text(),'Next >')]/@href").extract_first("")  # xpath和上面的css是一样的,省去了判断
        yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)

    def parse_detail(self, response):
        pass
