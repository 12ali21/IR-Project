postfix = ["ها", "های", "ی", "ای", "تری", "تر", "ترین", "گر" , "گری", "ام", "ات", "اش", "ای"]
punctuations = " \n\t.,?!()[]{}\"/*-_'،؛:؟!<>«»¬\u200c\u200F\u200E\u202b\u2067\u2069\u202C《》"
persian_numbers = "۰۱۲۳۴۵۶۷۸۹"
english_numbers = "0123456789"
LOG_BASE = 10




def count_common_words(tokens):
    word_count = {}
    for t in tokens:
        if t[0] in word_count:
            word_count[t[0]] += 1
        else:
            word_count[t[0]] = 1
    sorted_word_count = dict(
        sorted(word_count.items(), key=lambda item: item[1], reverse=True)
    )

    return sorted_word_count
