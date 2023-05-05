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
    # line below added by Kirsten
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

'''
Contributor: Kirsten

Saves results of every search query to a csv file for use in AI reranking.
'''
def results_to_csv(results):
    # opens/creates a file that it saves it to - file is always the same so it's always overwritten with every query if it's already an existing file
    with open("./corpus_data/query_results.csv", 'w', newline=None) as file:
        writer = csv.writer(file)
        # the fields of the document: doc_id, job_post, date, title, company_name, about_company, job_description, job_requirements, required_Qual
        fields = [f for f in results[0]]
        fields.insert(0, 'doc_id')
        writer.writerow(fields)
        for doc in results:
            # converts to string to get doc_id
            hit_str = str(doc)
            # doc_id is located after the first '\' character in the converted string
            id_start = hit_str.index('/')+1
            # doc_id ends before the first ')' character in the converted string
            id_stop = hit_str.index(')')
            # creates a substring of the doc_id to add into the csv file - in case it should be needed
            doc_id = hit_str[id_start:id_stop]
            # converts the doc to a dict for easier data accessing
            doc_dict = doc.to_dict()
            # inserts doc_id as the first piece of data 
            data = [doc_id]
            # gets the rest of the doc data from the results and adds it to the same list
            for key in doc_dict:
                # removes newline characters for accurate data parsing 
                val = doc_dict[key].replace('\n', '')
                # adds it to the data 
                data.append(val)
            # writes the full data from the job posting to the csv file
            writer.writerow(data)
    

