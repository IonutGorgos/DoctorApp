# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from scrapy.spiders import Spider
import re


class DocPlannerSpider(Spider):
    name = "docplanner"
    allowed_domains = ["docplanner.ro"]
    start_urls = ['https://www.docplanner.ro']

    def parse(self, response):
        # //*[@id="popular-queries-short"]/div/ul/li[1]/a
        specializari = response.xpath('//div[@id="popular-queries-short"]/div/ul')
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
        # [@id="search-content"]/div[1]/div/div/ul/li[1]/div/div/div/div[2]/h2/a
        shortdes = response.xpath('//div[@id="search-content"]/div[1]/div/div/ul')
        for short in shortdes:
            link_doctor = short.xpath('.//li/div/div/div/div[2]/h2/a/@href').extract_first()
            if link_doctor is not None:
                yield Request(response.urljoin(link_doctor), callback=self.parse_info)
            next_page_url = response.xpath('//div[@id="search-content"]/div[3]/ul/li[@class="next"]/a').extract_first()
            if next_page_url is not None:
                yield Request(response.urljoin(next_page_url), callback=self.parse_paginatie)

    def parse_paginatie(self, response):
        shortdes = response.xpath('//div[@id="search-content"]/div[1]/div/div/ul')
        for short in shortdes:
            link_doctor = short.xpath('.//li/div/div/div/div[2]/h2/a/@href').extract_first()
            print link_doctor
            if link_doctor is not None:
                yield Request(response.urljoin(link_doctor), callback=self.parse_info)
            next_page_url = response.xpath('//div[@id="search-content"]/div[3]/ul/li[@class="next"]/a').extract_first()
            if next_page_url is not None:
                print "request new page"
                yield Request(response.urljoin(next_page_url), callback=self.parse_paginatie)

    def parse_info(self, response):
        loc_munca = response.xpath('//*[@id="profile-addresses-list"]/li[1]/div[1]/div[2]/div/div/div[1]/h2/a/span/text()').extract_first()
        specialitate = response.xpath('//*[@id="profile-header"]/div/div/div[2]/div/div[1]/h2/a/text()').extract_first()
        nume_doctor = response.xpath('//*[@id="profile-header"]/div/div/div[2]/div/div[1]/h1/text()').extract_first()
        yield {
            'nume': nume_doctor,
            'contact': response.xpath('//*[@id="profile-addresses-list"]/li/div[1]/div[2]/div/div/div[1]/div/p[1]/text()').extract_first(),
            'loc_munca': loc_munca,
            'specialitate': specialitate,
        }



















