from abc import ABC, abstractmethod
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer


class Encoder(ABC):
    """
    Class that encodes queries and any data entries to be retrieved (may be pretrained e.g. word2vec)
    1. must encode corpus as a whole 
    2. must be able to encode string queries using same encoder
    """
    @abstractmethod
    def encode(self, text: str):
        pass

class TermFrequencyEncoder(Encoder):
    def __init__(self):
        self.vectorizer = TfidfVectorizer()
        self.encoded_corpus_ = None

    def encode_corpus(self, corpus: np.ndarray):
        self.encoded_corpus_ = self.vectorizer.fit_transform(corpus)

    def encode(self, text: str):
        encoded_text = self.vectorizer.transform([text])
        return encoded_text