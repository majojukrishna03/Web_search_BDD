from collections import defaultdict
from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup
import threading

class WebCrawler:
    def __init__(self):
        self.index = defaultdict(list)
        self.visited = set()
        self.session_visited = set()
        self.links_found = 0
        self.lock = threading.Lock()  # Lock for synchronizing access to index

    def crawl(self, url, base_url=None, depth=0, max_depth=20):
        if url in self.visited or depth >= max_depth or self.links_found >= 10:
            return
        self.visited.add(url)
        self.session_visited.add(url)

        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            text = soup.get_text()

            # Acquire lock before accessing shared resource
            with self.lock:
                self.index[url] = text

            for link in soup.find_all('a'):
                href = link.get('href')
                if href:
                    if urlparse(href).netloc:
                        absolute_url = href
                    else:
                        absolute_url = urljoin(base_url or url, href)
                    if absolute_url.startswith("http"):
                        if absolute_url not in self.session_visited and absolute_url not in self.visited:
                            self.links_found += 1
                            if self.links_found > max_depth:
                                return
                            self.crawl(absolute_url, base_url=base_url or url, depth=depth+1, max_depth=max_depth)
        except Exception as e:
            print(f"Error crawling {url}: {e}")
