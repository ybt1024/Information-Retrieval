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
        content={"query": query_text}
    )
    return search("nf_docs", q_basic, 10)


def BM25_english_analyzer_search(query_text: str) -> List:
    q_basic = Match(
        stemmed_content={"query": query_text}
    )
    return search("nf_docs", q_basic, 10)


def BERT_embeddings_search(query_text: str) -> List:
    query_vector = encoder.encode([query_text]).tolist()[0]
    q_vector = generate_script_score_query(query_vector, "sbert_embedding")
    return search("nf_docs", q_vector, 10)


def reranking_BM25_english_anlyzer_using_BERT_search(query_text: str) -> List:
    q_basic = Match(
        stemmed_content={"query": query_text}
    )
    query_vector = encoder.encode([query_text]).tolist()[0]
    q_vector = generate_script_score_query(query_vector, "sbert_embedding")
    return rescore_search("nf_docs", q_basic, q_vector)


def search(index: str, query: Query, k: int) -> List:
    s = Search(using="default", index=index).query(query)[:k]
    response = s.execute()
    doc_ids = []
    for hit in response:
        doc_ids.append([hit.doc_id, hit.meta.id])
    return doc_ids


def search_by_ids(index: str, doc_ids: List, k: int) -> List:
    q_match_ids = Ids(values=doc_ids)
    s = Search(using="default", index=index).query(q_match_ids)[:k]
    response = s.execute()
    return response


def rescore_search(index: str, query: Query, rescore_query: Query) -> List:
    """
    using rescore filter from ES
    :param index:
    :param query:
    :param rescore_query:
    :return:
    """
    s = Search(using="default", index=index).query(query)[:100]
    s = s.extra(
        rescore={
            "window_size": 100,
            "query": {
                "rescore_query": rescore_query,
                "query_weight": 0,
                "rescore_query_weight": 1,
            },
        }
    )  # only weight on the query for rescoring
    response = s.execute()
    doc_ids = []
    for hit in response[:10]:
        doc_ids.append([hit.doc_id, hit.meta.id])
    return doc_ids