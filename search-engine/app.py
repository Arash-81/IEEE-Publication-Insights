from flask import Flask, request, jsonify, render_template
from elasticsearch import Elasticsearch
import json
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
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

    with open('./search_results.json', 'w') as f:
        json.dump(search_results, f)

    return render_template('results.html', search_results=search_results)

if os.path.exists('./publications.json'): #./search_results.json
    with open('./publications.json', 'r') as file:
        try:
            data = json.load(file)['Relevance']
        except json.JSONDecodeError:
            data = []
else:
    data = []

df = pd.DataFrame(data)

def concatenate_fields(row):
    title = row['title'] if row['title'] else ''
    ieee_keywords = ' '.join(row['IEEE Keywords']) if row['IEEE Keywords'] else ''
    author_keywords = ' '.join(row['Author Keywords']) if row['Author Keywords'] else ''
    abstract = row['abstract'] if row['abstract'] else ''
    return ' '.join([title, ieee_keywords, author_keywords, abstract])

if not df.empty:
    df['text'] = df.apply(concatenate_fields, axis=1)
    df['title'] = df['title'].fillna('').str.lower().str.strip()
    df = df[['title', 'text']]

    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(df['text'])
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
else:
    cosine_sim = None

def recommend_articles(article_title, top_n=5):
    if cosine_sim is None:
        return []

    article_title = article_title.lower().strip()

    try:
        idx = df[df['title'] == article_title].index[0]
    except IndexError:
        return []

    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    seen_titles = set()
    recommendations = []
    for i, score in sim_scores[1:]:
        title = df.iloc[i]['title']
        if title not in seen_titles:
            seen_titles.add(title)
            recommendations.append((title, score))
        if len(recommendations) >= top_n:
            break

    return [title for title, score in recommendations]

@app.route('/recommend', methods=['GET', 'POST'])
def recommend():
    if request.method == 'POST':
        article_title = request.form.get('article_title')
        top_n = int(request.form.get('top_n'))
        recommendations = recommend_articles(article_title, top_n)
        return render_template('recommendations.html', recommendations=recommendations)
    return render_template('recommend.html')

if __name__ == '__main__':
    app.run(debug=True)