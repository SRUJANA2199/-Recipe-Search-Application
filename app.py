from flask import Flask, request, render_template, jsonify
from opensearchpy import OpenSearch
import os
import pandas as pd

app = Flask(__name__, template_folder=os.path.join(os.getcwd(), 'templates'))

# OpenSearch client setup
client = OpenSearch(
    hosts=[{'host': 'localhost', 'port': 9200}],
    use_ssl=False
)

# Index some sample data (you can skip this if data is already indexed)
@app.route('/index_data')
def index_data():
    document = {
        'title': 'Introduction to OpenSearch',
        'content': 'OpenSearch is an open-source search engine...',
        'category': 'Technology'
    }
    response = client.index(index="website_data", body=document)
    client.indices.refresh(index="website_data")  # Refresh index to make sure the document is searchable
    return jsonify(response)

# Home route that serves the search form and recipe data
@app.route('/')
def home():
    # Load CSV data at startup
    file_path = r'C:\Users\SRUJANA\Downloads\ml\epi_recipe.final.csv'
    data = pd.read_csv(file_path)

    # Convert DataFrame to list of dictionaries
    recipes = data.to_dict(orient='records')
    return render_template('index.html', recipes=recipes)

# Search route that queries OpenSearch
@app.route('/search', methods=['POST'])
def search():
    query = request.form.get('query')
    print(f"Search query: {query}")

    search_body = {
        "query": {
            "multi_match": {
                "query": query,
                "fields": ["title", "content"]
            }
        }
    }
    
    try:
        response = client.search(index="website_data", body=search_body)
        print(response)  # Debugging line to check the response
        results = response['hits']['hits']
    except Exception as e:
        print(f"Search error: {e}")
        results = []
        
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
