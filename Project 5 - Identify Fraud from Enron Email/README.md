# Identifying Fraud from the Enron Dataset
### Written by Andrew Gapic

## Introduction

In the year 2000, Enron was known as one of the largest energy companies in the United States, claiming nearly $111 billion in revenues. At the end of 2001, it was revealed that there was widespread corporate fraud. Essentially all of Enron's nonexistent profits were created through a method called "mark-to-market" accounting, in which they would report profits even though they didn't earn a single dime. Even worse, they were solely responsible for the California electricity crisis, by which they performed large-scale blackouts to seize arbitrage opportunities.

The goal for this project is to analyze the characteristics of employees who worked at Enron during the crisis to predict if they are a person of interest ("POI"). Various resources (documentaries, news articles, etc.) were used to label people in the data set as POIs if they were previously indicted (that is, there is a 100% chance they were guilty). The application of machine learning to this project may be of assistance if we take the predictions from the Enron data model and apply them to other companies facing similar circumstances, through identifying persons of interest (we are using a naive assumption here by assuming fraud at other companies is similar to that of Enron, which may or may not be the case).

## Overview and Outliers

The dataset consisted of 146 records with 20 features (14 financial features, 6 e-mail features) and 1 label `POI`. Overall, there were 18 POIs identified beforehand and labelled accordingly. Three data points were removed: 

* `Lockhart Eugene E`  -- no values input for features

* `TOTAL` -- this was the sum of all the other points

* `The Travel Agency in the Park`  -- uncertain as to what this means -- could be an input error

### Record Reconstruction

There were two records in the dataset that looked suspicious: `BELFER ROBERT` and `BHATNAGAR SANJAY`. Spot checking the PDF `enron61702insiderpay.pdf`, included with this folder, I found that the data entered into `final_project_dataset.pkl` was shifted one column to the right relative to the PDF. It was clear as the total stock value was actually the deferred stock value in the PDF. I reconstructed both Sanjay's and Robert's data based on the PDF since they had important data that would aid us in our analysis.

## Feature Selection/Engineering

<table>
  <tr>
    <td><b>Feature</b></td>
    <td><b>Score</b></td>
    <td><b>Frequency in Data</b></td>
  </tr>
  <tr>
    <td>Total Stock Value</td>
    <td>22.51</td>
    <td>125</td>
  </tr>
  <tr>
    <td>Exercised Stock Options</td>
    <td>22.35</td>
    <td>100</td>
  </tr>
  <tr>
    <td>Bonus</td>
    <td>20.79</td>
    <td>81</td>
  </tr>
  <tr>
    <td>Salary</td>
    <td>18.29</td>
    <td>94</td>
  </tr>
  <tr>
    <td>Stock and Payments (total)</td>
    <td>17.39</td>
    <td>107</td>
  </tr>
  <tr>
    <td>Deferred Income</td>
    <td>11.42</td>
    <td>49</td>
  </tr>
  <tr>
    <td>Long Term Incentive</td>
    <td>9.92</td>
    <td>65</td>
  </tr>
  <tr>
    <td>Total Payments</td>
    <td>9.28</td>
    <td>123</td>
  </tr>
  <tr>
    <td>Restricted Stock</td>
    <td>8.83</td>
    <td>110</td>
  </tr>
  <tr>
    <td>Shared Receipt with POI</td>
    <td>8.59</td>
    <td>86</td>
  </tr>
  <tr>
    <td>Loan Advances</td>
    <td>7.18</td>
    <td>3</td>
  </tr>
</table>


The top eleven features were selected using scikit-learn's `SelectKBest` algorithm, as can be seen from the chart above. Interestingly, `loan advances` only appears three times in the data yet made it to the top eleven features list. Even more somewhat counterintuitive is that only one e-mail feature made it to the list. It is important to realize that SelectKBest gives us a better idea of the data through univariate feature selection, it doesn't necessarily optimize it, meaning the inclusion of e-mail features into our model may give us more accurate results.

Three new features were engineered and tested alongside the selection of these features:

* `stock and payments` - The sum of the total stock value and total payments of that employee. 

*  `to_poi_ratio` - proportion of e-mails sent to POIs

* `from_poi_ratio` - proportion of e-mails received from POIs

Extra caution was used when populating the POI fields, as some employees appeared to have more e-mails received from POIs than overall e-mails received (see James Bannatine, for instance). Additionally, people that were already marked as POIs were not included in this ratio to avoid double counting or inflated values. Unfortunately, these values were not able to make it to the top eleven selected features.

