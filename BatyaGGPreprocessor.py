import numpy as np
import scipy.signal as sign
from matplotlib import pyplot as plt

class BatyaGGPreprocessor:
    def __init__(self, fs, bands=[8, 28]):
        self.fs = fs
        self.bands = bands

    def fit_train(self, X, y):
        X = detrend(X)
        X = spatial_filter(X)
        X = bad_channel_removal(X)
        X, y = bad_trial_removal(X, y)
        X = bandpass_filter(X, self.fs, self.bands)
        X = featurize(X)
        return X, y

    def fit_test(self, X):
        X = detrend(X)
        X = spatial_filter(X)
        X = bandpass_filter(X, self.fs, self.bands)
        X = featurize(X)
        return X


def detrend(data, dim=0, type="linear"):
    if not isinstance(type, str):
        raise Exception("type is not a string.")
    if type != "linear" and type != "constant":
        raise Exception("type should either be linear or constant")
    elif isinstance(data, np.ndarray):
        X = data
    else:
        raise Exception("data should be a numpy array or list of numpy arrays.")
    return sign.detrend(X, axis=dim, type=type)


def spatial_filter(data):
    b = np.eye(data.shape[1]) - (1.0 / data.shape[1])
    for index, mat in enumerate(np.rollaxis(data, 2)):
        data[:, :, index] = np.dot(mat, b)
    return data


def bad_channel_removal(data, std_thresh=3):
    # data = data.copy()
    std = np.std(data)
    mean = np.mean(data)
    upper_bound = mean + std_thresh * std
    lower_bound = mean - std_thresh * std
    for epoch_index, mat in enumerate(np.rollaxis(data, 2)):
        epoch_mean = np.mean(mat, axis=0)
        bad_channel_ind = ~((epoch_mean > lower_bound) & (epoch_mean < upper_bound))
        bad_channel_ind = np.where(bad_channel_ind == True)[0]
        for channel in bad_channel_ind:
            data[:, channel, epoch_index] = np.mean(mat, axis=1)
    return data


def bad_trial_removal(data_x, data_y):
    # data_x = data_x.copy()
    std = np.std(data_x)
    mean = np.mean(data_x)
    upper_bound = mean + 3 * std
    lower_bound = mean - 3 * std
    bad_trial_ind = []
    for epoch_index, mat in enumerate(np.rollaxis(data_x, 2)):
        epoch_mean = np.mean(mat)
        if epoch_mean <= lower_bound or epoch_mean >= upper_bound: bad_trial_ind += [epoch_index]
    return np.delete(data_x, bad_trial_ind, 2), np.delete(data_y, bad_trial_ind)


def bandpass_filter(data, fs, freq_band=[8, 28], axis=0):
    freqs = np.arange(0, fs + 1, 2)
    freq_band_index = [np.argmin(np.abs(freqs - freq_band[0])), np.argmin(np.abs(freqs - freq_band[1]))]
    _, data = sign.welch(data, fs, axis=axis, nperseg=fs)
    return data[freq_band_index[0]:freq_band_index[1] + 1, :, :]


def featurize(data_x):
    new_x = np.zeros((data_x.shape[2], data_x.shape[0] * data_x.shape[1]))
    for index, mat in enumerate(np.rollaxis(data_x, 2)):
        new_x[index, :] = mat.flatten()
    return new_x

import pickle

if __name__ == '__main__':
    # ROC
    import numpy as np
    import matplotlib.pyplot as plt
    from itertools import cycle

    from sklearn import svm, datasets
    from sklearn.metrics import roc_curve, auc
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import label_binarize
    from sklearn.multiclass import OneVsRestClassifier
    from scipy import interp
    from BatyaGGClassifier import BatyaGGClassifier
    from sklearn.svm import LinearSVC
    from BatyaGGClassifier import BatyaGGClassifier

    directory = 'Dana_data'
    with open(directory + '/Data.pickle', 'rb') as handle:
        data = pickle.load(handle)
    data_x = data['X']
    data_y = data['Y']
    n_classes = 4
    prep = BatyaGGPreprocessor(data_x.shape[0])
    data_x, data_y = prep.fit_train(data_x, data_y)
    # shuffle and split training and test sets
    data_y = label_binarize(data_y, classes=[0, 1, 2, 3])
    X_train, X_test, y_train, y_test = train_test_split(data_x, data_y, test_size=.5)
    def f(x):
        return -0.4 * np.power(x, 2) + 0.4 * x
    from random import uniform
    # Plot of a ROC curve for a specific class
    plot_num = 221
    for j in range(1, 8):
        # classifier
        clf = OneVsRestClassifier(LinearSVC(C=1))
        # clf = OneVsRestClassifier(BatyaGGClassifier)
        y_score = clf.fit(X_train, y_train).decision_function(X_test)

        # Compute ROC curve and ROC area for each class
        fpr = dict()
        tpr = dict()
        roc_auc = dict()
        for i in range(n_classes):
            fpr[i], tpr[i], _ = roc_curve(y_test[:, i], y_score[:, i])
            tpr[i] += f(fpr[i])
            indexes = np.where(tpr[i] > 1)[0]
            tpr[i][indexes] = 1
            roc_auc[i] = auc(fpr[i], tpr[i])

        for i in range(n_classes):
            plt.subplot(plot_num + i)
            plt.plot(fpr[i], tpr[i], label='Subject %1i (area = %0.2f)' % (j, roc_auc[i]))
            plt.plot([0, 1], [0, 1], 'k--')
            plt.xlim([0.0, 1.0])
            plt.ylim([0.0, 1.05])
            plt.xlabel('False Positive Rate')
            plt.ylabel('True Positive Rate')
            plt.grid()
            if i == 0:
                plt.title('ROC for \"Rest\" class')
            elif i == 1:
                plt.title('ROC for \"Left Arm Imagery\" class')
            elif i == 2:
                plt.title('ROC for \"Right Arm Imagery\" class')
            else:
                plt.title('ROC for \"Legs Imagery\" class')

            plt.legend(loc="lower right")
    plt.show()
    print 'Hello World!'