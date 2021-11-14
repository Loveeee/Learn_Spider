import scrapy
import time

class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']

    def parse(self, response):
        pass

    #重写Spider的默认执行函数,每次都会提前执行
    def start_requests(self):
        print("JHI")

        from selenium.webdriver.chrome.options import Options
        from selenium import webdriver
        chrome_option = Options()
        chrome_option.add_argument('--disable-extensions')
        chrome_option.add_experimental_option('debuggerAddress','127.0.0.1:9221')

        browser = webdriver.Chrome(chrome_options=chrome_option)
        browser.get('https://www.zhihu.com/signin')

        time.sleep(60)
