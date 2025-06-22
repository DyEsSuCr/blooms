import subprocess


def run_scrapy_spider(command, description):
    print(f'\n>>> Running: {description}')
    try:
        subprocess.run(command, check=True)
        print(f'✅ {description} completed successfully.')
    except subprocess.CalledProcessError:
        print(f'❌ Error while running: {description}')
        exit(1)


# ------------------------------------------
# Available category options for the scraper:
# 'Food Safety'       = Food Safety
# 'Global Trade'      = Global Trade
# 'Technology'        = Technology
#
# Available content types:
# 'Article'           = Article
# 'Event'             = Event
# 'Podcast'           = Podcast
# 'Video'             = Video
# 'Virtual Town Hall' = Virtual Town Hall
# 'Webinar'           = Webinar
# ------------------------------------------

freshproduce_cmd = [
    'scrapy',
    'crawl',
    'freshproduce',
    '-a',
    'categories=Technology|Food Safety|Global Trade',
    '-a',
    'page_size=50',
    '-a',
    'content_type=Article',
    '-a',
    'sort_by=2',
    '-O',
    'data/raw/freshproduce.json',
]

articles_cmd = [
    'scrapy',
    'crawl',
    'articles',
    '-O',
    'data/processed/scraped_data.csv',
]


run_scrapy_spider(freshproduce_cmd, 'Fresh Produce Spider')
run_scrapy_spider(articles_cmd, 'Articles Spider')
