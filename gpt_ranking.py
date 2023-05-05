"""
openai embeddings 
- we use chatgpt/openai to rerank the results of the original query to show best resume matches
adapted from https://github.com/openai/openai-cookbook/blob/main/examples/Recommendation_using_embeddings.ipynb
"""

# imports
# import List
from typing import List
import openai
import os
import pandas as pd
import pickle
from utils import load_resume
from openai.embeddings_utils import (
    get_embedding,
    distances_from_embeddings,
    tsne_components_from_embeddings,
    chart_from_components,
    indices_of_nearest_neighbors_from_distances,
)

class Rerank():

    def __init__(self, result_path, resume) -> None:
        self.model = "text-embedding-ada-002"
        self.results_df = pd.read_csv(result_path)
        self.results_df
        self.resume_data = resume
        self.to_embedding_strings = []
        self.resume_ind = None
        self.embedding_list = []
        self.resume_embedding = None
        self.indices_of_nearest_neighbors = None
        self.get_resume_result_strings()

    def get_resume_result_strings(self):
        # list of strings to be passed into functions
        # using the job posting, title, job description, job requirements, and required qualifications as important data
        self.to_embedding_strings = [str(jPos) + ', ' + str(t) + ', ' + str(jDes) + ', ' + str(jReq) + ', ' + str(jQual) 
                  for (jPos, t, jDes, jReq, jQual) in 
                  zip(self.results_df.get('job_post'), self.results_df.get('title'), 
                      self.results_df.get('job_description'), self.results_df.get('job_requirements'), self.results_df.get('required_Qual'))]
        # adding user's resume to the end of the list
        self.to_embedding_strings.append(self.resume_data)
        # index of resume in the list
        self.resume_ind = len(self.to_embedding_strings) - 1
        self.recommendations_from_strings()

    def recommendations_from_strings(self, ) -> List[int]:
        """Return nearest neighbors of a given string."""
        # get embeddings for all strings (function from embeddings_utils.py)
        self.embedding_list = [get_embedding(string, engine=self.model) for string in self.to_embedding_strings ]
        # get the embedding of the source string
        self.resume_embedding = self.embedding_list[self.resume_ind]
        # get distances between the source embedding and other embeddings (function from embeddings_utils.py)
        distances = distances_from_embeddings(self.resume_embedding, self.embedding_list, distance_metric="cosine")
        # get indices of nearest neighbors (function from embeddings_utils.py)
        self.indices_of_nearest_neighbors = indices_of_nearest_neighbors_from_distances(distances)
        # return self.indices_of_nearest_neighbors


