from flask import Flask, request, jsonify, render_template
from elasticsearch import Elasticsearch
import json
import os

app = Flask(__name__)

# Initialize Elasticsearch client
es = Elasticsearch(
    "https://localhost:9200",
    verify_certs=False,
    ca_certs="../http_ca.crt",
    api_key="RmdtSG01QUI5YXdHS0tiQkJCcEE6UGxhZFc5aUFSNjJPUjZQZG1XcHRlZw=="
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    form_data = request.form.to_dict(flat=False)
    
    # Build the Elasticsearch query
    must_clauses = []
    for i in range(len(form_data['searchTerm[]'])):
        search_term = form_data['searchTerm[]'][i]
        metadata_field = form_data['metadata[]'][i]
        if metadata_field != 'all':
            must_clauses.append({
                "match": {metadata_field: search_term}
            })
        else:
            must_clauses.append({
                "query_string": {
                    "query": search_term
                }
            })

    query = {
        "query": {
            "bool": {
                "must": must_clauses
            }
        }
    }

    # Perform the search
    index_name = "relevance"
    response = es.search(index=index_name, body=query)

    # Extract the search results
    search_results = [hit['_source'] for hit in response['hits']['hits']]

    # Save results to a JSON file
    results_file = './search_results.json'
    with open(results_file, 'w') as file:
        json.dump(search_results, file, indent=4)

    return jsonify(search_results)

if __name__ == '__main__':
    app.run(debug=True)
