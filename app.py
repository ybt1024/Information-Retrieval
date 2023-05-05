'''
Code for the Flask App

Contributor: Ziming Xu
'''
from typing import List
from utils import load_resume, load_csv
from gpt import GPT
from gpt_ranking import Rerank
import os
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request
from search import BM25_standard_analyzer_search, BM25_english_analyzer_search, search_by_ids

app = Flask(__name__)
PER_PAGE = 8
gptAPI = GPT()
app.config['UPLOAD_FOLDER'] = "./corpus_data"
query = ""
pdf = None

# home page
@app.route("/")
def home():
    return render_template("home.html")


# result page
@app.route("/results", methods=["POST"])
def results():
    global query; global pdf
    '''
    Result page that returns searched documents and GPT comment
    '''
    # TODO:
    query = request.form["query"]
    pdf = request.files["file"]
    answer = None
    most_frequent_skills = None
    if pdf:
        filename = secure_filename(pdf.filename)
        pdf.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        resume = load_resume(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        prompt = "What are the most suitable jobs based on this resume: " + resume
        answer = gptAPI.getResponse(prompt) + " You can enter these into the search bar to find possible listings."
    if query:
        most_frequent_skills = required_skills_process(gptAPI.getResponse("Identify skills that are most frequently required by employers for " + query))
    matched_docs = BM25_standard_analyzer_search(query)
    return render_template('results.html',
                           page_id=0,
                           is_last=True,
                           docs=matched_docs,
                           query=query,
                           answer = answer,
                           most_frequent_skills = most_frequent_skills
                           )

# result page for reranked results - based on cosine similarity
@app.route("/reranked_results", methods=["POST"])
def reranked_results():
    global query; global pdf
    '''
    Result page that returns searched documents and GPT comment
    '''
    # TODO:
    answer = None
    reranked_matches = []
    if pdf:
        filename = secure_filename(pdf.filename)
        resume = load_resume(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        answer = "These are the reranked results of your original query. They are ranked in order of which postings match your resume best."
        matched_docs = BM25_standard_analyzer_search(query)
        gpt_reranking = Rerank("./corpus_data/query_results.csv", resume)
        reranked_ind = gpt_reranking.indices_of_nearest_neighbors[1:]
        list_docs = []
        for hit in matched_docs:
            list_docs.append(hit)
        for ind in reranked_ind:
            reranked_matches.append(list_docs[ind])
    else:
        answer = "You must have submitted a resume to have AI rerank your results. " 
        answer += "Upload your resume and retype your query, then reclick the search button and the AI Rerank button after to have it rerank the results of your query. "
        answer += "You must upload your resume everytime you enter a new search if you want to use the AI Reranking feature."
        reranked_matches = []
    return render_template('results.html',
                           page_id=0,
                           is_last=True,
                           docs=reranked_matches,
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


def required_skills_process(skills: str) -> str:
    index = skills.index("1")
    return skills[index:]


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
