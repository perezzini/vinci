import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import learning_curve
from sklearn.model_selection import validation_curve
from sklearn.metrics import confusion_matrix
from sklearn.metrics import roc_curve
from sklearn.utils.multiclass import unique_labels
from inspect import signature

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

def tnr(y_true, y_pred):
    fp = fp(y_true, y_pred)
    tn = tn(y_true, y_pred)
    return tn/(float(tn + fp))

def tpr(y_true, y_pred):
    """
    AKA Recall or Sensitivity
    """
    return recall_score(y_pred=y_pred, y_true=y_true)

def plot_learning_curves(estimator,
                        title,
                        X,
                        y,
                        ylim=(0.0, 1.01),
                        cv=None,
                        n_jobs=-1,
                        train_sizes=np.linspace(.1, 1.0, 5),
                        scoring='accuracy',
                        verbose=1,
                        plot_std=True):
    """
    Generate a simple plot of the test and training learning curve.

    Parameters
    ----------
    estimator : object type that implements the "fit" and "predict" methods
        An object of that type which is cloned for each validation.

    title : string
        Title for the chart.

    X : array-like, shape (n_samples, n_features)
        Training vector, where n_samples is the number of samples and
        n_features is the number of features.

    y : array-like, shape (n_samples) or (n_samples, n_features), optional
        Target relative to X for classification or regression;
        None for unsupervised learning.

    ylim : tuple, shape (ymin, ymax), optional
        Defines minimum and maximum yvalues plotted.

    cv : int, cross-validation generator or an iterable, optional
        Determines the cross-validation splitting strategy.
        Possible inputs for cv are:
          - None, to use the default 3-fold cross-validation,
          - integer, to specify the number of folds.
          - :term:`CV splitter`,
          - An iterable yielding (train, test) splits as arrays of indices.

        For integer/None inputs, if ``y`` is binary or multiclass,
        :class:`StratifiedKFold` used. If the estimator is not a classifier
        or if ``y`` is neither binary nor multiclass, :class:`KFold` is used.

        Refer :ref:`User Guide <cross_validation>` for the various
        cross-validators that can be used here.

    n_jobs : int or None, optional (default=None)
        Number of jobs to run in parallel.
        ``None`` means 1 unless in a :obj:`joblib.parallel_backend` context.
        ``-1`` means using all processors. See :term:`Glossary <n_jobs>`
        for more details.

    train_sizes : array-like, shape (n_ticks,), dtype float or int
        Relative or absolute numbers of training examples that will be used to
        generate the learning curve. If the dtype is float, it is regarded as a
        fraction of the maximum size of the training set (that is determined
        by the selected validation method), i.e. it has to be within (0, 1].
        Otherwise it is interpreted as absolute sizes of the training sets.
        Note that for classification the number of samples usually have to
        be big enough to contain at least one sample from each class.
        (default: np.linspace(0.1, 1.0, 5))
    """
    plt.figure()
    plt.title(title)
    if ylim is not None:
        plt.ylim(*ylim)
    plt.xlabel('Number of observations')
    plt.ylabel('Score')
    train_sizes, train_scores, test_scores = learning_curve(
        estimator,
        X,
        y,
        cv=cv,
        n_jobs=n_jobs,
        train_sizes=train_sizes,
        scoring=scoring,
        verbose=verbose
    )
    train_scores_mean = np.mean(train_scores, axis=1)
    train_scores_std = np.std(train_scores, axis=1)
    test_scores_mean = np.mean(test_scores, axis=1)
    test_scores_std = np.std(test_scores, axis=1)

    plt.grid()

    if plot_std:
        # Draw bands
        plt.fill_between(train_sizes, train_scores_mean - train_scores_std, train_scores_mean + train_scores_std, color="#DDDDDD")
        plt.fill_between(train_sizes, test_scores_mean - test_scores_std, test_scores_mean + test_scores_std, color="#DDDDDD")

    # Draw lines
    plt.plot(train_sizes, train_scores_mean, '--', color="#111111",  label="Training score")
    plt.plot(train_sizes, test_scores_mean, color="#111111", label="Cross-validation score")
    plt.legend(loc="best")
    return plt

