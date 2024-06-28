import json
import math
from PersianStemmer import PersianStemmer
from utils import *

def index(pretty=True, cache=False):
    if cache:
        try:
            with open("./data/positional_index.json", "r") as f:
                pos_index = json.load(f)
            with open("./data/doc_length.json", "r") as f:
                length = json.load(f)
            with open("./data/champion_list.json", "r") as f:
                champion_list = json.load(f)
            return pos_index, length, champion_list
        except:
            pass

    indentation = 4 if pretty else None

    f = open("./data/IR_data_news_12k.json")
    data = json.load(f)
    all_tokens = []
    stopwords = get_stopwords(from_cache=True, pretty=pretty)
    print("Indexing documents..")
    print("Tokenizing and Normalizing..")
    for id, doc in data.items():
        # --- Tokenizing ---
        tokens = tokenize(doc["content"])
        # --- Normalizing ---
        tokens = normalize(tokens, int(id), stopwords)
        all_tokens.extend(tokens)
        # break
    f.close()

    # Word count
    word_counts = count_common_words(all_tokens)
    with open("./data/word_count_after.json", "w") as f:
        json.dump(word_counts, f, ensure_ascii=False, indent=indentation)

    print("Stemming..")
    # --- Stemming ---
    all_tokens = stem(all_tokens, stopwords)

    word_counts = count_common_words(all_tokens)
    with open("./data/word_count_stemmed.json", "w") as f:
        json.dump(word_counts, f, ensure_ascii=False, indent=indentation)

    with open("./data/tokens.json", "w") as f:
        json.dump(all_tokens, f, ensure_ascii=False, indent=indentation)

    print("Indexing..")
    pos_index = positional_indexing(all_tokens, len(data))
    with open("./data/positional_index.json", "w") as f:
        json.dump(pos_index, f, ensure_ascii=False, indent=indentation)
    print("Indexing done.")

    # Create champion list
    champion_list = create_champion_list(pos_index)
    with open("./data/champion_list.json", "w") as f:
        json.dump(champion_list, f, ensure_ascii=False, indent=indentation)

    # Calculate length of each document
    length = calculate_doc_length(all_tokens, pos_index)
    with open("./data/doc_length.json", "w") as f:
        json.dump(length, f, ensure_ascii=False, indent=indentation)

    return pos_index, length, champion_list


# TODO: Tokenizing
def tokenize(content):
    tokens = []
    for p in punctuations:
        content = content.replace(p, " ")
    for t in content.split():
        # split by numbers
        on_num = False
        new_t = ""
        for c in t:
            new_t = new_t.strip(punctuations)
            if c in persian_numbers or c in english_numbers:
                if not on_num and new_t != "":
                    tokens.append(new_t)
                    new_t = ""
                on_num = True
            else:
                if on_num and new_t != "":
                    tokens.append(new_t)
                    new_t = ""
                on_num = False
            new_t += c
        if new_t != "":
            tokens.append(new_t)

    if tokens[-1] == "پیام":
        tokens.pop()
    if tokens[-1] == "انتهای":
        tokens.pop()
    return tokens


# TODO: Normalization
def normalize(tokens, docId, stopwords=[]):
    normalized_tokens = []
    check_verb = False
    check_email = False
    last_token = ""
    i = 0
    for t in tokens:
        new_t = t
        # Correct spacing
        # می و نمی
        if t == "می" or t == "نمی":
            check_verb = True
            last_token = t
            continue

        if "@" in t:
            check_email = True
            last_token = t
            continue

        if check_verb:
            new_t = last_token + "\u200c" + t
            check_verb = False

        if check_email:
            new_t = last_token + "." + t
            check_email = False

        # postfix spacings
        if t in postfix and last_token != "":
            new_t = last_token + "\u200c" + t
            normalized_tokens.pop()
            i -= 1

        # Unicode replacements
        new_t = new_t.replace("ك", "ک")
        new_t = new_t.replace("ي", "ی")
        new_t = new_t.replace("ئ", "ی")
        new_t = new_t.replace("ة", "ه")
        new_t = new_t.replace("ۀ", "ه")
        new_t = new_t.replace("ؤ", "و")
        new_t = new_t.replace("إ", "ا")
        new_t = new_t.replace("أ", "ا")
        new_t = new_t.replace("آ", "ا")
        new_t = new_t.replace("ٱ", "ا")
        new_t = new_t.replace("ٲ", "ا")
        new_t = new_t.replace("ٔ", "")  # hamze
        new_t = new_t.replace("ء‌‌", "")  # hamze
        new_t = new_t.replace("ْ", "")  # sokun
        new_t = new_t.replace("ً", "")  # tanvin fatha
        new_t = new_t.replace("ٍ", "")  # tanvin kasra
        new_t = new_t.replace("ٌ", "")  # tanvin zamma
        new_t = new_t.replace("ّ", "")  # tashdid
        new_t = new_t.replace("َ", "")  # fatha
        new_t = new_t.replace("ِ", "")  # kasra
        new_t = new_t.replace("ُ", "")  # zamma

        # 2 face words
        new_t = new_t.replace("هیجده", "هجده")
        new_t = new_t.replace("دگمه", "دکمه")
        new_t = new_t.replace("ملیون", "میلیون")
        new_t = new_t.replace("اتوموبیل", "اتومبیل")
        new_t = new_t.replace("استامبول", "استانبول")
        new_t = new_t.replace("انشتین", "انیشتین")
        new_t = new_t.replace("طهران", "تهران")
        new_t = new_t.replace("روبات", "ربات")
        new_t = new_t.replace("هيئت", "هیات")
        new_t = new_t.replace("آیینه", "آینه")
        new_t = new_t.replace("ترکتور", "تراکتور")

        # replace english numbers to persian numbers
        new_t = new_t.replace("0", "۰")
        new_t = new_t.replace("1", "۱")
        new_t = new_t.replace("2", "۲")
        new_t = new_t.replace("3", "۳")
        new_t = new_t.replace("4", "۴")
        new_t = new_t.replace("5", "۵")
        new_t = new_t.replace("6", "۶")
        new_t = new_t.replace("7", "۷")
        new_t = new_t.replace("8", "۸")
        new_t = new_t.replace("9", "۹")

        if new_t in stopwords:
            continue
        normalized_tokens.append((new_t, docId, i))
        i += 1
        last_token = t

    return normalized_tokens


