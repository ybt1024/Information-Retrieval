# load pretrained sentence BERT encoder. Each embedding has 768 dimensions
python -m embedding_service.server --embedding sbert  --model all-mpnet-base-v2

# load nf docs into the index called "nf_docs"
python load_es_index.py --index_name nf_docs --nf_folder_path pa5_data/nfcorpus-pa5