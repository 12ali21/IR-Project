from indexer import tokenize, normalize, stem, positional_indexing
import math
import json

def search(query, pos_index, length, k = 5):
    query_tokens = tokenize(query)
    query_tokens = normalize(query_tokens, 0, [])
    query_tokens = stem(query_tokens)
    query_index = positional_indexing(query_tokens, 1)

    scores = {}
    print(query_index)
    for term in query_index.keys():
        q_posts = query_index[term][2]
        if term in pos_index:
            idf = pos_index[term][1]
            w_q = q_posts[0][1] * idf
            postings = pos_index[term][2]
            for doc in postings.keys():
                w_d = postings[doc][1] * idf
                if doc in scores:
                    scores[doc] += w_q * w_d
                else:
                    scores[doc] =  w_q * w_d

    # print(scores)
    for doc in scores:
        scores[doc] /= length[doc]
    # print(scores)

    # return top k results
    results = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    print(len(results))
    f = open("data/IR_data_news_12k.json", "r")
    data = json.load(f)
    f.close()
    for i in range(k):
        if i >= len(results):
            break
        print("Score: ", results[i][1])
        result = data[str(results[i][0])]
        print("Title: ", result['title'])
        print("URL: ", result['url'])
