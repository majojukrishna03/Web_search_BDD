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
    keyword = request.args.get('keyword')
    url = request.args.get('url')
    
    if not (keyword and url):
        return jsonify({'error': 'Both keyword and URL parameters are required'}), 400

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

def index_documents(keyword):
    indexer = Indexer()
    indexer.index = crawler.index
    results = indexer.search(keyword)
    
    if results:
        ranker = Ranker()
        ranked_results = ranker.rank_results(results, indexer.index, keyword)
        return ranked_results
    else:
        return None

if __name__ == '__main__':
    app.run(debug=True)