The total stock and payments field appeared to work out well, with a score of 17.39. This could very well be due to the fact that it's some sort of weighted average between total stock value and total payments. Either way, I felt that it was a good variable to capture a more holistic value for an employee's financial footprint in the company.

Each feature was scaled using MinMaxScaler, scored using SelectKBest, and then run under various classification algorithms. This was all done in a pipeline as to avoid information leakage (the MinMax of the entire data set will indeed be different than the MinMax of the training and test data sets).

## Algorithm

The two different algorithms used were decision tree classifiers and logistic regression, with logistic regression having a higher performance. Logistic regression works out nicely as it thrives in classifying data as a positive or a negative. In our case, it provided excellent results when it came to classifying a person as a POI or not.

Tuning was done both manually and automatically using GridSearchCV. It proved to be very important as the results for each algorithm differed drastically even when one parameter different even slightly.

Manual tuning included determining which parameters to add to each algorithm and adding/removing features. GridSearchCV provided a convenient way to perform linear combinations for all of the different parameters and report the best result (which we can get using `clf.best_estimator_` and `clf.best_params_`).

#### More on Tuning

In a nutshell, parameter tuning is important because it _optimizes_ our algorithm's performance on our given data set. To measure our algorithm's performance, we need to validate and evaluate our data for each different combination of our selected parameters. Algorithms tend to be very general in nature and _not_ specifically tuned to any data set. Therefore, we must iteratively tune our algorithm until we obtain an evaluation we are satisified with.

#### Tuning Process

The process used to manually tune each algorithm is shown below. Each metric was the result of 50 iterations and the mean was used to obtain the final values.

* All original features used (no new features)

<table>
  <tr>
    <td><b>Metric</b></td>
    <td><b>Logistic Regression</b></td>
    <td><b>Decision Tree</b></td>
  </tr>
  <tr>
    <td>Recall</td>
    <td>0.6</td>
    <td>0.4</td>
  </tr>
  <tr>
    <td>Precision</td>
    <td>0.429</td>
    <td>0.33</td>
  </tr>
  <tr>
    <td>Accuracy</td>
    <td>0.86</td>
    <td>0.837</td>
  </tr>
</table>


* All original features and all new features

<table>
  <tr>
    <td><b>Metric</b></td>
    <td><b>Logistic Regression</b></td>
    <td><b>Decision Tree</b></td>
  </tr>
  <tr>
    <td>Recall</td>
    <td>0.6</td>
    <td>0.4</td>
  </tr>
  <tr>
    <td>Precision</td>
    <td>0.75</td>
    <td>0.33</td>
  </tr>
  <tr>
    <td>Accuracy</td>
    <td>0.93</td>
    <td>0.837</td>
  </tr>
</table>


* Top 11 features selected from SelectKBest without new features

<table>
  <tr>
    <td><b>Metric</b></td>
    <td><b>Logistic Regression</b></td>
    <td><b>Decision Tree</b></td>
  </tr>
  <tr>
    <td>Recall</td>
    <td>0.4</td>
    <td>0.44</td>
  </tr>
  <tr>
    <td>Precision</td>
    <td>0.25</td>
    <td>0.356</td>
  </tr>
  <tr>
    <td>Accuracy</td>
    <td>0.791</td>
    <td>0.849</td>
  </tr>
</table>


* Top 11 features selected from SelectKBest and new features added

<table>
  <tr>
    <td><b>Metric</b></td>
    <td><b>Logistic Regression</b></td>
    <td><b>Decision Tree</b></td>
  </tr>
  <tr>
    <td>Recall</td>
    <td>0.8</td>
    <td>0.56</td>
  </tr>
  <tr>
    <td>Precision</td>
    <td>0.44</td>
    <td>0.547</td>
  </tr>
  <tr>
    <td>Accuracy</td>
    <td>0.86</td>
    <td>0.893</td>
  </tr>
</table>


* Top 11 features selected from SelectKBest and new features added except "stock_and_payments". (final algorithm)

<table>
  <tr>
    <td><b>Metric</b></td>
    <td><b>Logistic Regression</b></td>
    <td><b>Decision Tree</b></td>
  </tr>
  <tr>
    <td>Recall</td>
    <td>0.8</td>
    <td>0.52</td>
  </tr>
  <tr>
    <td>Precision</td>
    <td>0.571</td>
    <td>0.493</td>
  </tr>
  <tr>
    <td>Accuracy</td>
    <td>0.91</td>
    <td>0.879</td>
  </tr>
