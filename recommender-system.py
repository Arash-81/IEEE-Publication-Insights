import json
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

with open('./publications.json', 'r') as file:
    data = json.load(file)['Relevance']

df = pd.DataFrame(data)

def concatenate_fields(row):
    title = row['title'] if row['title'] else ''
    ieee_keywords = ' '.join(row['IEEE Keywords']) if row['IEEE Keywords'] else ''
    author_keywords = ' '.join(row['Author Keywords']) if row['Author Keywords'] else ''
    abstract = row['abstract'] if row['abstract'] else ''
    return ' '.join([title, ieee_keywords, author_keywords, abstract])


df['text'] = df.apply(concatenate_fields, axis=1)

df['title'] = df['title'].fillna('').str.lower().str.strip()

df = df[['title', 'text']]

vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = vectorizer.fit_transform(df['text'])

cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

def recommend_articles(article_title, cosine_sim=cosine_sim, df=df, top_n=5):
    article_title = article_title.lower().strip()

    try:
        idx = df[df['title'] == article_title].index[0]
    except IndexError:
        return "Title not found in the dataset."

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

def display_recommendations(recommendations):
    if isinstance(recommendations, str):
        print(recommendations)
    else:
        print("Recommended articles:")
        for idx, title in enumerate(recommendations, 1):
            print(f"{idx}. {title}")

def main():
    article_title = input("Enter the exact title of the article: ")
    top_n = int(input("Enter the number of recommendations (e.g., 5, 10, 15): "))
    recommendations = recommend_articles(article_title, top_n=top_n)
    display_recommendations(recommendations)

if __name__ == "__main__":
    main()