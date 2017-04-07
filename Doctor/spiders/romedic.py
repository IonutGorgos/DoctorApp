# -*- coding: utf-8 -*-
import scrapy


class RomedicSpider(scrapy.Spider):
    name = "romedic"
    allowed_domains = ["romedic.com"]
    start_urls = ['http://romedic.com/']

    def parse(self, response):
        pass
