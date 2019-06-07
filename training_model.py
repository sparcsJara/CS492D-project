from sklearn.preprocessing import LabelEncoder, OneHotEncoder
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB, MultinomialNB, BernoulliNB
from sklearn.metrics import classification_report, accuracy_score, roc_curve, auc, confusion_matrix
import numpy as np
from sklearn.ensemble import RandomForestClassifier, BaggingClassifier
from sklearn.multiclass import OneVsRestClassifier

from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
import time
from sklearn import tree
from sklearn.model_selection import KFold
import matplotlib.pyplot as plt
from sklearn.preprocessing import label_binarize
from itertools import cycle

path = input("input the path of preprocessed data")
web_hose = pd.read_json(path)
print(web_hose.shape)

encoder = LabelEncoder()

X = web_hose["content"]
y = encoder.fit_transform(web_hose["category"])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=None)

count = 0
new_list = []
for x in X_train:
    new_list.append(np.asarray(x))
train_vectors = np.array(new_list)
new_list = []
for x in X_test:
    new_list.append(np.asarray(x))
test_vectors = np.array(new_list)

clf = GaussianNB()
clf.fit(train_vectors, y_train)
pred = clf.predict(test_vectors)
print(accuracy_score(y_test, pred, ))
print(classification_report(y_test, pred))

clf2 = MultinomialNB()
clf2.fit(train_vectors, y_train)
pred2 = clf2.predict(test_vectors)
print(accuracy_score(y_test, pred2, ))
print(classification_report(y_test, pred2))

clf3 = BernoulliNB()
clf3.fit(train_vectors, y_train)
pred3 = clf2.predict(test_vectors)
print(accuracy_score(y_test, pred3, ))
print(classification_report(y_test, pred3))

log_clf = LogisticRegression(solver='sag', multi_class='multinomial')
log_clf.fit(train_vectors, y_train)
log_pred = log_clf.predict(test_vectors)
print(classification_report(y_test, log_pred))
print(confusion_matrix(y_test, log_pred))

rf = RandomForestClassifier(n_estimators=20)
rf.fit(train_vectors, y_train)
pred3 = rf.predict(test_vectors)
print(classification_report(y_test, pred3))

estimator = SVC(kernel="linear")
n_estimators = 20
n_jobs = 1
model = BaggingClassifier(base_estimator=estimator,
                          n_estimators=n_estimators,
                          max_samples=1. / n_estimators,
                          n_jobs=n_jobs)
model.fit(train_vectors, y_train)
print("fit end")
y_pred_train = model.predict(train_vectors)
y_pred_test = model.predict(test_vectors)
print(classification_report(y_train, y_pred_train))
print(classification_report(y_test, y_pred_test))

