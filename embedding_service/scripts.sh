# load pretrained sentence BERT encoder. Each embedding has 768 dimensions
# modify the model name to use different models
python -m embedding_service.server --embedding sbert  --model all-mpnet-base-v2

# load nf docs into the index called "nf_docs"
python load_es_index.py --index_name job_posting --corpus_folder_path ./corpus_data/data_job_posts.csv