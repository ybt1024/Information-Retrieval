from typing import List

from elasticsearch_dsl import Search
from elasticsearch_dsl.query import Match, MatchAll, ScriptScore, Ids, Query
from elasticsearch_dsl.connections import connections
from embedding_service.client import EmbeddingClient
from example_query import generate_script_score_query

import csv

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
    return search("job_posting", q_basic, 8)


def search(index: str, query: Query, k: int) -> List:
    s = Search(using="default", index=index).query(query)[:k]
    s = s.extra(explain=True)
    response = s.execute()
    results_to_csv(response)
    return response


def search_by_ids(index: str, doc_ids: List, k: int) -> List:
    q_match_ids = Ids(values=doc_ids)
    s = Search(using="default", index=index).query(q_match_ids)[:k]
    s = s.extra(explain=True)
    response = s.execute()
    return response


def format_explanation(explanation):
    description = explanation['description']
    value = explanation['value']
    formatted = f"{description} (score: {value:.2f})"

    if 'details' in explanation:
        details = explanation['details']
        formatted_details = [format_explanation(detail) for detail in details]
        formatted += "\n  " + "\n  ".join(formatted_details)
   
    return formatted


def results_to_csv(results):
    with open("./corpus_data/query_results.csv", 'w', newline=None) as file:
        writer = csv.writer(file)
        fields = [f for f in results[0]]
        fields.insert(0, 'doc_id')
        writer.writerow(fields)
        for num, doc in enumerate(results):
            hit_str = str(doc)
            id_start = hit_str.index('/')+1
            id_stop = hit_str.index(')')
            doc_id = hit_str[id_start:id_stop]
            doc_dict = doc.to_dict()
            data = [doc_id]
            for key in doc_dict:
                val = doc_dict[key].replace('\n', '')
                data.append(val)
            writer.writerow(data)
    

