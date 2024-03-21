from abc import ABC, abstractmethod
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import TruncatedSVD, PCA
import numpy as np


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
        sorted_results = cluster_member_similarities.flatten().argsort()[::-1]
        return sorted(cluster_sim_pairs, reverse = True, key = lambda x: x[1])
    
    def _fit_dim_reducer(self, data, min_explained_var):
        return PCA(n_components = min_explained_var).fit(data)