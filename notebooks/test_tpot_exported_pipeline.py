import numpy as np
import pandas as pd
from sklearn.ensemble import ExtraTreesRegressor, GradientBoostingRegressor, RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline, make_union
from tpot.builtins import StackingEstimator
from sklearn.preprocessing import FunctionTransformer
from copy import copy

# NOTE: Make sure that the outcome column is labeled 'target' in the data file
tpot_data = pd.read_csv('PATH/TO/DATA/FILE', sep='COLUMN_SEPARATOR', dtype=np.float64)
features = tpot_data.drop('target', axis=1)
training_features, testing_features, training_target, testing_target = \
            train_test_split(features, tpot_data['target'], random_state=None)

# Average CV score on the training set was: -873.5371544595959
exported_pipeline = make_pipeline(
    make_union(
        FunctionTransformer(copy),
        FunctionTransformer(copy)
    ),
    StackingEstimator(estimator=ExtraTreesRegressor(bootstrap=False, max_features=0.35000000000000003, min_samples_leaf=1, min_samples_split=13, n_estimators=100)),
    StackingEstimator(estimator=GradientBoostingRegressor(alpha=0.85, learning_rate=0.01, loss="lad", max_depth=4, max_features=0.9000000000000001, min_samples_leaf=8, min_samples_split=9, n_estimators=100, subsample=0.05)),
    RandomForestRegressor(bootstrap=True, max_features=0.25, min_samples_leaf=2, min_samples_split=2, n_estimators=100)
)

exported_pipeline.fit(training_features, training_target)
results = exported_pipeline.predict(testing_features)
