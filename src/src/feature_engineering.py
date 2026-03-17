def engineer_features(df):
    d = df.copy()
    
    # Total square footage
    d['TotalSF'] = d['GrLivArea'] + d['TotalBsmtSF']
    
    # Age of house
    d['HouseAge'] = 2010 - d['YearBuilt']
    
    # Was it remodeled?
    d['WasRemodeled'] = (d['YearRemodAdd'] > d['YearBuilt']).astype(int)
    
    # Combined quality signal
    d['QualCondScore'] = d['OverallQual'] * d['OverallCond']
    
    # Total bathrooms
    d['TotalBaths'] = d['FullBath'] + 0.5 * d['HalfBath']
    
    # Quality × Age interaction
    d['QualAge'] = d['OverallQual'] / (d['HouseAge'] + 1)
    
    return d

