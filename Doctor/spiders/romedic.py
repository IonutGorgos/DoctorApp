# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
import re


class RomedicSpider(scrapy.Spider):
    name = "romedic"
    allowed_domains = ["romedic.com"]
    start_urls = ['http://www.romedic.ro/medici.php']

    def parse(self, response):
        specializari = response.xpath('//ul[@class="col2v1"]')
        for specializare in specializari:
            spec = str(specializare.xpath('.//li/a/text()').extract())
            # spec = re.sub(r'\s{3,}|[\r\n\t]', ' ', spec)
            link = specializare.xpath('//li/a/@href').extract()
            if link is not None:
                yield Request(response.urljoin(link))
            yield {
                'Specializare': spec,
                'Link': link,
            }
