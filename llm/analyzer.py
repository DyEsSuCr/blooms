import re
import httpx

API_URL = 'https://api.deepseek.com/v1/chat/completions'


class ArticleAnalyzer:
    def __init__(self, client: httpx.AsyncClient, api_key: str):
        self.api_key = api_key
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
        }
        self.client = client

    def build_prompt(self, article_text: str) -> list:
        system_msg = 'You are an AI assistant designed to help extract key insights from a text. You must follow the exact output format specified by the user.'
        user_prompt = f"""
        Please analyze the following article text and provide:
        1. A clear and concise one-sentence summary that captures the main point
        2. 3 to 5 topics or keywords that best represent the central themes

        IMPORTANT: Return your response in exactly this format:
        SUMMARY: [your one-sentence summary here]
        TOPICS: topic1, topic2, topic3, topic4, topic5

        Article text:
        {article_text}
        """
        return [
            {'role': 'system', 'content': system_msg},
            {'role': 'user', 'content': user_prompt},
        ]

    async def analyze(self, article_text: str) -> str | None:
        payload = {
            'model': 'deepseek-chat',
            'messages': self.build_prompt(article_text),
            'stream': False,
        }

        try:
            response = await self.client.post(
                API_URL, headers=self.headers, json=payload, timeout=60
            )
            response.raise_for_status()
            return response.json()['choices'][0]['message']['content'].strip()
        except Exception as e:
            print(f'API error: {e}')
            return None

    @staticmethod
    def parse_response(text: str) -> tuple[str, list]:
        if not text:
            return 'No summary available.', []

        summary_match = re.search(r'SUMMARY:\s*(.+)', text)
        topics_match = re.search(r'TOPICS:\s*(.+)', text)

        summary = summary_match.group(1).strip() if summary_match else 'No summary available.'
        topics_str = topics_match.group(1).strip() if topics_match else ''
        topics = [t.strip() for t in topics_str.split(',') if t.strip()]
        return summary, topics
