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
            specializare2 = specializare.xpath('.//li/a/text()').extract()
            for spec in specializare2:
                spec = re.sub(r'\s{2,}|[\n\t]', '', spec)
                yield {
                    'Specializare': spec,
                }
            link = specializare.xpath('.//li/a/@href').extract()
            for l in link:
                if l is not None:
                    yield Request(response.urljoin(l))


