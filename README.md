# Information-Retrieval
Final Project for COSI132a - Information Retrieval --- ChatGPT Job Search Engine
created by Ziming Xu, Jiafan He, Kirsten Tapalla, Yunbin Tu

google doc for design:
https://docs.google.com/document/d/1Sbf95iD2irQPIrFikL26B-8QzEZfoAwzdPwyAQI5zJc/edit

Google Slides:
https://docs.google.com/presentation/d/12I_tTYuDChPN_23LzLDvwwOCTjgRwC3dTY1Tcbo0Sk8/edit#slide=id.g23e94a77bfb_0_297


# System Design
This is an application that integrates Chat-GPT to help people find suitable jobs.
We uses elasticsearch to rank the searched jobs from user query.
Users can upload resume and search for jobs ranked by Chat-GPT. Chat-GPT will provide information regarding recommended jobs and required skills etc.
Users can also rerank the searched results based on Chat-GPT's analysis of the resume

Documents:
corpus_data                 - job postings data and sample resumes for testing
embedding_service           - embedding service required documents 
es_service                  - elastic search (7.10.2) service required documents 
templates                   - html webpage templates 
.gitignore                  - gitignore file 
app.py                      - the Flask application python file
example_query.py            - example query adopted from previous assignments for reference
gpt_ranking.py              - GPT reranking module
gpt.py                      - GPT API (gpt-3.5-turbo) connection module
load_es_index.py            - file to load elastic search indices
README.md                   - this file
requirements.txt            - requirements to be installed before running the app
search.py                   - to search for stored indices in the database
utils.py                    - Utility functions to load documents/csv files/resumes


# Setup Instructions 
1. Unzip the project zip file
2. Activate Environment by running conda activate cosi132a
3. Download ES from https://www.elastic.co/downloads/past-releases/elasticsearch-7-10-2. 
And put the downloaded “elasticsearch-7.10.2” into the unziped folder
4. cd to the project folder
5. Run pip install -r requirements.txt
6. Run the following on command line to start ES engine: 
        cd elasticsearch-7.10.2/
        ./bin/elasticsearch
7. On another terminal window, run the following to start embedding service:
        python -m embedding_service.server --embedding sbert  --model all-mpnet-base-v2
8. Load the indices by running:
        python load_es_index.py --index_name job_posting --corpus_folder_path ./corpus_data/data_job_posts.csv
9. Initialize your API key registered from https://platform.openai.com/account/api-keys
10. Store your APIKEY locally (Only need to do once), and GPT will fetch the key from local environment:
    On Mac:
        export APIKEY="......."  # in bash
    On Windows:
        $env:APIKEY="....." # in powershell
11. Run python app.py to use the app! 

Note: you can use the samples resumes in corpus_data folder for testing instead of uploading your own! 


# explain api in elastic search

elastic search returns the total hits, max score, and other basic information.
![1](https://user-images.githubusercontent.com/60807383/236937626-f0a4cf37-55cc-48e7-83c0-38b43af4a09a.png)

for explanation, it gives detailed weight for every token and every part of the formula.

 ![2](https://user-images.githubusercontent.com/60807383/236937635-db51833e-2097-48f9-b202-9d5bb974484c.png)



