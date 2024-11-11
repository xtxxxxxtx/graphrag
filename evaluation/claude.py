import anthropic
import time
from typing import List, Dict
import asyncio
from datetime import datetime
import json
import os
import argparse
from eval_prompts import *

prompt_dict = {
    "comprehensive": COMPREHENSIVENESS_PROMPT,
    "diversity": DIVERSITY_PROMPT,
    "empowerment": EMPOWERMENT_PROMPT,
    "directness": DIRECTNESS_PROMPT,
}


# Synchronous Version
class ClaudeBatchProcessor:
    def __init__(self, api_key: str, model: str = "claude-3-5-sonnet-20241022"):
        self.client = anthropic.Client(api_key=api_key)
        self.model = model
        self.rate_limit_delay = 1

    def process_single_query(self, query: str, system_prompt: str = None) -> Dict:
        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": query}
                ]
            )

            return {
                "query": query,
                "response": message.content[0].text,
                "timestamp": datetime.now().isoformat(),
                "status": "success"
            }

        except Exception as e:
            return {
                "query": query,
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
                "status": "error"
            }

    def process_batch(self, queries: List[str], system_prompt: str = None) -> List[Dict]:
        results = []
        for query in queries:
            result = self.process_single_query(query, system_prompt)
            results.append(result)
            time.sleep(self.rate_limit_delay)
        return results

    def save_results(self, results: List[Dict], filename: str):
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)


# Example usage of synchronous version
def main_sync(queries, system_prompt):
    # Initialize with your API key
    api_key = os.environ["CLAUDE_API_KEY"]
    processor = ClaudeBatchProcessor(api_key)

    # Process the batch
    results = processor.process_batch(queries, system_prompt)

    # Save results
    processor.save_results(results, "evaluation_result.json")

    # Print results
    for result in results:
        print(f"\nQuery: {result['query']}")
        if result['status'] == 'success':
            print(f"Response: {result['response']}")
        else:
            print(f"Error: {result['error']}")


# Asynchronous Version (using concurrent.futures for parallel processing)
from concurrent.futures import ThreadPoolExecutor


class AsyncClaudeBatchProcessor:
    def __init__(self, api_key: str, model: str = "claude-3-5-sonnet-20241022", max_workers: int = 3):
        self.client = anthropic.Client(api_key=api_key)
        self.model = model
        self.rate_limit_delay = 1
        self.max_workers = max_workers

    def process_single_query(self, query: str, system_prompt: str = None) -> Dict:
        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": query}
                ]
            )
            time.sleep(self.rate_limit_delay)  # Rate limiting

            return {
                "query": query,
                "response": message.content[0].text,
                "timestamp": datetime.now().isoformat(),
                "status": "success"
            }

        except Exception as e:
            return {
                "query": query,
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
                "status": "error"
            }

    def process_batch(self, queries: List[str], system_prompt: str = None) -> List[Dict]:
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = [
                executor.submit(self.process_single_query, query, system_prompt)
                for query in queries
            ]
            results = [future.result() for future in futures]
        return results

    def save_results(self, results: List[Dict], filename: str):
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)


# Example usage of parallel processing version
def main_parallel(queries, system_prompt):
    # Initialize with your API key
    api_key = os.environ["CLAUDE_API_KEY"]
    processor = AsyncClaudeBatchProcessor(api_key, max_workers=3)

    # Process the batch
    results = processor.process_batch(queries, system_prompt)

    # Save results
    processor.save_results(results, "evaluation_result.json")

    # Print results
    for result in results:
        print(f"\nQuery: {result['query']}")
        if result['status'] == 'success':
            print(f"Response: {result['response']}")
        else:
            print(f"Error: {result['error']}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="evaluate graph rag. ",
    )

    parser.add_argument(
        "--direction",
        help="evaluation direction",
        required=False,
        default="comprehensive",
        choices=("comprehensive", "diversity", "empowerment", "directness"),
    )
    parser.add_argument(
        "--question_dir",
        default=None,
        type=str,
    )
    parser.add_argument(
        "--rag_ans_dir",
        default=None,
        type=str,
    )
    parser.add_argument(
        "--llm_ans_dir",
        default=None,
        type=str,
    )

    args = parser.parse_args()
    query_prompt = prompt_dict[args.direction]
    if args.question_dir:
        raise NotImplementedError
    else:
        questions = ["Which public figures are repeatedly mentioned across various entertainment articles?"]

    if args.rag_ans_dir:
        raise NotImplementedError
    else:
        rag_ans = ["""The entertainment industry is vast and diverse, encompassing film, television, music, sports, and
                    digital media. Certain public figures stand out due to their significant contributions and influence
                    across these sectors. The following summary highlights key individuals who are repeatedly
                    mentioned in various entertainment articles, reflecting their impact and presence within the industry.
                    Actors and Directors [...] Public Figures in Controversy [...] Musicians and Executives [...]
                    Athletes and Coaches [...] Influencers and Entrepreneurs [...]
                    The repeated mention of these figures in entertainment articles signifies their ongoing relevance and
                    the public’s interest in their work. Their influence spans across various aspects of entertainment, from
                    shaping cultural narratives in film and television to driving trends in music and digital media. These
                    individuals not only contribute to their respective fields but also influence the broader cultural
                    landscape, often becoming central figures in social discussions and public discourse."""]

    if args.llm_ans_dir:
        raise NotImplementedError
    else:
        llm_ans = ["""Public figures who are repeatedly mentioned across various entertainment articles include Taylor
                Swift, Travis Kelce, Britney Spears, and Justin Timberlake. These individuals have been highlighted
                for various reasons, ranging from their professional achievements to their personal lives.
                Taylor Swift [...] Travis Kelce [...] Britney Spears [...] Justin Timberlake [...]
                These figures are frequently covered due to their high-profile status and the public’s interest in their
                careers and personal lives. Their activities, whether in music, sports, or personal relationships, have
                significant cultural and economic impacts, as evidenced by the media coverage and public reactions."""]

    queries = []
    for q, rag_a, llm_a in zip(questions, rag_ans, llm_ans):
        queries.append(query_prompt.format(QUESTION=q, GRAPH_RAG_ANSWER=rag_a, CHAT_LLM_ANSWER=llm_a))


    system_prompt = """You are a helpful AI assistant. Please provide concise, 
    accurate responses to queries. If you're unsure about something, say so."""

    main_parallel(queries, system_prompt=system_prompt)