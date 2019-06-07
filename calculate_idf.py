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
import pathlib

json_path = input("input the path of json data")
top_500_path = input("input the path of top 500 ")
ngram_list = []
ngram_count_dict = {}
with open(top_500_path, 'r',  encoding='UTF-8') as f:
    lines = f.readlines()
    for line in lines:
        ngram_list.append(line.split(':')[0])
        ngram_count_dict[line.split(':')[0]] = 0



stop_words = stopwords.words('english')
stop_words.extend(['from', 'subject', 're', 'edu', 'use'])

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
    stop_removals = remove_stopwords(word_tokens)
    ngrams = word_ngram(stop_removals,1)
    t1 = word_ngram(target_content, 2)
    t2 = word_ngram(target_content, 3)
    ngrams = ngrams + word_ngram(target_content, 2)
    ngrams = ngrams + word_ngram(target_content, 3)
    freqlist = make_freqlist(ngrams)
    return freqlist


def wordgram_map(articles):
    dict_map = []
    count = 0
    for article in articles:
        count += 1
        article_map = wordgram_analyze(article)
        dict_map.append(article_map)
        if count %100 == 0:
            print(count)
    return dict_map

def idf_value(dict_map,articles_len,word):
    word_count = 0
    for dict_elem in dict_map:
        if word in dict_elem:
            word_count += 1
    if word_count is 0:
        word_count = 1
    return math.log(articles_len/word_count)


def find_ngram_number(ngram):
    ngram.count(' ')

file = pathlib.Path(json_path)
file_text = file.read_text(encoding='utf-8')
json_data = json.loads(file_text)
articles = []
for univ, univ_artilces in json_data.items():
    for article in univ_artilces:
        articles.append(article["content"])
print(len(articles))
# dict_map = wordgram_map(articles)
article_len = len(articles)

count = 0

output_txt_name = json_path.split["."][0].split("/")[1] + "idf,txt"

with open(output_txt_name, 'w', encoding='UTF-8') as f:
    for article in articles:
        article_map = wordgram_analyze(article)
        for ngram in ngram_list:
            ngram_elem = tuple(ngram.split(' '))
            if ngram_elem in article_map:
                ngram_count_dict[ngram] += 1
        count += 1
        if count % 100 == 0:
            print(count)

    for ngram in ngram_list:
        word_count = ngram_count_dict[ngram]
        ngram_idf_value = math.log(article_len / word_count)
        str_sentecne = ngram + ":" + str(ngram_idf_value)
        f.write("%s\n" % str_sentecne)
        # ngram_elem = tuple(ngram.split(' '))
        # str_sentecne = ngram+":"+str(idf_value(dict_map,article_len,ngram_elem))
        # f.write("%s\n" % str_sentecne)

