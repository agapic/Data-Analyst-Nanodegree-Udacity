#!/usr/bin/python

import sys
import pickle
import fix_records
import add_features
import selection_and_tuning
import operator
from sklearn.pipeline import Pipeline
sys.path.append("../tools/")

from feature_format import featureFormat, targetFeatureSplit
from tester import dump_classifier_and_data

### Task 1: Select what features you'll use.
### features_list is a list of strings, each of which is a feature name.
### The first feature must be "poi".
# Exhaustive list of every available feature in the data
feature_list = [
            "poi",
            "deferral_payments",
            "deferred_income",
            "director_fees",
            "exercised_stock_options",
            "expenses",
            "from_messages",
            "from_poi_to_this_person",
            "from_this_person_to_poi",
            "long_term_incentive",
            "loan_advances",
            "other",
            "bonus",
            "restricted_stock",
            "restricted_stock_deferred",
            "salary",
            "shared_receipt_with_poi",
            "to_messages",
            "total_payments",
            "total_stock_value"]

### Load the dictionary containing the dataset
with open("final_project_dataset.pkl", "r") as data_file:
    data_dict = pickle.load(data_file)

### Task 2: Remove outliers/fix records
for key in ["TOTAL", "THE TRAVEL AGENCY IN THE PARK", "LOCKHART EUGENE E"]:
    data_dict.pop(key, 0)

data_dict = fix_records.fixBhatnagar(data_dict)
data_dict = fix_records.fixBelfer(data_dict)

# List valid occurrences

non_nas = {}
for feature in feature_list:
    for k, v in data_dict.iteritems():
        if v[feature] != 'NaN':
            if feature not in non_nas.keys():
                non_nas[feature] = 0
            non_nas[feature] += 1

valid_records_per_feature = sorted((non_nas).items(), key = operator.itemgetter(1), reverse = True)
print valid_records_per_feature
### Task 3: Create new feature(s)
### Store to my_dataset for easy export below.

# Select 11 Best Features

feature_list = selection_and_tuning.get_k_best(data_dict, feature_list, 11)
feature_list.insert(0, 'poi')

# Create latent features
#data_dict = add_features.financial_data_feature(data_dict)
#feature_list.append("stock_and_payments")
data_dict = add_features.poi_interaction_ratios(data_dict)
feature_list.append("to_poi_ratio")
feature_list.append("from_poi_ratio")

my_dataset = data_dict
my_features_list = feature_list

### Extract features and labels from dataset for local testing
data = featureFormat(data_dict, feature_list, sort_keys = True)
labels, features = targetFeatureSplit(data)

### Task 4: Classifiers

from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import MinMaxScaler
from sklearn.feature_selection import SelectKBest
from sklearn.svm import SVC
from sklearn import tree
scaler = MinMaxScaler()

classifiers = [{'classifier': LogisticRegression(),
                'params': {  "clf__C": [0.05, 0.5, 1, 10, 10**2, 10**3, 10**5, 10**10, 10**15],
                    "clf__tol":[10**-1, 10**-2, 10**-4, 10**-5, 10**-6, 10**-10, 10**-15],
                    "clf__class_weight":['balanced']
                    }},
               {'classifier': tree.DecisionTreeClassifier(),
                'params':
                    {
                        "clf__criterion": ["gini", "entropy"],
                        "clf__min_samples_split": [10,15,20,25]
                    }
                }]

#Task 5: Evaluate

# This is used when comparing multiple algorithms. If more algorithms are used, this should be
# modularized to a function
# for c in classifiers:
#     clf = Pipeline(steps=[("scaler", scaler), ("skb", SelectKBest(k='all')), ("clf", c['classifier'])])
#     selection_and_tuning.evaluate(clf, my_dataset, feature_list, features, labels, 50, c['params'])

# This is our best algorithm, tuned and optimized.
clf = Pipeline(steps=[("scaler", scaler),
                      ("skb", SelectKBest(k='all')),
                      ("clf", LogisticRegression(tol=0.1, C = 10**9, class_weight='balanced'))])



### Task 6: Dump your classifier, dataset, and features_list so anyone can
### check your results. You do not need to change anything below, but make sure
### that the version of poi_id.py that you submit can be run on its own and
### generates the necessary .pkl files for validating your results.

dump_classifier_and_data(clf, my_dataset, feature_list)
