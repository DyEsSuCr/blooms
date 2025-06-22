import scrapy
import json
import re
from ..items import ArticleItem


class ArticlesSpider(scrapy.Spider):
    name = 'articles'
    allowed_domains = ['www.freshproduce.com']

    def start_requests(self):
        with open('data/raw/freshproduce.json', 'r') as file:
            data = json.load(file)

        for entry in data:
            url = f'{entry["url"]}'
            if 'pdf-viewer?contentId=' not in url:
                yield scrapy.Request(url, callback=self.parse, meta={'entry': entry})

    def parse(self, response):
        page_content = response.css('main#pageContent ::text').getall()
        page_content = ' '.join(page_content).strip()
        page_content = re.sub(r'\s+', ' ', page_content)

        entry = response.meta['entry']

        item = ArticleItem()

        item['url'] = response.url
        item['title'] = entry['title']
        item['descripcion'] = entry['descripcion']
        item['categories'] = entry['categories']
        item['page_content'] = page_content

        yield item
