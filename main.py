# A persian news search engine
from PersianStemmer import PersianStemmer
from utils import *
from indexer import index


if __name__ == "__main__":
    pos_index = index(pretty=True)
    query = input("Enter your query: ")
    
