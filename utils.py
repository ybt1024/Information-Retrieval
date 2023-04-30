from pathlib import Path
from typing import Dict, Union, Generator
import os
import json
import functools
import time
import numpy as np
import pandas as pd
import csv

def timer(func):
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_t = time.perf_counter()
        f_value = func(*args, **kwargs)
        elapsed_t = time.perf_counter() - start_t
        mins = elapsed_t // 60
        print(
            f"'{func.__name__}' elapsed time: {mins} minutes, {elapsed_t - mins * 60:0.2f} seconds"
        )
        return f_value

    return wrapper_timer


def load_qrels(nf_split_file: Union[str, os.PathLike]) -> Dict[str, Dict]:
    # load the query relevance test file as a nested dictionary
    qrels_df = pd.read_csv(nf_split_file, sep="\t", header=0)
    docs_rels_dict = dict()

    for i, group in enumerate(qrels_df.groupby("corpus-id")):
        doc_id = group[0]
        doc_rels_dict = dict()
        group_df = group[1][["query-id", "score"]]
        for _, row in group_df.iterrows():
            doc_rels_dict[row["query-id"]] = row["score"]
        docs_rels_dict[doc_id] = doc_rels_dict
    return docs_rels_dict


def load_nf_docs(nf_folder_path: Union[str, os.PathLike]) -> Generator[Dict, None, None]:
    # prepare and load the nf documents for ES indexing
    nf_folder_path = Path(nf_folder_path)
    nf_docs_path = nf_folder_path.joinpath("corpus.jsonl")
    nf_split_path = nf_folder_path.joinpath("test.tsv")
    nf_docs_embeds_path = nf_folder_path.joinpath("nf_docs_sb_mp_net_embedddings.npy")

    docs_rels_dict = load_qrels(nf_split_path)
    nf_docs_embeddings = np.load(str(nf_docs_embeds_path))
    with open(nf_docs_path, "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            doc_dict = json.loads(line)
            doc_dict["annotation"] = docs_rels_dict.get(doc_dict["_id"], dict())
            doc_dict["sbert_embedding"] = nf_docs_embeddings[i].tolist()
            yield doc_dict


def load_csv(doc_path: Union[str, os.PathLike]) -> Generator[Dict, None, None]:
    with open(doc_path, 'r') as file:
        reader = csv.DictReader(file)
        next(reader)
        for row in reader:
            # Yield a dictionary containing only the desired columns
            yield {
                'jobpost': row['jobpost'],
                'date': row['date'],
                'Title': row['Title'],
                'Company': row['Company'],
                'aboutC': row['aboutC'],   # about company
                'JobDescription': row['JobDescription'],
                'JobRequirment': row['JobRequirment'],
                'RequiredQual': row['RequiredQual'],
            }

if __name__ == "__main__":

    pass



