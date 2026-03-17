"""
Generate a realistic synthetic house price dataset
mimicking Kaggle's House Prices dataset structure.
"""
import numpy as np
import pandas as pd
import json

np.random.seed(42)
N = 1460  # Same size as Kaggle dataset

neighborhoods = {
    'NoRidge': 1.35, 'NridgHt': 1.25, 'StoneBr': 1.30,
    'Timber':  1.10, 'Veenker': 1.08, 'Somerst': 1.05,
    'ClearCr': 1.02, 'Crawfor': 1.00, 'CollgCr': 0.98,
    'Blmngtn': 0.96, 'Gilbert': 0.95, 'NWAmes':  0.93,
    'SawyerW': 0.90, 'Mitchel': 0.88, 'NAmes':   0.85,
    'NPkVill': 0.83, 'SWISU':   0.80, 'Blueste': 0.78,
    'Sawyer':  0.78, 'OldTown': 0.75, 'Edwards': 0.73,
    'BrkSide': 0.72, 'Landmrk': 0.70, 'MeadowV': 0.68,
    'IDOTRR':  0.65, 'BrDale':  0.63
}

house_styles = ['1Story', '2Story', '1.5Fin', 'SFoyer', 'SLvl']
bldg_types   = ['1Fam', 'TwnhsE', 'Twnhs', '2fmCon', 'Duplex']
conditions   = ['Norm', 'Feedr', 'PosN', 'Artery', 'RRAe', 'RRNn', 'PosA', 'RRAn', 'RRNe']
qualities    = ['Ex', 'Gd', 'TA', 'Fa', 'Po']
quality_map  = {'Ex': 5, 'Gd': 4, 'TA': 3, 'Fa': 2, 'Po': 1}

df = pd.DataFrame()
df['Id']           = range(1, N+1)
df['Neighborhood'] = np.random.choice(list(neighborhoods.keys()), N, p=[1/len(neighborhoods)]*len(neighborhoods))
df['BldgType']     = np.random.choice(bldg_types,   N, p=[0.82,0.09,0.04,0.03,0.02])
df['HouseStyle']   = np.random.choice(house_styles, N, p=[0.50,0.30,0.11,0.05,0.04])
df['OverallQual']  = np.random.choice(range(1,11),  N, p=[0.01,0.01,0.02,0.04,0.06,0.15,0.24,0.28,0.12,0.07])
df['OverallCond']  = np.random.choice(range(1,10),  N, p=[0.01,0.01,0.05,0.04,0.18,0.40,0.19,0.09,0.03])
df['YearBuilt']    = np.random.randint(1872, 2011, N)
df['YearRemodAdd'] = df['YearBuilt'] + np.random.randint(0, 40, N)
df['YearRemodAdd'] = df['YearRemodAdd'].clip(upper=2010)

df['GrLivArea']    = (np.random.normal(1500, 400, N)).clip(400, 5000).astype(int)
df['TotalBsmtSF']  = (df['GrLivArea'] * np.random.uniform(0.3, 0.9, N)).clip(0, 3000).astype(int)
df['1stFlrSF']     = (df['GrLivArea'] * np.random.uniform(0.4, 0.7, N)).clip(200, 4000).astype(int)
df['2ndFlrSF']     = np.where(df['HouseStyle']=='2Story', (df['GrLivArea']*0.4).astype(int), 0)

df['BedroomAbvGr'] = np.random.choice([1,2,3,4,5], N, p=[0.03,0.18,0.52,0.22,0.05])
df['FullBath']     = np.random.choice([0,1,2,3],   N, p=[0.01,0.30,0.57,0.12])
df['HalfBath']     = np.random.choice([0,1,2],     N, p=[0.56,0.39,0.05])
df['TotRmsAbvGrd'] = df['BedroomAbvGr'] + df['FullBath'] + np.random.randint(1, 4, N)

df['GarageCars']   = np.random.choice([0,1,2,3,4], N, p=[0.06,0.22,0.58,0.12,0.02])
df['GarageArea']   = (df['GarageCars'] * np.random.normal(220, 40, N)).clip(0, 1400).astype(int)

df['LotArea']      = (np.random.lognormal(9.2, 0.5, N)).clip(1300, 215000).astype(int)
df['LotFrontage']  = (np.random.normal(70, 25, N)).clip(20, 200).astype(int)

df['ExterQual']    = np.random.choice(qualities, N, p=[0.08,0.38,0.49,0.04,0.01])
df['KitchenQual']  = np.random.choice(qualities, N, p=[0.07,0.40,0.48,0.04,0.01])
df['BsmtQual']     = np.random.choice(qualities + ['NA'], N, p=[0.10,0.42,0.39,0.04,0.01,0.04])

df['SaleCondition'] = np.random.choice(['Normal','Abnorml','Partial','AdjLand','Alloca','Family'],
                                        N, p=[0.82,0.07,0.07,0.01,0.01,0.02])
df['MoSold']       = np.random.choice(range(1,13), N)
df['YrSold']       = np.random.choice([2006,2007,2008,2009,2010], N, p=[0.18,0.22,0.22,0.22,0.16])

# --- Price formula (realistic) ---
nbhd_mult  = df['Neighborhood'].map(neighborhoods)
qual_score = df['OverallQual'] / 10
cond_score = df['OverallCond'] / 10
age_factor = 1 - (2010 - df['YearBuilt']) * 0.002
remod_bonus= np.where(df['YearRemodAdd'] > df['YearBuilt'], 0.05, 0)
ext_mult   = df['ExterQual'].map(quality_map) / 3
kit_mult   = df['KitchenQual'].map(quality_map) / 3
bsmt_q     = df['BsmtQual'].map({**quality_map, 'NA': 0}) / 3

base_price = (
    50000
    + df['GrLivArea']   * 75
    + df['TotalBsmtSF'] * 25
    + df['GarageArea']  * 50
    + df['LotArea']     * 0.5
    + df['OverallQual'] * 8000
    + df['GarageCars']  * 3000
    + df['FullBath']    * 4000
    + df['BedroomAbvGr']* 2500
)

price = (base_price
         * nbhd_mult
         * (0.6 + qual_score * 0.8)
         * (0.85 + cond_score * 0.3)
         * age_factor.clip(0.5, 1)
         * (1 + remod_bonus)
         * (0.7 + ext_mult * 0.6)
         * (0.75 + bsmt_q  * 0.5)
)

noise = np.random.normal(1, 0.06, N)
df['SalePrice'] = (price * noise).clip(34900, 755000).astype(int)

# Train / test split
train = df.sample(frac=0.8, random_state=42)
test  = df.drop(train.index).drop(columns=['SalePrice'])

train.to_csv('data/train.csv', index=False)
test.to_csv('data/test.csv',  index=False)

print(f"✅ Dataset created: {len(train)} train, {len(test)} test rows")
print(f"   Price range: ${train['SalePrice'].min():,} – ${train['SalePrice'].max():,}")
print(f"   Mean price : ${train['SalePrice'].mean():,.0f}")
