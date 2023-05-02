"""
openai embeddings 
- we use chatgpt/openai to rerank the results of the original query to show best resume matches
adapted from https://github.com/openai/openai-cookbook/blob/main/examples/Recommendation_using_embeddings.ipynb
"""

# imports
import List
import openai
import pandas as pd
import pickle
from openai.embeddings_utils import (
    get_embedding,
    distances_from_embeddings,
    tsne_components_from_embeddings,
    chart_from_components,
    indices_of_nearest_neighbors_from_distances,
)

# constants
EMBEDDING_MODEL = "text-embedding-ada-002"

# load data 
# data is considered to be 20 results generated by orig. query and user resume
dataset_path = "corpus_data/original_query_results.csv"
results_df = pd.read_csv(dataset_path)
# client resume as a csv file
resume_path = "resume.csv"
resume_df = pd.read_csv(resume_path)

# list of strings to be passed into functions
# using the job posting, title, job description, and job requirements as important data
to_embedding_strings = [str(jPos) + ', ' + str(t) + ', ' + str(jDes) + ', ' + str(jReq) 
                  for (jPos, t, jDes, jReq) in 
                  zip(results_df.get('jobpost'), results_df.get('title'), 
                      results_df.get('jobDescription'), results_df.get('jobRequirements'))]
# adding objective, experience, and skills from client's resume at final position 
resume_data = [str(o) + ', ' + str(s) + ', ' + str(e) 
               for (o, s, e) in 
               zip(resume_df.get('objective'), 
                   resume_df.get('skills'), resume_df.get('experience'))]
to_embedding_strings.append(resume_data[0])

# index of resume in the list
resume_ind = len(to_embedding_strings) - 1

# print dataframe
# n_examples = 5
# df.head(n_examples)

# print the title, description, and label of each example
# for idx, row in df.head(n_examples).iterrows():
#     print("")
#     print(f"Title: {row['title']}")
#     print(f"Description: {row['description']}")
#     print(f"Label: {row['label']}")

# establish a cache of embeddings to avoid recomputing
# cache is a dict of tuples (text, model) -> embedding, saved as a pickle file

# set path to embedding cache
embedding_cache_path = "data/recommendations_embeddings_cache.pkl"

# load the cache if it exists, and save a copy to disk
try:
    embedding_cache = pd.read_pickle(embedding_cache_path)
except FileNotFoundError:
    embedding_cache = {}
with open(embedding_cache_path, "wb") as embedding_cache_file:
    pickle.dump(embedding_cache, embedding_cache_file)

# define a function to retrieve embeddings from the cache if present, and otherwise request via the API
def embedding_from_string(
    string: str,
    model: str = EMBEDDING_MODEL,
    embedding_cache=embedding_cache
) -> list:
    """Return embedding of given string, using a cache to avoid recomputing."""
    if (string, model) not in embedding_cache.keys():
        embedding_cache[(string, model)] = get_embedding(string, model)
        with open(embedding_cache_path, "wb") as embedding_cache_file:
            pickle.dump(embedding_cache, embedding_cache_file)
    return embedding_cache[(string, model)]


# print the first 10 dimensions of the embedding
# example_embedding = embedding_from_string(example_string)
# print(f"\nExample embedding: {example_embedding[:10]}...")

def recommendations_from_strings(
   strings: List[str],
   index_of_resume_string: int,
   model=EMBEDDING_MODEL,
) -> List[int]:
   """Return nearest neighbors of a given string."""
   # get embeddings for all strings
   embeddings = [embedding_from_string(string, model=model) for string in strings ]
   # get the embedding of the source string
   resume_embedding = embeddings[index_of_resume_string]
   # get distances between the source embedding and other embeddings (function from embeddings_utils.py)
   distances = distances_from_embeddings(resume_embedding, embeddings, distance_metric="cosine")
   # get indices of nearest neighbors (function from embeddings_utils.py)
   indices_of_nearest_neighbors = indices_of_nearest_neighbors_from_distances(distances)
   return indices_of_nearest_neighbors

def print_recommendations_from_strings(
    strings: list[str],
    index_of_resume_string: int,
    k_nearest_neighbors: int = 5,
    model=EMBEDDING_MODEL,
) -> list[int]:
    """Print out the k nearest neighbors of a given string."""
    # get embeddings for all strings
    embeddings = [embedding_from_string(string, model=model) for string in strings]
    # get the embedding of the source string
    query_embedding = embeddings[index_of_resume_string]
    # get distances between the source embedding and other embeddings (function from embeddings_utils.py)
    distances = distances_from_embeddings(query_embedding, embeddings, distance_metric="cosine")
    # get indices of nearest neighbors (function from embeddings_utils.py)
    indices_of_nearest_neighbors = indices_of_nearest_neighbors_from_distances(distances)

    # print out source string
    resume_string = strings[index_of_resume_string]
    print(f"Source string: {resume_string}")
    # print out its k nearest neighbors
    k_counter = 0
    for i in indices_of_nearest_neighbors:
        # skip any strings that are identical matches to the starting string
        if resume_string == strings[i]:
            continue
        # stop after printing out k articles
        if k_counter >= k_nearest_neighbors:
            break
        k_counter += 1

        # print out the similar strings and their distances
        print(
            f"""
        --- Recommendation #{k_counter} (nearest neighbor {k_counter} of {k_nearest_neighbors}) ---
        String: {strings[i]}
        Distance: {distances[i]:0.3f}"""
        )

    return indices_of_nearest_neighbors

print_recommendations_from_strings(to_embedding_strings, resume_ind, EMBEDDING_MODEL)
