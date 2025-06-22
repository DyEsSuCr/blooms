import asyncio
import pandas as pd


class ArticleProcessor:
    def __init__(self, df: pd.DataFrame, analyzer, concurrency: int = 5):
        self.df = df
        self.analyzer = analyzer
        self.semaphore = asyncio.Semaphore(concurrency)

    async def process_row(self, row) -> dict:
        async with self.semaphore:
            title = row['title']
            url = row['url']
            category = row['categories']
            content = row['page_content']

            if pd.isna(content) or not content.strip():
                summary, topics = 'No content', []
            else:
                response = await self.analyzer.analyze(content)
                summary, topics = self.analyzer.parse_response(response)

            return {
                'Title': title,
                'URL': url,
                'Category': category,
                'Summary': summary,
                'Topics': topics,
                # 'Topics': ', '.join(topics),
            }

    async def process_all(self) -> list:
        tasks = [self.process_row(row) for _, row in self.df.iterrows()]
        return await asyncio.gather(*tasks)
