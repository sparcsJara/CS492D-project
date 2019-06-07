import pathlib
from nltk import OrderedDict, bigrams, trigrams
import _operator
import os,math
from gensim.utils import simple_preprocess
from nltk.corpus import stopwords
import json
from collections import Counter
import nltk
from nltk.tokenize import word_tokenize
import re
import numpy as np
from empath import Empath


json_path = input("input the path of json data")
idf_path = input("input the path of idf file ")

stop_words = stopwords.words('english')
stop_words.extend(['from', 'subject', 're', 'edu', 'use'])

lexicon = Empath()

ngram_list = []
idf_dict = {}
with open(idf_path, 'r',  encoding='UTF-8') as f:
    lines = f.readlines()
    for line in lines:
        ngram_list.append(line.split(':')[0])
        idf_dict[line.split(':')[0]] = float(line.split(':')[1])
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

def tf_value(content_dictionary, word):
    ngram_elem = tuple(word.split(' '))
    if ngram_elem in content_dictionary:
        return content_dictionary[ngram_elem] / len(dictionary)
    return 0

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

def normalize_ngram_vectors(x):
    max = np.max(x)
    min = np.min(x)
    divider = max - min
    tmp = x - min
    return tmp/divider

def vectorize(content_dictionary, article_len):
    vector_list = []
    for ngram in ngram_list:
        idf_tf_value= tf_value(content_dictionary, ngram) * idf_dict[ngram]
        vector_list.append(idf_tf_value)
    return normalize_ngram_vectors(np.array(vector_list))


file = pathlib.Path(json_path)
file_text = file.read_text(encoding='utf-8')
json_data = json.loads(file_text)
vector_list = []
affective_attributes = ["anger", "sadness", "swearing_terms", "positive_emotion", "negative_emotion", "nervousness" ,"fear", "hate"]
education_attribute = ["school", "college","business", "programming", "science", "economics", "politics", "technology","philosophy","law"]
supporting_attributes = ["help", "money",  "vacation", "health", "government", "leisure", "wealthy", "banking", "internet", "exercise","play","religion", "sports",  "restaurant", "payment"]
interpersonal_attributes = ["trust","listen","appearance", "friends","family",  "healing", "communication", "love", "hearing", "sympathy"]
working_attributes = ["work", "office", "white_collar_job", "blue_collar_job","rural","urban"]
reputation_attributes = ["occupation",  "pride", "dispute", "royalty", "journalism", "social_media", "leader", "legend", "heroic","power","achievement"]
anti_social_attributes = ["violence", "fight", "injury", "rage","torment", "terrorism","poor", "alcohol","aggression","suffering", "crime"]

empath_attributes = affective_attributes+education_attribute+supporting_attributes+interpersonal_attributes+working_attributes+reputation_attributes+anti_social_attributes

print(len(json_data.items()))

articles_count = 0
for univ, univ_articles in json_data.items():
    for article in univ_articles:
        articles_count += 1
print(articles_count)

temp_count = 0
output_txt_name = json_path.split["."][0].split("/")[1] + "_vector,txt"

with open(output_txt_name, 'w', encoding='UTF-8') as f:
    univ_dict = {}
    f.write("{")

    item_count = 0
    for univ, univ_articles in json_data.items():
        vector_list = []
        for article in univ_articles:
            dictionary = wordgram_analyze(article["content"])
            ngram_vector = vectorize(dictionary, articles_count)
            ngram_vector = ngram_vector.tolist()
            empath_vector = lexicon.analyze(article["content"], normalize=True, categories=empath_attributes)
            empath_vector = (list)(empath_vector.values())
            merging_vector = ngram_vector + empath_vector
            vector_list.append(merging_vector)
            temp_count += 1
            if temp_count %100 ==0:
                print(temp_count)
        f.write("\""+univ +"\"" + ":")
        f.write(json.dumps(vector_list))
        item_count += 1
        if(item_count < len(json_data.items())):
            f.write(",\n")
    f.write("}")

