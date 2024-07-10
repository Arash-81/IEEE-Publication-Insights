from elasticsearch import Elasticsearch
import json
# Initialize Elasticsearch client
es = Elasticsearch(
    "https://localhost:9200", 
    verify_certs=False, 
    ca_certs="./http_ca.crt", 
    api_key="RmdtSG01QUI5YXdHS0tiQkJCcEE6UGxhZFc5aUFSNjJPUjZQZG1XcHRlZw=="
)


# Define the query without the date filter
query = {
    "query": {
        "bool": {
            "must": [
                {"range": {"Cites in Papers": {"gt": 10}}},
                {"range": {"Full Text Views": {"gt": 1000}}}
            ]
        }
    }
}

index_name = "relevance"
response = es.search(index=index_name, body=query)

results = [hit['_source'] for hit in response['hits']['hits']]

with open('./search_results.json', 'w', encoding='utf-8') as json_file:
    json.dump(results, json_file, ensure_ascii=False, indent=4)

