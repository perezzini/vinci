import numpy as np
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import cross_val_score
from ml import model_evaluation

def best_estimator(estimator,
                    X_train,
                    y_train,
                    cv,
                    param_grid,
                    scoring='accuracy',
                    n_jobs=-1,
                    verbose=1):
    """
    Hyperparameters optimization: finds optimal hyperparameters combination
    using CV
    """
    grid = GridSearchCV(estimator=estimator,
                        param_grid=param_grid,
                        scoring=scoring,
                        n_jobs=n_jobs,
                        cv=cv,
                        verbose=verbose)
    grid.fit(X_train, y_train)

    print('# Best estimator stats optimized for', scoring, ':')
    print()
    print('Best index:', grid.best_index_)
    print()
    print('CV scores for each search done:', grid.cv_results_['mean_test_score'])
    print()
    print("CV score for the best estimator found: %0.5f (std %0.5f)" % (grid.best_score_, grid.cv_results_['std_test_score'][grid.best_index_]))
    print()
    print('Best params found:', grid.best_params_)

    return grid

def plot_grid_search(cv_results,
                    grid_param_1,
                    grid_param_2,
                    name_param_1,
                    name_param_2):
    # Get Test Scores Mean and std for each grid search
    scores_mean = cv_results['mean_test_score']
    scores_mean = np.array(scores_mean).reshape(len(grid_param_2),len(grid_param_1))

    scores_sd = cv_results['std_test_score']
    scores_sd = np.array(scores_sd).reshape(len(grid_param_2),len(grid_param_1))

    # Plot Grid search scores
    _, ax = plt.subplots(1,1)

    # Param1 is the X-axis, Param 2 is represented as a different curve (color line)
    for idx, val in enumerate(grid_param_2):
        ax.plot(grid_param_1, scores_mean[idx,:], '-o', label= name_param_2 + ': ' + str(val))

    ax.set_title("Grid Search Scores", fontsize=20, fontweight='bold')
    ax.set_xlabel(name_param_1, fontsize=16)
    ax.set_ylabel('CV Average Score', fontsize=16)
    ax.legend(loc="best", fontsize=15)
    ax.grid('on')

    return plt

def nested_cv(estimator,
            X,
            y,
            param_grid,
            scoring='accuracy',
            inner_cv=2,
            outer_cv=5,
            n_jobs=-1,
            verbose=1):
    """
    Returns average cross-validation accuracy. This gives us a good estimate of what
    to expect if we tune the hyperparameters of the estimator and then use it on unseen data.
    """
    grid = GridSearchCV(estimator=estimator,
                        param_grid=param_grid,
                        scoring=scoring,
                        cv=inner_cv,
                        verbose=verbose)
    scores = cross_val_score(grid,
                            X,
                            y,
                            scoring=scoring,
                            cv=outer_cv)

    return np.mean(scores), np.std(scores)
