from abc import ABC, abstractmethod

class Encoder(ABC):
    """
    Class that encodes queries and any data entries to be retrieved
    """
    @abstractmethod
    def encode(self, string: str):
        pass