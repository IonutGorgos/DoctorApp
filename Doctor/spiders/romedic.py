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
            link_doctor = short.xpath('.//b/a/@href').extract_first()
            if link_doctor is not None:
                yield Request(response.urljoin(link_doctor), callback=self.parse_info)
            next_page_url = response.xpath('//div[@class="paginatie"]/a[@class="pag_sel"]/@href').extract_first()
            if next_page_url is not None:
                yield Request(response.urljoin(next_page_url), callback=self.parse_paginatie)

    def parse_paginatie(self, response):
        shortdes = response.xpath('//div[@class="shortdes"]')
        for short in shortdes:
            link_doctor = short.xpath('.//b/a/@href').extract_first()
            if link_doctor is not None:
                yield Request(response.urljoin(link_doctor), callback=self.parse_info)
            next_page_url = response.xpath('//div[@class="paginatie"]/a[@class="pag_sel"]/@href').extract_first()
            if next_page_url is not None:
                yield Request(response.urljoin(next_page_url), callback=self.parse_paginatie)

    def parse_info(self, response):
        div = response.xpath('//div[@class="articol_text"]/div[@class="box_1"]')
        loc_munca = response.xpath('//div[@class="articol_text"]/div[@class="box_1"]/a').extract_first()
        if loc_munca is not None:
            loc = response.xpath('//div[@class="articol_text"]/div[@class="box_1"]/a/text()').extract_first()
        else:
            loc = response.xpath(
                '//div[@class="articol_text"]/div[@class="box_1"]/span[@class="style6"]/following-sibling::text()').extract_first()
        specialitate = response.xpath('//div[@class="articol_text"]/div[@class="box_1"]/br/following-sibling::span[1]/following-sibling::text()').extract_first()
        nume_doctor = response.xpath('//div[@class="articol_text"]/h1/text()').extract_first()
        for contact in div:
            yield {
                'nume': nume_doctor,
                'contact': contact.xpath('.//div[@class="t"]/text()').extract_first(),
                'loc_munca': loc,
                'specialitate': specialitate,
            }












