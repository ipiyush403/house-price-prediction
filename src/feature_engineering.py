
def engineer_features(df):
    d = df.copy()
    d['TotalSF']       = d['GrLivArea'] + d['TotalBsmtSF']
    d['HouseAge']      = 2010 - d['YearBuilt']
    d['WasRemodeled']  = (d['YearRemodAdd'] > d['YearBuilt']).astype(int)
    d['QualCondScore'] = d['OverallQual'] * d['OverallCond']
    d['TotalBaths']    = d['FullBath'] + 0.5 * d['HalfBath']
    d['QualAge']       = d['OverallQual'] / (d['HouseAge'] + 1)
    return d
