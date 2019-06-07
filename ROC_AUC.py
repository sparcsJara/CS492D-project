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

path = 'all_the_news_preprocessed.txt'
web_hose = pd.read_json(path)
print(web_hose.shape)

encoder = LabelEncoder()

X = web_hose["content"]
y = encoder.fit_transform(web_hose["category"])
y = label_binarize(y, classes=[0, 1, 2])

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

log_clf = OneVsRestClassifier(LogisticRegression(solver='sag', multi_class='multinomial'))
y_score = log_clf.fit(train_vectors, y_train).decision_function(test_vectors)

class_name = ["C", "B", "A"]
n_classes = 3
fpr = dict()
tpr = dict()
roc_auc = dict()
lw = 1
for i in range(n_classes):
    fpr[i], tpr[i], _ = roc_curve(y_test[:, i], y_score[:, i])
    roc_auc[i] = auc(fpr[i], tpr[i])
colors = cycle(['blue', 'red', 'green'])
for i, color in zip(range(n_classes), colors):
    plt.plot(fpr[i], tpr[i], color=color, lw=lw,
             label='ROC curve of class {0} (area = {1:0.2f})'
                   ''.format(class_name[i], roc_auc[i]))
plt.plot([0, 1], [0, 1], 'k--', lw=lw)
plt.xlim([-0.05, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver operating characteristic for multi-class data')
plt.legend(loc="lower right")
plt.show()
