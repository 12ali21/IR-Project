from indexer import tokenize, normalize, stem

def search(query, pos_index):
    query_tokens = tokenize(query)
    query_tokens = normalize(query_tokens, 0, [])
    query_tokens = stem(query_tokens)
    print(query_tokens)