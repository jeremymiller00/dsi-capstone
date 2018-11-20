
""" 
Functions -based solution
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pickle

from sklearn.preprocessing import StandardScaler
from sklearn.metrics import make_scorer, confusion_matrix, recall_score, roc_auc_score, roc_curve, recall_score, classification_report
from sklearn.model_selection import GridSearchCV, cross_val_score, RandomizedSearchCV, cross_validate
from sklearn.ensemble import GradientBoostingClassifier
import matplotlib.pyplot as plt


def standard_confusion_matrix(y_true, y_pred):
    """Make confusion matrix with format:
                  -----------
                  | TP | FP |
                  -----------
                  | FN | TN |
                  -----------
    Parameters
    ----------
    y_true : ndarray - 1D
    y_pred : ndarray - 1D

    Returns
    -------
    ndarray - 2D
    """
    [[tn, fp], [fn, tp]] = confusion_matrix(y_true, y_pred)
    return np.array([[tp, fp], [fn, tn]])

def print_roc_curve(y_test, probabilities, model_type):
    '''
    Calculates and prints a ROC curve given a set of test classes and probabilities from a trained classifier
    '''
    tprs, fprs, thresh = roc_curve(y_test, probabilities)
    plt.figure(figsize=(12,10))
    plt.plot(fprs, tprs, 
         label=model_type, 
         color='red')
    plt.plot([0,1],[0,1], 'k:')
    plt.legend()
    plt.xlabel("FPR")
    plt.ylabel("TPR")
    plt.title("ROC Curve AUC: {} Recall: {}".format(roc_auc, recall))
    plt.show()

######################################################################

if __name__ == '__main__':
    # change path to get appropriate cutoff (first_quarter, first_half, third_quarter; CHANGE PATH IN WRITE OUT!)
    X_train = pd.read_csv('data/processed/first_half/X_train.csv')
    y_train = pd.read_csv('data/processed/first_half/y_train.csv')
    y_train = y_train['module_not_completed']
    X_test = pd.read_csv('data/processed/first_half/X_test.csv')
    y_test = pd.read_csv('data/processed/first_half/y_test.csv')
    y_test = y_test['module_not_completed']

    X_train.fillna(value = 0, inplace = True)
    X_test.fillna(value = 0, inplace = True)

    # estimator
    gb = GradientBoostingClassifier()
    
    # GridSearch parameters

    gb_params = {
            'max_depth': [2, 3, 5],
            'learning_rate': [0.001, 0.01, 0.1, 1],
            'n_estimators': [100, 1000],
            'subsample': [0.5, 0.3, 0.1],
            'min_samples_leaf': [1, 5, 10, 50],
            'min_samples_split': [2, 10, 50, 100]
            'max_features': ['auto', 'sqrt'],
    }

    gb_clf = RandomizedSearchCV(gb, 
                        param_distributions=gb_params,
                        n_iter = 10,
                        scoring='roc_auc',
                        n_jobs=-1,
                        cv=5)

    gb_clf.fit(X_train, y_train)

    gb_model = gb_clf.best_estimator_

    # best parameters determined by grid search
    # gb_model = GradientBoostingClassifier(criterion='friedman_mse', init=None,learning_rate=0.01, loss='deviance', max_depth=3, max_features='auto', max_leaf_nodes=None, min_impurity_decrease=0.0, min_impurity_split=None,min_samples_leaf=1, min_samples_split=2, min_weight_fraction_leaf=0.0, n_estimators=1000, presort='auto', random_state=None, subsample=0.1, verbose=0, warm_start=False)
    # gb_model.fit(X_train, y_train)

    # save model
    # pickle.dump(gb_model, open('models/gradient_boost_completion_first_half.p', 'wb')) 

    # cross validate
    cv = cross_validate(gb_model, X_train, y_train, scoring = 'roc_auc', cv=5, return_train_score=1)
    print(cv)

    # evaluation
    roc_auc_cv = cross_val_score(gb_model, X_train, y_train, scoring = 'roc_auc', cv=5)
    recall_cv = cross_val_score(gb_model, X_train, y_train, scoring = 'recall', cv=5)
    precision_cv = cross_val_score(gb_model, X_train, y_train, scoring = 'precision', cv=5)
    accuracy_cv = cross_val_score(gb_model, X_train, y_train, scoring = 'accuracy', cv=5)
    f1_cv = cross_val_score(gb_model, X_train, y_train, scoring = 'f1_micro', cv=5)

    print('Best Model: {}'.format(gb_model))
    # print('Best Model parameters: {}'.format(rf_model.best_params_))
    print('Roc Auc: {}'.format(roc_auc_cv))
    print('Recall Score: {}'.format(recall_cv))
    print('Precision Score: {}'.format(precision_cv))
    print('Accuracy Score: {}'.format(accuracy_cv))
    print('F1 Micro: {}'.format(f1_cv))


'''
    # final model evaluation (see jupyter notebook)
    predictions = gb_model.predict(X_test)
    roc_auc = roc_auc_score(y_test, predictions)
    probas = gb_model.predict_proba(X_test)[:, :1]
    tprs, fprs, thresh = roc_curve(y_test, probas)
    recall = recall_score(y_test, predictions)
    conf_mat = standard_confusion_matrix(y_test, predictions)
    class_report = classification_report(y_test, predictions)

    print_roc_curve(y_test, probas, 'Gradient Boosting')
    print('Best Model: {}'.format(gb_model))
    print('\nRoc Auc: {}'.format(roc_auc))
    print('\nRecall Score: {}'.format(recall))
    print('\nClassification Report:\n {}'.format(class_report))
    print('\nConfusion Matrix:\n {}'.format(standard_confusion_matrix(y_test, predictions)))

'''
