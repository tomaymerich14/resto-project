from sklearn.model_selection import GridSearchCV, RepeatedKFold
from get_dataframe import get_XY, get_service
from model import model_selection
from sklearn.pipeline import make_pipeline
from tempfile import mkdtemp
import numpy as np
from numpy import mean
from numpy import std


cachedir = mkdtemp()

def grid_search(df, jour, service):
    data = get_service(df, jour, service)
    X = get_XY(data)[0]
    y = get_XY(data)[1]

    model = model_selection('XGB')

    preproc = Trainer.set_pipeline(model)

    param_grid = {
        'xgbregressor__max_depth': np.arange(1, 5, 1),
        'xgbregressor__n_estimators': np.arange(30, 50, 5),
        'xgbregressor__learning_rate': np.arange(0.05, 0.3, 0.05),
    }

    pipe_xgb = make_pipeline(preproc, model, memory=cachedir)

    search_pipe_xgb = GridSearchCV(pipe_xgb,
                                   param_grid=param_grid,
                                   cv=5,
                                   n_jobs=-1,
                                   verbose=2,
                                   scoring='neg_mean_absolute_error')

    search_pipe_xgb.fit(X, y)

    cv = RepeatedKFold(n_splits=5, n_repeats=5, random_state=0)
    n_scores = cross_val_score(search_pipe_xgb.best_estimator_,
                               X,
                               y,
                               cv=cv,
                               scoring='neg_mean_absolute_error',
                               n_jobs=-1)
    print(search_pipe_xgb.best_params_), print('MAE: %.3f (%.3f)' %
                                               (mean(n_scores), std(n_scores)))
    return search_pipe_xgb.best_estimator_, search_pipe_xgb.best_params_, search_pipe_xgb.best_score_
