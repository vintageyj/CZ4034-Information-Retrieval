from abc import ABC, abstractmethod
import numpy as np
from cleantext import clean

import encoders
import indexers
from enums import *

class Retriever(ABC):
    """
    Class that retrieves results based on query
    1. must store data in original user-friendly format and return relevant results via retrieve_results
    """

    @abstractmethod
    def retrieve_results(self):
        pass

class BaseRetriever(Retriever):
    """
    Initialize desired encoder and indexer and handle searching
    """
    def __init__(self, encoder_type: EncoderType, indexer_type: IndexerType, corpus, encoder_kwargs = {}, indexer_kwargs = {}):
        self.encoder_type = encoder_type
        self.indexer_type = indexer_type
        self.corpus = corpus
        self._init_encoder(corpus, encoder_kwargs)
        self._init_indexer(indexer_kwargs)

    def _init_encoder(self, corpus, encoder_kwargs):
        enc = getattr(encoders, self.encoder_type.value)(**encoder_kwargs)
        self.encoder = enc
        self.encoder.encode_corpus(corpus)
        

    def _init_indexer(self, indexer_kwargs):
        indexer = getattr(indexers, self.indexer_type.value)(**indexer_kwargs)
        self.indexer = indexer
        self.indexer.create_indexes(self.encoder.encoded_corpus_)

    def retrieve_results(self, query: str):
        ## applying cleaning to query, assuming user only inputs normal text and not emojis, bullet points etc. this assumption speeds up querying and is based on normal expected user behavior
        query = clean(query, no_punct=True)
        encoded_query = self.encoder.encode(query)
        results = self.indexer.search_indexes(encoded_query)
        return results
