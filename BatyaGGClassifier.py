from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.ensemble import VotingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV
import numpy as np


class BatyaGGClassifier(BaseEstimator, ClassifierMixin):

    def __init__(self, zero_thresh=0.1, tol=100, step=0.1, max_iter=25):
        self.zero_thresh = zero_thresh
        self.tol = tol
        self.step = step
        self.max_iter = max_iter
        self.fitted = False
        self.clf = None

    def fit(self, X, y):
        X_new, y_new = self._remove_nols_in_y(X, y)
        svc = SVC(kernel='rbf', C=10, probability=True)  # C
        logreg = LogisticRegression(C=10, tol=1e-5)  # C
        abc = AdaBoostClassifier(n_estimators=500)
        gbc = GradientBoostingClassifier(n_estimators=1000, max_depth=5)  # max_depth
        rfc = RandomForestClassifier(n_estimators=500, n_jobs=-1)
        etc = ExtraTreesClassifier(n_estimators=500, bootstrap=True, n_jobs=-1)
        self.clf = VotingClassifier(estimators=[('svc', svc), ('logreg', logreg),
                                       ('abc', abc), ('gbc', gbc), ('rfc', rfc),
                                       ('etc', etc)], voting='soft')
        # tuning_parameters = {'svc__C': [33, 66], 'logreg__C': [33, 66]}
        # self.clf = GridSearchCV(clf, tuning_parameters, cv=5)
        self.clf.fit(X_new, y_new)
        self.fitted = True
        _, counts = np.unique(y, return_counts=True)
        zero_count = counts[0]
        pred_zero_count = 0
        loop_count = 0
        last_action = 'nothing'
        while np.abs(zero_count - pred_zero_count) > self.tol and loop_count < self.max_iter:
            test_prediction = self.predict(X)
            labels, counts = np.unique(test_prediction, return_counts=True)
            pred_zero_count = counts[0] if len(labels) == 4 else 0
            if pred_zero_count < zero_count:
                if last_action is 'decreased': self.step = self.step / 2
                self.zero_thresh += self.step
                last_action = 'increased'
            else:
                if last_action is 'increased': self.step = self.step / 2
                self.zero_thresh -= self.step
                last_action = 'decreased'
            loop_count += 1
        assert (type(self.zero_thresh) == float), "zero_thresh parameter must be float or double"
        assert (type(self.tol) == int), "tol parameter must be integer"
        assert (type(self.step) == float), "step parameter must be float or double"
        assert (type(self.max_iter) == int), "max_iter parameter must be integer"
        return self

    def _meaning(self, x):
        return (True if x >= self.treshold_ else False)

    def predict(self, X, y=None):
        if not self.fitted: raise RuntimeError("You must train classifier before predicting data")
        probs = self.clf.predict_proba(X)
        indexes = np.argmax(probs, axis=1)
        label_probs = probs[np.arange(0, probs.shape[0]), indexes]
        labels = indexes + 1
        doubtful_label_indexes = np.where(label_probs < self.zero_thresh)[0]
        labels[doubtful_label_indexes] = 0
        return labels

    def score(self, X, y):
        predicts = self.predict(X)
        eq = (predicts == y)
        where = np.where(eq == True)[0]
        return 1.0 * where.size / y.size

    def _remove_nols_in_y(self, data_x, data_y, remove=1):
        # input dim sample X channels, flattened or deflattened input
        indexes = np.where(data_y == 0)[0]
        indexes = indexes[:int(indexes.shape[0] * remove)]
        return np.delete(data_x, indexes, 0), np.delete(data_y, indexes, 0)

    # def accuracy(self):
    #     return self.clf.best_score_


