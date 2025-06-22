import asyncio
import pandas as pd
import httpx

from config import settings
from llm.analyzer import ArticleAnalyzer
from llm.processor import ArticleProcessor


async def main():
    df = pd.read_csv('data/processed/scraped_data.csv')

    async with httpx.AsyncClient() as client:
        analyzer = ArticleAnalyzer(client, api_key=settings.API_KEY)
        processor = ArticleProcessor(df, analyzer)
        enriched_data = await processor.process_all()

    output_df = pd.DataFrame(enriched_data)
    output_csv = 'data/processed/analysis_summary.csv'
    output_df.to_csv(output_csv, index=False)
    print(f'✅ Enriched data saved to {output_csv}')


if __name__ == '__main__':
    asyncio.run(main())
