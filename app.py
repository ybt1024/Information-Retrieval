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
    matched_docs = BM25_standard_analyzer_search(query)
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
    return


def string_to_int_list(s: str) -> List[int]:
    s = s[1:-1]
    return [int(num.replace("'", "")) for num in s.split(',')]


def slice(list: List, page_id: int, per_page: int) -> List:
    return list[page_id * PER_PAGE: min(len(list), (page_id + 1) * PER_PAGE)]


# document page
@app.route("/doc_data/<int:doc_id>")
def doc_data(doc_id):
    # TODO:
    document = search_by_ids("job_posting", [doc_id], 8)[0]
    return render_template("doc.html", document=document)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
