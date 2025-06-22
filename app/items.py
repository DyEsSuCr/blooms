import scrapy


class ArticleItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    descripcion = scrapy.Field()
    categories = scrapy.Field()
    page_content = scrapy.Field()
