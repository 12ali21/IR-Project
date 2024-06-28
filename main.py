# A persian news search engine
from PersianStemmer import PersianStemmer
from utils import *
from indexer import index
from search_engine import search


if __name__ == "__main__":
    pos_index, length, champion_list = index(pretty=True, cache=False)
    query = input("Enter your query: ")
    search(query, champion_list, length)
    # search(query, pos_index, length)
