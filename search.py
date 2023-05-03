from typing import List

from elasticsearch_dsl import Search
from elasticsearch_dsl.query import Match, MatchAll, ScriptScore, Ids, Query
from elasticsearch_dsl.connections import connections
from embedding_service.client import EmbeddingClient
from example_query import generate_script_score_query

encoder = EmbeddingClient(host="localhost", embedding_type="sbert")
connections.create_connection(hosts=["localhost"], timeout=100, alias="default")


def BM25_standard_analyzer_search(query_text: str) -> List:
    q_basic = Match(
        job_post={"query": query_text}
    )
    return search("job_posting", q_basic, 8)


def BM25_english_analyzer_search(query_text: str) -> List:
    q_basic = Match(
        job_post={"query": query_text}
    )
    return search("nf_docs", q_basic, 8)


def search(index: str, query: Query, k: int) -> List:
    s = Search(using="default", index=index).query(query)[:k]
    response = s.execute()
    return response


def search_by_ids(index: str, doc_ids: List, k: int) -> List:
    q_match_ids = Ids(values=doc_ids)
    s = Search(using="default", index=index).query(q_match_ids)[:k]
    response = s.execute()
    return response