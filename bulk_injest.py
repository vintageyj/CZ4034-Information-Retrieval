import csv
import pandas as pd
from os.path import join
import tqdm
from elasticsearch import Elasticsearch
from elasticsearch.helpers import streaming_bulk

DATASET_FOLDER = "data"
DATASET_FILENAME = "final_sg_companies_reviews_clean.csv"
DATASET_PATH = join(DATASET_FOLDER, DATASET_FILENAME)

INDEX_NAME = "sg_companies_reviews_clean"
ELASTIC_PASSWORD = "_zu3*L+gRcVhaVbDqb6P"

def create_index(client, index_name:str):
    """Creates an index in Elasticsearch if one isn't already there."""
    client.indices.create(
        index=index_name,
        body={
            "settings": {
                "number_of_shards": 1,

                "analysis": {
                    "analyzer": {
                        "english_stop_words": {
                            "type": "stop",
                            "tokenizer": "lower",
                            "stopwords": "_english_"
                        }
                    }
                },
            },
            "mappings": {
                    "properties": {
                    "@timestamp": {
                        "type": "date"
                    },
                    "Company Name": {
                        "type": "text",
                        "analyzer": "english_stop_words"
                    },
                    "Overall Rating": {
                        "type": "double"
                    },
                    "Review Date": {
                        "type": "date",
                        "format": "iso8601"
                    },
                    "Review Title": {
                        "type": "text",
                        "analyzer": "english_stop_words"
                    },
                    "Job Details": {
                        "type": "text",
                        "analyzer": "english_stop_words"
                    },
                    "Job Title": {
                        "type": "text",
                        "analyzer": "english_stop_words"
                    },
                    "Location": {
                        "type": "text"
                    },
                    "Pros": {
                        "type": "text",
                        "analyzer": "english_stop_words"
                    },
                    "Cons": {
                        "type": "text",
                        "analyzer": "english_stop_words"
                    },
                    "Overall Review with Title": {
                        "type": "text",
                        "analyzer": "english_stop_words"
                    },
                    "Predicted Sentiment": {
                        "type": "text"
                    },
                    "sentence": {
                        "type": "text",
                        "analyzer": "english_stop_words"
                    },
                    "position": {
                        "type": "text"
                    },
                    "sentiment": {
                        "type": "text"
                    },
                    "Country": {
                        "type": "text"
                    },
                }
            },
        },
        ignore=400,
    )


def generate_actions(data_path=DATASET_PATH):
    """Reads the file through csv.DictReader() and for each row
    yields a single document. This function is passed into the bulk()
    helper to create many documents in sequence.
    """
    with open(data_path, mode="r", encoding='utf-8') as f:
        reader = csv.DictReader(f)

        for row in reader:
            doc = {
                "Company Name": row["Company Name"],
                "Overall Rating": row["Overall Rating"],
                "Review Date": row["Review Date"],
                "Review Title": row["Review Title"],
                "Job Details": row["Job Details"],
                "Job Title": row["Job Title"],
                "Location": row["Location"],
                "Pros": row["Pros"],
                "Cons": row["Cons"],
                "Overall Review with Title": row["Overall Review with Title"],
                "Predicted Sentiment": row["Predicted Sentiment"],
                "sentence": row["sentence"],
                "position": row["position"],
                "sentiment": row["sentiment"],
                "Country": row["Country"],
            }
            yield doc


def main():

    print("Connecting to the Elastic cluster...")
    client = Elasticsearch(
        # Add your cluster configuration here!
        "http://localhost:9200",
        basic_auth=("elastic", ELASTIC_PASSWORD)
    )
    if not client.ping():
        raise ConnectionError("Connection failed")
    else:
        print("Connection successful")

    print("Creating an index...")
    create_index(client, INDEX_NAME)

    df = pd.read_csv(DATASET_PATH)
    number_of_docs = len(df)

    print("Indexing documents...")
    progress = tqdm.tqdm(unit="docs", total=number_of_docs)
    successes = 0
    for ok, action in streaming_bulk(
        client=client, index=INDEX_NAME, actions=generate_actions(),
    ):
        progress.update(1)
        successes += ok
    print("Indexed %d/%d documents" % (successes, number_of_docs))


if __name__ == "__main__":
    main()