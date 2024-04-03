from abc import ABC, abstractmethod
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import TruncatedSVD, PCA
import numpy as np

import bulk_injest
from elasticsearch.helpers import streaming_bulk
import pandas as pd

class Indexer(ABC):
    """
    Class that organizes indexed data to be retrival-ready, it must
    1. organize data into retrievable format using create_indexes
    2. search organized data for relevant documents and return indexes of those documents to the Retriever
    """

    @abstractmethod
    def create_indexes(self, data):
        """
        creates indexes out of ENCODED data
        """
        pass

    @abstractmethod
    def search_indexes(self, query):
        """
        searches indexes for an ENCODED query
        """
        pass

class SimpleIndexer(Indexer):
    def __init__(self):
        self.data_ = None

    def create_indexes(self, data: np.ndarray):
        self.data_ = data
    
    def search_indexes(self, query: np.ndarray):
        data_similarities = cosine_similarity(self.data_, query)
        data_sim_pairs = [(data_idx, sim) for data_idx, sim in enumerate(data_similarities)]
        return sorted(data_sim_pairs, reverse = True, key = lambda x: x[1])
    
class LeaderIndexer(Indexer):
    def __init__(self, n_clusters = 5, use_pca = False, min_explained_var = 0.95):
        self.n_clusters = n_clusters
        self.use_pca = use_pca
        self.min_explained_var = min_explained_var
        self.cluster_centers_ = None
        self.clusters_ = None
        self.data_ = None
        self.dim_reducer_ = None

    def create_indexes(self, data: np.ndarray):
        if self.use_pca:
            if not isinstance(data, np.ndarray):
                data = np.array(data)
            self.dim_reducer_ = self._fit_dim_reducer(data, self.min_explained_var)
            data = self.dim_reducer_.transform(data)

        kmeans = KMeans(n_clusters=self.n_clusters, n_init='auto')
        clusters = kmeans.fit_predict(data)
        self.cluster_centers_ = kmeans.cluster_centers_
        self.clusters_ = clusters
        self.data_ = data


    def search_indexes(self, query: np.ndarray):
        if self.use_pca:
            if not isinstance(query, np.ndarray):
                query = np.array(query)
            query = self.dim_reducer_.transform(query)

        ## find index of cluster center most similar to query
        leader_idx = np.argmax(cosine_similarity(self.cluster_centers_, query))
        cluster_indices = np.where(self.clusters_ == leader_idx)
        cluster_data = self.data_[cluster_indices]
        
        ## get similarities between cluster members and query
        cluster_member_similarities = cosine_similarity(cluster_data, query)
        cluster_sim_pairs = [(data_idx, sim) for data_idx, sim in enumerate(cluster_member_similarities)]
        # sorted_results = cluster_member_similarities.flatten().argsort()[::-1]
        return sorted(cluster_sim_pairs, reverse = True, key = lambda x: x[1])
    
    def _fit_dim_reducer(self, data, min_explained_var):
        return PCA(n_components = min_explained_var).fit(data)
    

class ElasticSearchIndexer(Indexer):
    def __init__(self, client):
        self.client = client
        self.index_name = None

    def create_indexes(self, data_path, index_name):
        # Creation can be done easily with ElasticSearch Kibana
        print("Creating index:", index_name)
        bulk_injest.create_index(self.client, index_name)

        df = pd.read_csv(data_path)
        number_of_docs = len(df)

        print("Indexing documents...")
        successes = 0
        for ok, action in streaming_bulk(
            client=self.client, index=index_name, actions=bulk_injest.generate_actions(data_path),
        ):
            successes += ok
        
        if successes != number_of_docs:
            raise ValueError("Failed to index all documents")
        self.index_name = index_name

    def search_indexes(self, queries:dict, pagination: tuple = (0, 10), operator = "must"):
        '''
        operator: variable that determines the type of boolean query to be used, can be
        "must" or "should", which correspond to AND and OR operators respectively
        '''

        query_list = []
        for field, query in queries.items():
            if field == "Review Date":
                dates = query.split("|")
                query_list.append({"range": {field: {"gte": dates[0], "lte": dates[1]}}})
            else:
                query_list.append({"match": {field: query}})

        response = self.client.search(
                index=self.index_name,
                from_=pagination[0],
                size=pagination[1],
                query={
                    "bool" : {
                        operator : query_list
                    }
                }
            )
        return response