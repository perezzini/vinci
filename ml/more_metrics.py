import math
from sklearn.metrics import confusion_matrix
from sklearn.metrics import recall_score

def confidence_interval(metric, const, n_test_samples):
    """
    Calculates the confidence interval for given metric, and
    a given constant that defines chosen probability
    """
    std_deviation = math.sqrt((metric*(1 - metric))/n_test_samples)
    return metric - std_deviation*const, metric + std_deviation*const

def tn(y_true, y_pred): return confusion_matrix(y_true, y_pred)[0, 0]

def fp(y_true, y_pred): return confusion_matrix(y_true, y_pred)[0, 1]

def fn(y_true, y_pred): return confusion_matrix(y_true, y_pred)[1, 0]

def tp(y_true, y_pred): return confusion_matrix(y_true, y_pred)[1, 1]

def specificity(y_true, y_pred):
    """
    AKA True Negative Rate
    """
    tn = tn(y_true, y_pred)
    fp = fp(y_true, y_pred)
    return tn/(float(tn + fp))

def fpr(y_true, y_pred):
    fp = fp(y_true, y_pred)
    tn = tn(y_true, y_pred)
    return fp/(float(tn + fp))

def tpr(y_true, y_pred):
    """
    AKA Recall or Sensitivity
    """
    return recall_score(y_pred=y_pred, y_true=y_true)
