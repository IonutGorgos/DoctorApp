# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from scrapy.spiders import Spider
import re


class RomedicSpider(Spider):
    name = "romedic"
    allowed_domains = ["romedic.ro"]
    start_urls = ['http://www.romedic.ro/medici/']

    def parse(self, response):
        specializari = response.xpath('//ul[@class="col2v1"]')
        for specializare in specializari:
            specializare2 = specializare.xpath('.//li/a/text()').extract()
            for spec in specializare2:
                spec = re.sub(r'\s{2,}|[\n\t]', '', spec)
                spec = re.sub('\n+', '\n', spec)
            link = specializare.xpath('.//li/a/@href').extract()
            for l in link:
                if l is not None:
                    yield Request(response.urljoin(l), callback=self.parse_items, encoding='utf-8')

    def parse_items(self, response):
        shortdes = response.xpath('//div[@class="shortdes"]')
        for short in shortdes:
            yield {
                'Nume doctor': short.xpath('.//b/a/text()').extract_first(),
            }
            next_page_url = response.xpath('//div[@class="paginatie"]/a[@class="pag_sel"]/@href').extract_first()
            if next_page_url is not None:
                yield Request(response.urljoin(next_page_url), callback=self.parse_paginatie)

    def parse_paginatie(self, response):
        shortdes = response.xpath('//div[@class="shortdes"]')
        for short in shortdes:
            yield {
                'Nume doctor': short.xpath('.//b/a/text()').extract_first(),
            }
            next_page_url = response.xpath('//div[@class="paginatie"]/a[@class="pag_sel"]/@href').extract_first()
            if next_page_url is not None:
                yield Request(response.urljoin(next_page_url), callback=self.parse_paginatie)











