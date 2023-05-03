from typing import List

from flask import Flask, render_template, request
from search import BM25_standard_analyzer_search, BM25_english_analyzer_search, search_by_ids

app = Flask(__name__)
PER_PAGE = 8

# home page
@app.route("/")
def home():
    return render_template("home.html")


# result page
@app.route("/results", methods=["POST"])
def results():
    # TODO:
    query = request.form["query"]

    # matched_doc_meta_ids = []
    matched_docs = BM25_standard_analyzer_search(query)
    print(matched_docs)
    # sliced_id = matched_doc_meta_ids[:min(len(matched_doc_meta_ids), PER_PAGE)]
    # matched_docs = search_by_ids("nf_docs", sliced_id, 10)
    # is_last = len(matched_doc_meta_ids) <= PER_PAGE

    return render_template('results.html',
                           page_id=0,
                           is_last=True,
                           docs=matched_docs,
                           query=query,
                           )


# "next page" to show more results
@app.route("/results/<int:page_id>", methods=["POST"])
def next_page(page_id):
    # TODO:
    query = request.form["query"]
    search_option = request.form["search_option"]
    doc_ids = request.form["matched_doc_ids"]
    print(doc_ids)
    matched_doc_ids = string_to_int_list(doc_ids)
    sliced_id = slice(matched_doc_ids, page_id, PER_PAGE)
    matched_docs = search_by_ids("nf_docs", sliced_id, 10)
    is_last = len(matched_doc_ids) <= (page_id + 1) * PER_PAGE
    return render_template('results.html',
                           page_id=page_id,
                           is_last=is_last,
                           docs=matched_docs,
                           query=query,
                           matched_doc_ids=matched_doc_ids,
                           search_option=search_option
                           )


def string_to_int_list(s: str) -> List[int]:
    s = s[1:-1]
    return [int(num.replace("'", "")) for num in s.split(',')]


def slice(list: List, page_id: int, per_page: int) -> List:
    return list[page_id * PER_PAGE: min(len(list), (page_id + 1) * PER_PAGE)]


# document page
@app.route("/doc_data/<int:doc_id>")
def doc_data(doc_id):
    # TODO:
    document = search_by_ids("nf_docs", [doc_id], 10)[0]
    return render_template("doc.html", document=document)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