</table>


The final classifier algorithm chosen was logistic regression with the following parameters obtained by using GridSearchCV: ```{tol : 0.1, C = 10^9, class_weight: balanced }```. Additionally, the final parameters used in the decision tree classifier were ```{ criterion: entropy, min_samples_split: 20 } ```

The most interesting thing I discovered whilst manually tuning the data was that when e-mail features were excluded from the final features, the recall rate, precision rate, and accuracy dropped significantly (0.4, 0.25, and 0.79 respectively for logistic regression). SelectKBest had no e-mail features included in the top features, and it turns out that the inclusion of e-mail features was necessary to achieve better results. In fact, the recall rate doubled to 0.8 when the ratio of POI e-mails sent/received to total e-mails sent/received was included in the data. This makes sense as POIs are more likely to interact with other POIs since trying to hide corporate fraud and conspiracy is certainly a daunting task and requires significant collaboration.

## Validation

Validation is important because it allows us to find a valid compromise between bias and variance. High bias relates to underfitting the data and high variance relates to overfitting it. Ideally, we want the best of both worlds and so splitting our data into training sets and testing sets. 

I validated my analysis in an `evaluate` function located in `selection_and_tuning.py`. Over 50 randomized trials, I used sklearn's `train_test_split` function to split 30% of the data into a test set, and 70% into a training set. I prematurely reported my recall, precision, and accuracy without performing any _actual_ cross-validation. Interestingly, the best parameters were the same when using only `train_test_split` and when using `train_test_split` followed by a stratified shuffle split. The only difference was that the latter reported lower results, which makes sense. For the sake of consistency and to see why cross-validation is so important, I kept my original results above.

Using `best_estimator_` attribute from GridSearchCV, I cross-validated the data using 1000 folds StratifiedShuffleSplit (`test_classifier` in tester.py. StratifiedShuffleSplit returns _stratified_ splits, meaning that the same (or very similar) percentage of POIs is included for each test set created as in the entire set. I confirmed this by using some simple math -- in the entire data set out POI ratio is 18/143 = 12.59%. Using 1000 folds and a random state of 0.42, StratifiedShuffleSplit used a test size of 15 with 2 POIs -- 2/15 = 13.3% ~= 12.59%. Therefore, performing stratified splits on our data helps improve our validation significantly.

## Evaluation

As shown above, the three evaluation metrics I used were recall, precision, and accuracy. Recall that the results from the `train_test_split` were as follows:

* Recall: 0.8

* Precision: 0.571

* Accuracy: 0.91

Using the provided `tester.py`, which uses a StratifiedShuffleSplit, the results were as follows:

* Recall: 0.733

* Precision: 0.414

* Accuracy: 0.826

The results from StratifiedShuffleSplit were indeed lower than using just train_test_split. This is because using stratified splits is more accurate than just splitting the data set, giving us a nice reality check on our inflated results.

While tester.py reported worse results than my own evaluation, the most important metric, recall, is still relatively high. Undoubtedly, when attempting to find people that are guilty of fraud, having a good recall and a low precision is ideal. This means that we are able to identify a POI a large amount of the time but only sometimes flag non-POIs as guilty. If we were to have a high precision and a bad recall, then we would only flag people that are most certainly guilty and avoid flagging innocent people at all costs. The difference is subtle but important in our case -- flagging an innocent person as guilty can easily be cleared however flagging a guilty person as innocent defeats the entire purpose of this assignment and is also what we are trying to avoid.

Another important point is how accuracy is a bad metric when dealing with this data, as the POI to non-POI ratio was extremely lopsided -- only 18 POIs were identified in a dataset of 143 records. If we were able to predict every person as 'innocent', we would get an accuracy rate of 87.41%, but our recall rate would be 0 and our precision would be 0. 

## Conclusion

Overall, I found this project to be very challenging and time consuming. As such, if time were not a scarce resource, I would certainly measure the performance of many more algorithms to see if I can do better. I was quite satisfied with logistic regression and I chose it because I learned how it's quite good for classification algorithms. Additionally, analyzing the e-mails would also have been quite useful, but only if the POIs were the ones writing them. Most commonly, top executives tend to have assistants that write e-mails for them, so it would be a very challenging task if that was taken into account. 

