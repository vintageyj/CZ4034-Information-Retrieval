from abc import ABC, abstractmethod
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sentence_transformers import SentenceTransformer


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
    
class SentenceTransformerEncoder(Encoder):
    def __init__(self):
        self.model_name = 'sentence-transformers/all-MiniLM-L6-v2' ## TODO: put model names into config file for easier experimentation
        self.model = SentenceTransformer(self.model_name)
        self.encoded_corpus_ = None

    def encode_corpus(self, corpus: np.ndarray):
        self.encoded_corpus_ = self.model.encode(corpus)

    def encode(self, text: str):
        encoded_text = self.model.encode([text])
        return encoded_text