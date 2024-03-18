from enum import Enum

class EncoderType(Enum):
    TermFrequencyEncoder = "TermFrequencyEncoder"
    SentenceTransformerEncoder = "SentenceTransformerEncoder"

class IndexerType(Enum):
    LeaderIndexer = "LeaderIndexer"