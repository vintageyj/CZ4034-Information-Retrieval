from abc import ABC, abstractmethod

class Indexer(ABC):
    """
    Class that organizes indexed data to be retrival-ready
    """
    
    @abstractmethod
    def create_indexes(self):
        pass

class LeaderIndexer(Indexer):
    def __init__(self):
        pass

    def create_indexes(self):
        pass