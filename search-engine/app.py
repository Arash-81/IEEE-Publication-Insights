from flask import Flask, request, jsonify, render_template
from elasticsearch import Elasticsearch
import json
import os

app = Flask(__name__)

es = Elasticsearch(
    "https://localhost:9200",
    verify_certs=False,
    ca_certs="../http_ca.crt",
    api_key="d2JXY29KQUJZcWFtaDJ1S2t5Y3I6S3FFdHpiS0ZTc2UzV1p4LThvakN4dw=="
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    form_data = request.form.to_dict(flat=False)
    
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

    index_name = "relevance"
    response = es.search(index=index_name, body=query)

    search_results = [hit['_source'] for hit in response['hits']['hits']]

    return render_template('results.html', search_results=search_results)

if __name__ == '__main__':
    app.run(debug=True)
