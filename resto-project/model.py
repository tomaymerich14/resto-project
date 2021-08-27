#SKLEARN
from sklearn.linear_model import Ridge, Lasso, LinearRegression
from sklearn.ensemble import GradientBoostingRegressor
from scipy import stats
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.compose import ColumnTransformer, make_column_transformer, make_column_selector
from sklearn.impute import SimpleImputer, KNNImputer
from sklearn.preprocessing import RobustScaler, OneHotEncoder, OrdinalEncoder
from sklearn.metrics import make_scorer
from sklearn.model_selection import cross_val_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import Ridge, Lasso, LinearRegression
from sklearn.model_selection import RandomizedSearchCV
from sklearn.svm import SVR
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
from sklearn.ensemble import AdaBoostRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import VotingRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.ensemble import StackingRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.inspection import permutation_importance



def model_selection(model_name):
    if model_name == 'Ridge':
        model_test = Ridge()

    if model_name == 'GradientBoostingRegressor':
        model_test = GradientBoostingRegressor(n_estimators=200, verbose=0, max_depth=5, learning_rate=0.05)

    if model_name == 'Stacked':
        gboost = GradientBoostingRegressor(n_estimators=100)
        ridge = Ridge()
        svm = SVR(C=1, epsilon=0.05)
        adaboost = AdaBoostRegressor(base_estimator=DecisionTreeRegressor(max_depth=None))


        model = VotingRegressor(
            estimators = [("gboost", gboost),("adaboost", adaboost),("ridge", ridge), ("svm_rbf", svm)],
            weights = [1,1,1,1], # to equally weight the two models
            n_jobs=-1
        )

    return model_test
