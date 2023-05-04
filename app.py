'''
Code for the Flask App

Contributor: Ziming Xu
'''
from typing import List
from utils import load_resume
from gpt import GPT
import os
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request
from search import BM25_standard_analyzer_search, BM25_english_analyzer_search, search_by_ids

app = Flask(__name__)
PER_PAGE = 8
gptAPI = GPT()
app.config['UPLOAD_FOLDER'] = "./corpus_data"


# home page
@app.route("/")
def home():
    return render_template("home.html")


# result page
@app.route("/results", methods=["POST"])
def results():
    '''
    Result page that returns searched documents and GPT comment
    '''
    # TODO:
    query = request.form["query"]
    pdf = request.files["file"]
    filename = secure_filename(pdf.filename)
    pdf.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    resume = load_resume(os.path.join(app.config["UPLOAD_FOLDER"], filename))
    prompt = "What are the most suitable jobs based on this resume: " + resume
    answer = gptAPI.getResponse(prompt)
    matched_docs = BM25_standard_analyzer_search(query)
    return render_template('results.html',
                           page_id=0,
                           is_last=True,
                           docs=matched_docs,
                           query=query,
                           answer = answer,
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
    '''
    Document page that returns matched doc
    '''
    # TODO:
    document = search_by_ids("job_posting", [doc_id], 8)[0]
    return render_template("doc.html", document=document)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
