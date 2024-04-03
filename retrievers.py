from abc import ABC, abstractmethod
import numpy as np
import pandas as pd
from cleantext import clean

import encoders
import indexers
from enums import *

from elasticsearch import Elasticsearch

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
    def __init__(self, encoder_type: EncoderType, indexer_type: IndexerType, data: pd.DataFrame, column_to_index: str, encoder_kwargs = {}, indexer_kwargs = {}):
        self.encoder_type = encoder_type
        self.indexer_type = indexer_type
        self.data = data
        self._init_encoder(data[column_to_index].to_numpy(), encoder_kwargs)
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
        result_uids = self.data.iloc[[result[0] for result in results]]['id'].to_numpy()
        result_similarities = [result[1] for result in results]
        return [(uid, sim.item()) for uid, sim in zip(result_uids, result_similarities)]

class ElasticRetriever(Retriever):
    """
    Class that retrieves results based on query using ElasticSearch
    """
    def __init__(self, indexer_type: IndexerType, data_path, elastic_pwd='_zu3*L+gRcVhaVbDqb6P', index_name = "sg_companies_reviews_clean", fresh_instance:bool = False, indexer_kwargs = {}):
        self.client = Elasticsearch(
            # Add your cluster configuration here!
            "http://localhost:9200",
            basic_auth=("elastic", elastic_pwd)
        )
        self.indexer_type = indexer_type
        self.data_path = data_path
        self.index_name = index_name
        self.fresh_instance = fresh_instance
        if self.client.ping():
            print("Connection to Elastic cluster successful")
        else:
            raise ConnectionError("Connection to Elastic cluster failed")
        self._init_indexer(indexer_kwargs)
        
    def _init_indexer(self, indexer_kwargs):
        indexer_kwargs['client'] = self.client
        self.indexer = getattr(indexers, self.indexer_type.value)(**indexer_kwargs)
        if self.index_name in self.client.indices.get_alias(index="*"):
            if not self.fresh_instance:
                return
            else:
                self.client.indices.delete(index=self.index_name)
        self.indexer.create_indexes(self.data_path, self.index_name)
        
    def retrieve_results(self, queries: dict, pagination: tuple = (0, 10000), operator = "must"):
        print(self.client)
        response = self.indexer.search_indexes(queries, pagination, operator)
        total_hits = response['hits']['total']['value']
        results = response['hits']['hits']

        # Extracting the '_source' field from each result
        sources = [result['_source'] for result in results]

        # Converting to DataFrame
        df = pd.DataFrame(sources)

        # Optionally, if you want to include the '_id' or '_score' field as well
        # df['_id'] = [result['_id'] for result in search_results]
        # df['_score'] = [result['_score'] for result in search_results]
        
        return total_hits, df