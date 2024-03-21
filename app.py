from flask import Flask, request, jsonify
from threading import Thread
from webcrawler import WebCrawler
from indexer import Indexer
from ranker import Ranker

app = Flask(__name__)
crawler = None

@app.route('/search', methods=['GET'])
def search():
    global crawler
    
    # Extract keyword and URL from request parameters
    keyword = request.args.get('keyword')
    url = request.args.get('url')
    
    # Check if both keyword and URL are provided
    if not (keyword and url):
        return jsonify({'error': 'Both keyword and URL parameters are required'}), 400

    try:
        # Create a new WebCrawler instance if not already initialized
        if crawler is None:
            crawler = WebCrawler()
        
        # Start crawling process in a separate thread
        crawler_thread = Thread(target=crawler.crawl, args=(url,))
        crawler_thread.start()
        crawler_thread.join()

        # Index documents and rank results
        results = index_and_rank(keyword)

        # Return search results or error if no results found
        if results:
            return jsonify(results)
        else:
            return jsonify({'error': 'Result not found for the given keyword and URL'}), 404
    
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

def index_and_rank(keyword):
    """
    Perform indexing and ranking of documents based on the given keyword.
    
    Args:
        keyword (str): The search keyword.
        
    Returns:
        dict: Ranked search results.
    """
    try:
        indexer = Indexer()
        indexer.index = crawler.index  # Use index from the crawler
        results = indexer.search(keyword)
        
        if results:
            ranker = Ranker()
            ranked_results = ranker.rank_results(results, indexer.index, keyword)
            return ranked_results
        else:
            return None
    
    except Exception as e:
        raise RuntimeError(f'An error occurred during indexing and ranking: {str(e)}')

if __name__ == '__main__':
    app.run(debug=True)
