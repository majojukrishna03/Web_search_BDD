from flask import Flask, request, jsonify, render_template
from threading import Thread
from webcrawler import WebCrawler
from indexer import Indexer
from ranker import Ranker
import csv

app = Flask(__name__)
crawler = None
indexing_complete = False  # Flag to indicate indexing status

@app.route('/search', methods=['GET'])
def search():
    global crawler, indexing_complete
    keyword = request.args.get('keyword')
    url = request.args.get('url')
    if keyword and url:
        if crawler is None:
            crawler = WebCrawler()
        crawler_thread = Thread(target=crawler.crawl, args=(url,))
        crawler_thread.start()
        crawler_thread.join()
        results = index_documents(keyword)

        if results:
            return jsonify(results)
        else:
            return jsonify({'error': 'Result not found for the given keyword and URL'}), 404
    else:
        return jsonify({'error': 'Both keyword and URL parameters are required'}), 400


def indexing_status():
    global indexing_complete
    return jsonify({'indexing_complete': indexing_complete})

def index_documents(keyword):
    global indexing_complete
    indexer = Indexer()
    indexer.index = crawler.index
    results = indexer.search(keyword)
    if results:
        ranker = Ranker()
        ranked_results = ranker.rank_results(results, indexer.index, keyword)
        indexing_complete = True  # Set indexing complete flag to True
        return ranked_results
    else:
        return None

if __name__ == '__main__':
    app.run(debug=True)