def plot_cm(y_true,
            y_pred,
            classes=None,
            normalize=False,
            title=None,
            cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if not title:
        if normalize:
            title = 'Normalized confusion matrix'
        else:
            title = 'Confusion matrix'

    # Compute confusion matrix
    cm = confusion_matrix(y_true, y_pred)
    # Only use the labels that appear in the data
    if classes:
        classes = classes[unique_labels(y_true, y_pred)]
    else:
        classes = unique_labels(y_true, y_pred)
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print('Normalized confusion matrix')
    else:
        print('Confusion matrix')

    print(cm)

    fig, ax = plt.subplots()
    im = ax.imshow(cm, interpolation='nearest', cmap=cmap)
    ax.figure.colorbar(im, ax=ax)
    # We want to show all ticks...
    ax.set(xticks=np.arange(cm.shape[1]),
           yticks=np.arange(cm.shape[0]),
           # ... and label them with the respective list entries
           xticklabels=classes, yticklabels=classes,
           title=title,
           ylabel='Actual label',
           xlabel='Predicted label')

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
             rotation_mode="anchor")

    # Loop over data dimensions and create text annotations.
    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j, i, format(cm[i, j], fmt),
                    ha="center", va="center",
                    color="white" if cm[i, j] > thresh else "black")
    fig.tight_layout()
    return ax

def plot_val_curves(estimator,
                    X,
                    y,
                    param_name,
                    param_range,
                    cv,
                    title,
                    xlabel,
                    ylabel,
                    scoring=None,
                    ylim=(0.0, 1.1),
                    n_jobs=-1,
                    verbose=0,
                    plot_std=True):
    train_scores, test_scores = validation_curve(estimator=estimator,
                                                X=X,
                                                y=y,
                                                param_name=param_name,
                                                param_range=param_range,
                                                cv=cv,
                                                scoring=scoring,
                                                n_jobs=n_jobs,
                                                verbose=verbose)
    train_scores_mean = np.mean(train_scores, axis=1)
    train_scores_std = np.std(train_scores, axis=1)
    test_scores_mean = np.mean(test_scores, axis=1)
    test_scores_std = np.std(test_scores, axis=1)

    plt.figure()
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.ylim(0.0, 1.1)
    lw = 2

    if plot_std:
        plt.fill_between(param_range, train_scores_mean - train_scores_std,
                         train_scores_mean + train_scores_std, alpha=0.2,
                         color="darkorange", lw=lw)
        plt.fill_between(param_range, test_scores_mean - test_scores_std,
                         test_scores_mean + test_scores_std, alpha=0.2,
                         color="navy", lw=lw)

    plt.semilogx(param_range, train_scores_mean, label="Training score",
                 color="darkorange", lw=lw)
    plt.semilogx(param_range, test_scores_mean, label="Cross-validation score",
                 color="navy", lw=lw)
    plt.legend(loc="best")
    return plt

def plot_roc_curve(y_true,
                y_score,
                pos_label=None,
                sample_weight=None):
    fpr, tpr, _ = roc_curve(y_true, y_score, pos_label=pos_label, sample_weight=sample_weight)

    plt.figure()
    plt.title('Receiver Operating Characteristic')
    plt.plot(fpr, tpr)
    plt.plot([0, 1], ls="--")
    plt.plot([0, 0], [1, 0] , c=".7")
    plt.plot([1, 1] , c=".7")
    plt.ylabel('True Positive Rate')
    plt.xlabel('False Positive Rate')

    return plt

def eval_threshold(threshold,
                    y_true,
                    y_score):
    fpr, tpr, thresholds = roc_curve(y_true, y_score)
    print('Sensitivity (REC):', tpr[thresholds > threshold][-1])
    print('Specificity:', tnr[thresholds > threshold][-1])

