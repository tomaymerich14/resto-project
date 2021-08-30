from get_dataframe import get_service
from get_dataframe import get_XY
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import GridSearchCV
import numpy as np
from tempfile import mkdtemp
import trainer

cachedir = mkdtemp()

df = trainer.preproc_data_d2
jour = 'Lundi'
service = 'midi'
model_name = 'XGB'

param_grid = {
    'max_depth': np.arange(1, 10, 2),
    'n_estimators': np.arange(10, 60, 10),
    'learning_rate': np.arange(0.1, 0.5, 0.1),
}

### -> possible models =
# 0:'RIDGE', 1:'DUMMY', 2:'GBR', 3:'XGB', 4:'LGBM', 5:'CATB'


def grid_search(df, jour, service, model_name, param_grid):
    data = get_service(df, jour, service)
    X = get_XY(data)[0]
    y = get_XY(data)[1]

    model = model_name

    preproc = trainer.set_pipeline(model)

    pipe_xgb = make_pipeline(preproc, model, memory=cachedir)

    search_pipe = GridSearchCV(pipe_xgb,
                               param_grid=param_grid,
                               cv=5,
                               n_jobs=-1,
                               verbose=2,
                               scoring='neg_mean_absolute_error')

    search_pipe.fit(X, y)

    return search_pipe.best_estimator_, search_pipe.best_params_, search_pipe.best_score_
