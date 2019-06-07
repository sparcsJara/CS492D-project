import pathlib

from nltk import OrderedDict, bigrams, trigrams
import _operator
import os,math
import gensim
from gensim.utils import simple_preprocess
from nltk.corpus import stopwords
import json
from collections import Counter
import nltk
from nltk.tokenize import word_tokenize
import re

stop_words = stopwords.words('english')
stop_words.extend(['from', 'subject', 're', 'edu', 'use'])



# 어절 n-gram 분석
# sentence: 분석할 문장, num_gram: n-gram 단위
def word_ngram(sentence, num_gram):
    # in the case a file is given, remove escape characters
    sentence = re.sub('\S*@\S*\s?', '', sentence)
    sentence = re.sub('\s+', ' ', sentence)
    sentence = re.sub("\'", "", sentence)
    sentence = sentence.replace('\n', ' ').replace('\r', ' ')
    text = tuple(sentence.split(' '))
    ngrams = [text[x:x + num_gram] for x in range(0, len(text))]
    return tuple(ngrams)


# n-gram 빈도 리스트 생성
def make_freqlist(ngrams):
    freqlist = {}
    for ngram in ngrams:
        if (ngram in freqlist):
            freqlist[ngram] += 1
        else:
            freqlist[ngram] = 1
    return freqlist


def remove_stopwords(word_tokens):
    result = []
    for w in word_tokens:
        if w not in stop_words:
            result.append(w)
    return " ".join(result)

def wordgram_analyze(content):
    target_content = content
    word_tokens = word_tokenize(target_content)
    stop_removals =remove_stopwords(word_tokens)

    ngrams = word_ngram(stop_removals, 1) + word_ngram(target_content, 2) + word_ngram(target_content, 3)
    freqlist = make_freqlist(ngrams)
    return freqlist
    # sorted_freqlist = sorted(freqlist.items(), key=_operator.itemgetter(1), reverse = True)
    # return sorted_freqlist

def tf_value(dictionary, word):
    return dictionary[word] / len(dictionary)

#article 내의 단어 분석
def tf_analyze(content):
    dictionary = wordgram_analyze(content)
    tf_dict = OrderedDict()
    for k,v in dictionary.items():
        tf_dict[str(k)] = tf_value(dictionary, str(k))
    return OrderedDict(sorted(tf_dict.items(), key=_operator.itemgetter(1), reverse=True))

def wordgram_map(articles):
    dict_map = []
    for article in articles:
        article_map = wordgram_analyze(article)
        dict_map.append(article_map)
    return dict_map

def idf_value(articles_len, dict_map ,word):
    word_count = 0
    for dict_elem in dict_map:
        if word in dict_elem:
            word_count += 1
    if word_count is 0:
        word_count = 1
    return math.log(articles_len/word_count)

def idf_analysis(articles, content):
    dict_map = wordgram_map(articles)
    dict_idf = OrderedDict()
    dict_file = wordgram_analyze(content)
    for dict_elem in dict_file.keys():
        dict_idf[dict_elem] = idf_value(len(articles). dict_map, dict_elem)
    return OrderedDict(sorted(dict_idf.items(),key=_operator.itemgetter(1),reverse=True))

def tfidf_analysis(dict_tf, dict_idf):
    tf_idf_dict = OrderedDict()
    for tf_elem in dict_tf.keys():
        tf_idf_dict[tf_elem] = dict_tf[tf_elem] * dict_idf[tf_elem]
    return OrderedDict(sorted(tf_idf_dict.items(),key=_operator.itemgetter(1),reverse=True))




path = input("input the path of json data")
file = pathlib.Path(path)
file_text = file.read_text(encoding='utf-8')
json_data = json.loads(file_text)
articles = []
# for object in json_data["Princeton University"]:
#     articles.append(object["content"])
for univ, univ_artilces in json_data.items():
    for article in univ_artilces:
        articles.append(article["content"])
result_dict = Counter()
count = 0
for article in articles:
    if not isinstance(article, str):
        continue
    temp_dict = Counter(wordgram_analyze(article))
    result_dict += temp_dict
    result_dict = result_dict.most_common(10000)
    result_dict = dict(result_dict)
    result_dict = Counter(result_dict)
    count += 1
    if count % 100 == 0:
        print(count)

frequency_dict = OrderedDict(result_dict)
frequency_ordered_dict = OrderedDict(sorted(frequency_dict.items(), key=_operator.itemgetter(1), reverse=True))
top_500 = list(frequency_ordered_dict.items())[0:500]
output_txt_name = path.split["."][0].split("/")[1] + "_top_500,txt"
with open(output_txt_name, 'w', encoding='UTF-8') as f:
    for item in top_500:
        str_sentence = ""
        str_sentence = (' '.join(item[0])) + ":" + str(item[1])
        f.write("%s\n" % str_sentence)
