from sklearn.pipeline import Pipeline
from sklearn.preprocessing import RobustScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer

NUMERIC_FEATURES = [
    'GrLivArea', 'TotalBsmtSF', 'LotArea', 'GarageArea',
    'OverallQual', 'OverallCond', 'YearBuilt', 'BedroomAbvGr',
    'FullBath', 'GarageCars', 'TotalSF', 'HouseAge',
    'WasRemodeled', 'QualCondScore', 'TotalBaths', 'QualAge'
]

CATEGORICAL_FEATURES = ['Neighborhood', 'BldgType', 'HouseStyle', 'SaleCondition']

numeric_pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', RobustScaler())
])

categorical_pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('encoder', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
])

preprocessor = ColumnTransformer([
    ('num', numeric_pipeline, NUMERIC_FEATURES),
    ('cat', categorical_pipeline, CATEGORICAL_FEATURES)
])