def get_stopwords(from_cache=True, pretty=False):
    indentation = 4 if pretty else None
    if from_cache:
        try:
            with open("./data/stopwords.json", "r") as f:
                stopwords = json.load(f)
            return stopwords
        except:
            pass
    stopwords = []
    f = open("./data/IR_data_news_12k.json")
    data = json.load(f)
    all_tokens = []
    for id, doc in data.items():
        tokens = tokenize(doc["content"])
        tokens = normalize(tokens, int(id))
        all_tokens.extend(tokens)
        # break
    f.close()

    print("Counting words")
    # Word count before removing stopwords
    word_counts = count_common_words(all_tokens)
    with open("./data/word_count_before.json", "w") as f:
        json.dump(word_counts, f, ensure_ascii=False, indent=indentation)
    print("Removing stopwords..")
    top50 = list(word_counts.keys())[:50]
    try:
        with open("./data/stopwords.json", "w") as f:
            json.dump(top50, f, ensure_ascii=False, indent=indentation)
    except:
        print("Error saving stopwords")

    return top50


# Stemming
def stem(tokens, stopwords=[]):
    ps = PersianStemmer()
    ps.enableVerb = True
    stemmed_tokens = []
    i = 0
    for t in tokens:
        i += 1
        stemmed_t = ps.run(t[0])
        if stemmed_t in stopwords:
            continue
        stemmed_tokens.append((stemmed_t, t[1], t[2]))
        if i % 1000000 == 0:
            print(i, "/", len(tokens), " tokens stemmed")
    return stemmed_tokens


# TODO: Indexing
def positional_indexing(tokens, num_docs):
    # sort tokens
    tokens.sort()
    print("Tokens sorted")
    # create positional index
    positional_index = {}
    i = 0
    lt = ""
    while i < len(tokens):
        t = tokens[i][0]
        if t == "":
            i += 1
            continue
        doc = tokens[i][1]
        pos = tokens[i][2]
        if t == lt:

            # Update postings
            postings = positional_index[t][2]
            if doc in postings:
                docFreq = postings[doc][0]
                docFreq += 1
                postings[doc][0] = docFreq

                positions = postings[doc][2]
                positions.append(pos)
                postings[doc][2] = positions

            else:
                # Update frequency
                freq = positional_index[t][0]
                freq += 1
                positional_index[t][0] = freq
                postings[doc] = [1, 0, [pos]]
        else:
            # {term : freq, idf, {doc: (docFreq, tf, [pos])}}
            positional_index[t] = [1, 0, {doc: [1, 0, [pos]]}]
            # update idf for previous token
            if lt != "":
                positional_index[lt][1] = round(
                    math.log(num_docs / positional_index[lt][0], LOG_BASE), 4
                )

                # Update tf for previous tokens documents
                postings = positional_index[lt][2]
                for d in postings.keys():
                    docFreq = postings[d][0]
                    tf = round(1 + math.log(docFreq, LOG_BASE), 4)
                    postings[d][1] = tf
                positional_index[lt][2] = postings
        lt = t
        i += 1
        if i % 100000 == 0:
            print(i, "/", len(tokens), " tokens indexed")
    # update tf-idf for last token
    if lt != "":
        positional_index[lt][1] = round(
            math.log(num_docs / positional_index[lt][0], LOG_BASE), 4
        )
        postings = positional_index[lt][2]
        for d in postings.keys():
            docFreq = postings[d][0]
            tf = round(1 + math.log(docFreq, LOG_BASE), 4)
            postings[d][1] = tf
        positional_index[lt][2] = postings

    return positional_index

def create_champion_list(pos_index, CHAMPION_LIST_SIZE=50):
    champion_list = {}
    for term in pos_index.keys():
        postings = pos_index[term][2]
        champion_list[term] = [pos_index[term][0], pos_index[term][1], {}]
        for d, v in postings.items():
            champion_list[term][2][d] = v
        champion_list[term][2] = dict(sorted(champion_list[term][2].items(), key=lambda x: x[1][1], reverse=True))
        champion_list[term][2] = dict(list(champion_list[term][2].items())[:CHAMPION_LIST_SIZE])
    return champion_list

def calculate_doc_length(tokens, pos_index):
    # sort based on docId
    tokens.sort(key=lambda x: x[1])

    length = {}
    for term in tokens:
        if term[1] not in length:
            length[term[1]] = 0
        t = term[0]
        doc = term[1]
        if t in pos_index:
            idf = pos_index[t][1]
            postings = pos_index[t][2]
            tf = 0
            tf = postings[doc][1]

            w_d = tf * idf
            length[doc] += w_d * w_d

    for doc in length.keys():
        length[doc] = math.sqrt(length[doc])

    return length
