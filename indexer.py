from collections import defaultdict
import threading

class Indexer:
    def __init__(self):
        self.index = defaultdict(list)
        self.lock = threading.Lock()  # Lock for synchronizing access to index

    def index_page(self, url, text):
        with self.lock:
            self.index[url] = text

    def search(self, keyword):
        results = []
        with self.lock:
            for url, text in self.index.items():
                if keyword.lower() in text.lower():
                    results.append(url)
        return results[:10]
