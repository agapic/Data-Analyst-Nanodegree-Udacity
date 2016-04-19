from sklearn.feature_selection import SelectKBest
from sklearn import cross_validation
from sklearn.metrics import accuracy_score, precision_score, recall_score
from sklearn.cross_validation import train_test_split
from sklearn.grid_search import GridSearchCV
from sklearn.cross_validation import StratifiedShuffleSplit
from numpy import mean
from tester import test_classifier

import sys
sys.path.append("../tools/")
from feature_format import featureFormat, targetFeatureSplit

def get_k_best(data_dict, feature_list, num_features):
    """
    Function for selecting our KBest features.
    :param data_dict: List of employees and features
    :param feature_list: List of features to select
    :param num_features: Number (k) of features to select in the algorithm (k = 11)
    :return: Returns a list of the KBest feature names
    """
    data = featureFormat(data_dict, feature_list)
    target, features = targetFeatureSplit(data)

    clf = SelectKBest(k = num_features)
    clf = clf.fit(features, target)
    feature_weights = {}
    for idx, feature in enumerate(clf.scores_):
        feature_weights[feature_list[1:][idx]] = feature
    best_features = sorted(feature_weights.items(), key = lambda k: k[1], reverse = True)[:num_features]
    new_features = []
    for k, v in best_features:
        new_features.append(k)
    return new_features


def evaluate(clf, dataset, feature_list, features, labels, num_iter, params):
    """
    Function used to evaluate our algorithm -- prints out the mean precision, recall, and accuracy.
    :param clf: Classifier algorithm (e.g. LogisticRegression(), DecisionTreeClassifier()
    :param features:
    :param labels: Feature we're trying to classify -- POI / non-POI
    :param num_iter: Amount of time we should iterate through the data -- 50 in this case
    :param params: Parameters used in the classifier pipeline.
                    e.g. {
                        "clf__criterion": ["gini", "entropy"],
                        "clf__min_samples_split": [10,15,20,25]
                    }
    :return: Prints the accuracy, precision, and recall score.
    """

    features_train, features_test, labels_train, labels_test = \
        train_test_split(features, labels, test_size=0.3, random_state=42)



    precision_values = []
    recall_values = []
    accuracy_values = []
    print clf
    for i in xrange(0, num_iter):
        #print params
        clf = GridSearchCV(clf, params)
        clf.fit(features_train, labels_train)
        print '*****************************'
        print clf.best_estimator_
        print clf.best_params_

        clf = clf.best_estimator_
        #test_classifier(clf, dataset, feature_list)
        pred = clf.predict(features_test)
        precision_values.append(precision_score(labels_test, pred))
        recall_values.append(recall_score(labels_test, pred))
        accuracy_values.append(accuracy_score(labels_test, pred))
    print 'Recall score: ', mean(recall_values)
    print 'Precision score: ', mean(precision_values)
    print 'Accuracy score: ' , mean(accuracy_values)

