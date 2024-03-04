from abc import ABC, abstractmethod
import numpy as np

class Retriever(ABC):
    """
    Class that retrieves results based on query
    """

    @abstractmethod
    def retrieve_candidates(self):
        pass

class LeaderRetriever(Retriever):
    """
    Perform Leader Search for retrieval, by taking a query and looking for the nearest "leader" and returning results in the same cluster as the leader
    """
    def __init__(self):
        pass

    def retrieve_candidates(self, query: np.array):
        pass