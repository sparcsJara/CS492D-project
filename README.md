# CS492D-project
Machine learning for social science

# How to install packages 
pip install -r requirments.txt

# How to use it
아래와 같이 순차적으로 사용해주세요.

(1) top 500 ngram 구하기 \n
corpus/data.json file 
-> get_ngram.py
-> top_500.txt

(2) 각 ngram의 idf 계산 \n
corpus/data.json + top_500.txt
-> calculate_idf.py
-> idf.txt

(3) vectorize \n
corpus/data.json + idf.txt 
-> vectorize.py
-> vector.txt

(4) categorize \n
corpus/univlist.json + vector.txt
-> categorize.py
-> preprocessed.txt

(5) model training \n
preprocessed.txt
-> training_model.py

(6) ROC AUC curve \n
preprocessed.txt
->ROC_AUC.py

(7) empath difference \n
preprocessed.txt
-> empath_statics.py




