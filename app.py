from flask import Flask, render_template, request, jsonify
import json
import re
from collections import defaultdict

app = Flask(__name__)

# Load datasets
def load_datasets():
    """Load all media datasets from JSON files"""
    datasets = {}
    media_types = ['movies', 'shows', 'books', 'games']
    
    for media_type in media_types:
        try:
            with open(f'data/{media_type}.json', 'r') as f:
                datasets[media_type] = json.load(f)
        except FileNotFoundError:
            datasets[media_type] = []
    
    return datasets

def search_by_title(query, datasets):
    """Search for exact and partial matches by title"""
    results = defaultdict(list)
    query_lower = query.lower()
    
    for media_type, media_list in datasets.items():
        for item in media_list:
            title_lower = item['title'].lower()
            if query_lower in title_lower:
                # Calculate match score (exact match gets higher score)
                if query_lower == title_lower:
                    item['match_score'] = 100
                else:
                    item['match_score'] = 80
                results[media_type].append(item)
    
    # Sort by match score
    for media_type in results:
        results[media_type].sort(key=lambda x: x['match_score'], reverse=True)
    
    return results

def search_by_terms(query, datasets):
    """Search through genres, descriptions, and other metadata"""
    results = defaultdict(list)
    query_terms = query.lower().split()
    
    for media_type, media_list in datasets.items():
        for item in media_list:
            score = 0
            searchable_text = f"{item.get('genres', '')} {item.get('description', '')} {item.get('characters', '')}".lower()
            
            # Count matching terms with proper scoring
            for term in query_terms:
                if term in searchable_text:
                    score += 1
                if term in item['title'].lower():
                    score += 2  # Title matches get bonus points
            
            if score > 0:
                # Calculate max possible score per term (3 points max: 1 for text + 2 for title)
                max_possible_score = len(query_terms) * 3
                # Normalize to 0-100 and cap at 100
                normalized_score = min(100, (score / max_possible_score) * 100)
                item['match_score'] = normalized_score
                results[media_type].append(item)
    
    # Sort by match score
    for media_type in results:
        results[media_type].sort(key=lambda x: x['match_score'], reverse=True)
    
    return results

def get_cross_recommendations(search_results, datasets, limit=5):
    """Get cross-category recommendations based on search results"""
    if not search_results:
        return {}
    
    # Collect found items to exclude from cross-recommendations
    found_items = set()
    for media_type, items in search_results.items():
        for item in items:
            found_items.add((media_type, item['title'].strip().lower()))
    
    # Collect all genres and themes from found results (normalized)
    themes = set()
    for media_type, items in search_results.items():
        for item in items[:3]:  # Use top 3 results from each category
            if 'genres' in item:
                # Strip whitespace and normalize case, filter out empty strings
                genres = [genre.strip().lower() for genre in item['genres'].split(',') if genre.strip()]
                themes.update(genres)
    
    # Find similar items in other categories
    cross_recommendations = defaultdict(list)
    
    for media_type, media_list in datasets.items():
        for item in media_list:
            # Skip items already in search results
            item_key = (media_type, item['title'].strip().lower())
            if item_key in found_items:
                continue
            
            # Strip whitespace and normalize case for item genres, filter out empty strings
            item_genres = set(genre.strip().lower() for genre in item.get('genres', '').split(',') if genre.strip())
            common_themes = themes & item_genres
            
            if common_themes:
                item['match_score'] = min(100, len(common_themes) * 20)  # Cap at 100%
                cross_recommendations[media_type].append(item)
    
    # Sort and limit results
    for media_type in cross_recommendations:
        cross_recommendations[media_type].sort(key=lambda x: x['match_score'], reverse=True)
        cross_recommendations[media_type] = cross_recommendations[media_type][:limit]
    
    return cross_recommendations

@app.route('/')
def homepage():
    """Render the homepage with search form"""
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    """Handle search requests"""
    query = request.form.get('query', '').strip()
    search_mode = request.form.get('mode', 'title')
    
    if not query:
        return render_template('results.html', error="Please enter a search term")
    
    datasets = load_datasets()
    
    if search_mode == 'title':
        results = search_by_title(query, datasets)
    else:  # terms mode
        results = search_by_terms(query, datasets)
    
    # Get cross-category recommendations
    cross_recommendations = get_cross_recommendations(results, datasets)
    
    return render_template('results.html', 
                         query=query, 
                         mode=search_mode,
                         results=results, 
                         cross_recommendations=cross_recommendations)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)