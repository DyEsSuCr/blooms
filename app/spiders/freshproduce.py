import scrapy
import json
from urllib.parse import urlencode
from ..items import ArticleItem


class FreshproduceSpider(scrapy.Spider):
    name = 'freshproduce'
    allowed_domains = ['www.freshproduce.com']

    def __init__(self, categories='', page_size=100, content_type='', sort_by=2, *args, **kwargs):
        super(FreshproduceSpider, self).__init__(*args, **kwargs)
        self.categories = categories
        self.page_size = page_size
        self.content_type = content_type
        self.sort_by = sort_by
        self.base_url = 'https://www.freshproduce.com/api/search/query'

    def start_requests(self):
        params = {
            'staticCategories': self.categories,
            'pageSize': self.page_size,
            'sortBy': self.sort_by,
            'filteredCategories': self.content_type,
            'pageNumber': 0,
        }
        start_url = f'{self.base_url}?{urlencode(params)}'
        yield scrapy.Request(start_url, callback=self.parse)

    def parse(self, response):
        data = json.loads(response.text)

        for result in data['results']:
            item = ArticleItem()
            item['url'] = f'https://{self.allowed_domains[0]}{result["url"]}'
            item['title'] = result['tileTitle']
            item['descripcion'] = result['tileDescription']
            item['categories'] = result['categories']

            yield item

        paging_info = data.get('pagingSpecification', {})
        current_page = paging_info.get('pageNumber', 0)
        total_pages = paging_info.get('totalNumberOfPages', 0)

        if current_page < total_pages - 1:
            next_page = current_page + 1

            params = {
                'staticCategories': self.categories,
                'pageSize': self.page_size,
                'filteredCategories': self.content_type,
                'sortBy': self.sort_by,
                'pageNumber': next_page,
            }

            next_url = f'{self.base_url}?{urlencode(params)}'
            yield scrapy.Request(next_url, callback=self.parse)
