class Ranker:
    def rank_results(self, results, index, keyword):
        ranked_results = {}
        for url in results:
            text = index[url]
            score = text.lower().count(keyword.lower())
            ranked_results[url] = score
        return dict(sorted(ranked_results.items(), key=lambda x: x[1], reverse=True))
