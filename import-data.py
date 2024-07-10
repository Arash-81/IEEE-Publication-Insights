import json
from elasticsearch import Elasticsearch

es = Elasticsearch(
    "https://localhost:9200", 
    verify_certs=False, 
    ca_certs="./http_ca.crt", 
    api_key="RmdtSG01QUI5YXdHS0tiQkJCcEE6UGxhZFc5aUFSNjJPUjZQZG1XcHRlZw=="
)

def process_publications(publications, index_name):
    for publication in publications:
        es.index(index=index_name, document=publication)

def process_json_file(file_path):
    with open(file_path, "r", encoding="utf-8") as json_file:
        try:
            data = json.load(json_file)
            relevance = data.get("Relevance", [])
            newest = data.get("Newest", [])
            return relevance, newest
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON in file {file_path}: {e}")
            return [], []

file_path = './publications.json'
relevance, newest = process_json_file(file_path)

process_publications(relevance, "relevance")
process_publications(newest, "newest")
