"""
Contributor: Kirsten 

- openai embeddings 
- we use chatgpt/openai to rerank the results of the original query to show best resume matches
- takes the results of the original query and the user's/the uploaded resume to rerank the results based on cosine similarity
- adapted from https://github.com/openai/openai-cookbook/blob/main/examples/Recommendation_using_embeddings.ipynb
"""

# imports
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

    ''' 
    Initializes the reranker parameters. Model/Engine used is set to the 2nd version of what openAI has (currently the most recent).
    @param result_path (str): path to saved csv file of original text box query
    @param resume (str): string of data read from a pdf of a resume

    '''
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
        # calls on method that collects the necessary/important information for embedding generation
        self.get_resume_result_strings()

    '''
    Gets data from the provided results and resume. Fills the list of strings to be passed into the other functions for embedding generation.
    Uses the job posting, title, job description, job requirements, and required qualifications as important data from the results.
    Uses all information on the resume. Takes note of where in the list the resume data is added.
    '''
    def get_resume_result_strings(self):
        # data accessed through the pandas dataframe
        self.to_embedding_strings = [str(jPos) + ', ' + str(t) + ', ' + str(jDes) + ', ' + str(jReq) + ', ' + str(jQual) 
                  for (jPos, t, jDes, jReq, jQual) in 
                  zip(self.results_df.get('job_post'), self.results_df.get('title'), 
                      self.results_df.get('job_description'), self.results_df.get('job_requirements'), self.results_df.get('required_Qual'))]
        # adding user's resume to the end of the list
        self.to_embedding_strings.append(self.resume_data)
        # index of resume in the list
        self.resume_ind = len(self.to_embedding_strings) - 1
        # calls on method that implements the reranking of the results
        self.recommendations_from_strings()

    '''
    Determines which job listings from the results are best suited for the resume submitted. Many of the functions are already built into the 
    openAI interface.
    '''
    def recommendations_from_strings(self) -> List[int]:
        """Return nearest neighbors of a given string."""
        # gets embeddings for all of the strings - job posting query results and resume (get_embedding() function from embeddings_utils.py)
        self.embedding_list = [get_embedding(string, engine=self.model) for string in self.to_embedding_strings ]
        # gets the embedding of the source string through the index that was previously stored/noted
        self.resume_embedding = self.embedding_list[self.resume_ind]
        # get distances between the resume's embedding and the embeddings of the job posting results through cosine similarity (distances_from_embeddings() function from embeddings_utils.py)
        distances = distances_from_embeddings(self.resume_embedding, self.embedding_list, distance_metric="cosine")
        # get indices of nearest neighbors (indices_of_nearest_neighbors_from_distances() function from embeddings_utils.py)
        self.indices_of_nearest_neighbors = indices_of_nearest_neighbors_from_distances(distances)


