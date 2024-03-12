from abc import ABC, abstractmethod
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


class Indexer(ABC):
    """
    Class that organizes indexed data to be retrival-ready, it must
    1. organize data into retrievable format using create_indexes
    2. search organized data for relevant documents and return indexes of those documents to the Retriever
    """

    @abstractmethod
    def create_indexes(self, data):
        pass

    @abstractmethod
    def search_indexes(self, query):
        pass
    
class LeaderIndexer(Indexer):
    def __init__(self, n_clusters=5):
        self.n_clusters = n_clusters
        self.cluster_centers_ = None
        self.clusters_ = None
        self.data_ = None

    def create_indexes(self, data: np.ndarray):
        kmeans = KMeans(n_clusters=self.n_clusters, n_init='auto')
        clusters = kmeans.fit_predict(data)
        self.cluster_centers_ = kmeans.cluster_centers_
        self.clusters_ = clusters
        self.data_ = data


    def search_indexes(self, query: np.ndarray):
        ## find index of cluster center most similar to query
        leader_idx = np.argmax(cosine_similarity(self.cluster_centers_, query))
        cluster_indices = np.where(self.clusters_ == leader_idx)
        cluster_data = self.data_[cluster_indices]
        
        ## get similarities between cluster members and query
        cluster_member_similarities = cosine_similarity(cluster_data, query)
        # cluster_sim_pairs = [(data, sim) for (data, sim) in zip(cluster_data, cluster_member_similarities)]
        sorted_results = cluster_member_similarities.flatten().argsort()[::-1]
        return sorted_results