def plot_precision_recall_vs_threshold(precisions,
                                    recalls,
                                    thresholds,
                                    actual_threshold=0):
    plt.figure()
    plt.plot(thresholds, precisions[:-1], "b--", label="Precision")
    plt.plot(thresholds, recalls[:-1], "g-", label="Recall")
    plt.xlabel("Discrimination threshold")
    plt.legend(loc="lower left")
    plt.ylim([0, 1.05])
    plt.vlines(x=actual_threshold, ymin=0, ymax=1, linestyles='--')
    return plt

def plot_precision_recall_curve(precisions, recalls, thresholds, t=0, fill_area=True):
    plt.figure()
    # In matplotlib < 1.5, plt.fill_between does not have a 'step' argument
    # step_kwargs = ({'step': 'post'}
    #                if 'step' in signature(plt.fill_between).parameters
    #                else {})
    plt.step(recalls, precisions, color='b', where='post')
    # plt.plot(recalls, precisions, color='b')
    if fill_area:
        plt.fill_between(recalls, precisions, alpha=0.2, color='b')

    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.ylim([0.0, 1.08])
    plt.xlim([0.0, 1.0])
    plt.title('Precision-Recall curve')

    # plot the current threshold on the line
    close_default_clf = np.argmin(np.abs(thresholds - t))
    # plt.scatter(recalls[close_default_clf],
    #             precisions[close_default_clf],
    #             marker='o')
    # plt.annotate(t, (recalls[close_default_clf], precisions[close_default_clf]))
    plt.plot(recalls[close_default_clf], precisions[close_default_clf], 'o', c='k',
            markersize=5)
    plt.text(recalls[close_default_clf]+.02, precisions[close_default_clf]+.02, t)
    # plt.text(recalls[close_default_clf],
    #         precisions[close_default_clf],
    #         t,
    #         horizontalalignment='center',
    #         verticalalignment='center',
    #         transform=plt.transAxes)
    return plt

def plot_validation_curves(estimator,
                            X,
                            y,
                            param_name,
                            param_range,
                            cv,
                            scoring='accuracy',
                            n_jobs=-1,
                            verbose=1):
    # Calculate accuracy on training and test set using range of parameter values
    train_scores, test_scores = validation_curve(estimator=estimator,
                                                 X=X,
                                                 y=y,
                                                 param_name=param_name,
                                                 param_range=param_range,
                                                 cv=cv,
                                                 scoring=scoring,
                                                 n_jobs=n_jobs,
                                                 verbose=verbose)


    # Calculate mean and standard deviation for training set scores
    train_mean = np.mean(train_scores, axis=1)
    train_std = np.std(train_scores, axis=1)

    # Calculate mean and standard deviation for test set scores
    test_mean = np.mean(test_scores, axis=1)
    test_std = np.std(test_scores, axis=1)

    # Plot mean accuracy scores for training and test sets
    plt.plot(param_range, train_mean, label="Training score", color="black")
    plt.plot(param_range, test_mean, label="Cross-validation score", color="dimgrey")

    # Plot accurancy bands for training and test sets
    plt.fill_between(param_range, train_mean - train_std, train_mean + train_std, color="gray")
    plt.fill_between(param_range, test_mean - test_std, test_mean + test_std, color="gainsboro")

    # Create plot
    plt.figure()
    plt.title('Validation curves')
    plt.xlabel(param_name)
    plt.ylabel('Score')
    plt.tight_layout()
    plt.legend(loc="best")
    return plt

def adjusted_classes(y_scores, t):
    """
    This function adjusts class predictions based on the prediction threshold (t).
    Will only work for binary classification problems.
    """
    return [1 if y >= t else 0 for y in y_scores]

def precision_recall_threshold(precisions, recalls, thresholds, y_scores, y_test, t=0.5, fill_area=True):
    """
    plots the precision recall curve and shows the current value for each
    by identifying the classifier's threshold (t).
    """

    # generate new class predictions based on the adjusted_classes
    # function above and view the resulting confusion matrix.
    y_pred_adj = adjusted_classes(y_scores, t)
    print(confusion_matrix(y_test, y_pred_adj))

    # plot the curve
    plot_precision_recall_curve(precisions, recalls, thresholds, t, fill_area=fill_area)
