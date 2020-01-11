#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import pandas_profiling as pp

train_data = pd.read_csv('./input/house-prices-advanced-regression-techniques/train.csv')

data  = train_data.copy()

data.info()

data.describe()

data.head()

any(data.isnull())

# isnull result is showing us that columnns Alley(91), FireplaceQu(770), PoolQC(7), Fence(281), MiscFeature(54)
# have missing data ranging from 50%-96%

# Hence droping columns Alley, PoolQC, Fence, MiscFeature
data = data.drop(['Alley', 'PoolQC', 'Fence', 'MiscFeature'], axis = 1) 


# In[2]:


# Impute LotFrontageMedian
mLotFrontageMedian = data.LotFrontage.median(skipna=True)
data["LotFrontage"].fillna(value=mLotFrontageMedian, inplace=True)

# Impute MasVnrArea
mMasVnrAreaMedian = data.MasVnrArea.median(skipna=True)
data["MasVnrArea"].fillna(value=mMasVnrAreaMedian, inplace=True)


# Impute GarageYrBlt
mGarageYrBltMedian = data.GarageYrBlt.median(skipna=True)
data["GarageYrBlt"].fillna(value=mGarageYrBltMedian, inplace=True)

# Extract all numeric columns
num_data = (data.select_dtypes(include = ['int64', 'float64']))

num_cols = list(num_data)
print("Has any Missing Values? \n")
for col in num_cols:
    print(col, ": ", any(num_data[col].isnull()))

data.profile_report()
# In[3]:


# As per above Correlation matrix the following list of columns are not correlated with Target variable: SalePrice
# Hence drop-ing them

data = data.drop(['3SsnPorch', 'MiscVal', 'MoSold', 'YrSold', 'BsmtHalfBath', 'BsmtFinSF2', 'LowQualFinSF', 'Id'], axis = 1)

list(data)


# In[4]:


# Imputing Categorical Values

cat_data = data.select_dtypes(include=['object'])

cat_data.fillna('UNKNOWN', inplace=True)

cat_cols = list(cat_data)

print("Has any Missing Values? \n")
for col in cat_cols:
    print(col, ": ", any(cat_data[col].isnull()))
    


# In[5]:


# Import label encoder 
from sklearn import preprocessing 
  
# label_encoder object knows how to understand word labels. 
label_encoder = preprocessing.LabelEncoder() 
  
    
# Encode labels for all the nominal-value columns

columns = [
        'MSZoning', 'Street', 'LotShape', 'LandContour', 'Utilities', 'LotConfig', 'LandSlope',
        'Neighborhood', 'Condition1', 'Condition2', 'BldgType', 'HouseStyle', 'RoofStyle', 'RoofMatl',
        'Exterior1st', 'Exterior2nd', 'MasVnrType', 'Foundation', 'BsmtExposure',
        'BsmtFinType1', 'BsmtFinType2', 'Heating', 'CentralAir',
        'Electrical', 'Functional', 'GarageType', 'GarageFinish',
        'PavedDrive', 'SaleType', 'SaleCondition']

data_nominal = pd.DataFrame(columns = columns)

for col in columns:
    # print(cat_data[col].unique())
    data_nominal[col] = label_encoder.fit_transform(cat_data[col]) 
  
list(cat_data)


data = data.drop([
        'MSZoning', 'Street', 'LotShape', 'LandContour', 'Utilities', 'LotConfig', 'LandSlope',
        'Neighborhood', 'Condition1', 'Condition2', 'BldgType', 'HouseStyle', 'RoofStyle', 'RoofMatl',
        'Exterior1st', 'Exterior2nd', 'MasVnrType', 'Foundation', 'BsmtExposure',
        'BsmtFinType1', 'BsmtFinType2', 'Heating', 'CentralAir',
        'Electrical', 'Functional', 'GarageType', 'GarageFinish',
        'PavedDrive', 'SaleType', 'SaleCondition'], axis = 1)

data = pd.concat([data, data_nominal], axis = 1)

list(data)


# ONE HOT ENCODING
enc_cat_data = pd.get_dummies(
    cat_data, columns = [
        'MSZoning', 'Street', 'LotShape', 'LandContour', 'Utilities', 'LotConfig', 'LandSlope',
        'Neighborhood', 'Condition1', 'Condition2', 'BldgType', 'HouseStyle', 'RoofStyle', 'RoofMatl',
        'Exterior1st', 'Exterior2nd', 'MasVnrType', 'Foundation', 'BsmtExposure',
        'BsmtFinType1', 'BsmtFinType2', 'Heating', 'CentralAir',
        'Electrical', 'Functional', 'GarageType', 'GarageFinish',
        'PavedDrive', 'SaleType', 'SaleCondition']
)

list(data)


data = data.drop([
        'MSZoning', 'Street', 'LotShape', 'LandContour', 'Utilities', 'LotConfig', 'LandSlope',
        'Neighborhood', 'Condition1', 'Condition2', 'BldgType', 'HouseStyle', 'RoofStyle', 'RoofMatl',
        'Exterior1st', 'Exterior2nd', 'MasVnrType', 'Foundation', 'BsmtExposure',
        'BsmtFinType1', 'BsmtFinType2', 'Heating', 'CentralAir',
        'Electrical', 'Functional', 'GarageType', 'GarageFinish',
        'PavedDrive', 'SaleType', 'SaleCondition'], axis = 1)

data = pd.concat([data, enc_cat_data], axis = 1)

list(data)

# In[6]:


ordinalColNames = ['ExterQual', 'ExterCond', 'BsmtQual', 'BsmtCond', 'HeatingQC', 'KitchenQual', 'FireplaceQu', 'GarageQual', 'GarageCond']

# ['TA' 'Fa' nan 'Gd' 'Po' 'Ex']

# Create mapper
scale_mapper = {'Ex': 5, 
                'Gd': 4,
                'TA': 3,
                'Fa': 2,
                'Po': 1,
                'UNKNOWN': 0
               }
# Map feature values to scale
for col in ordinalColNames :
    data[col] = data[col].replace(scale_mapper)
    #print(data[col])
    
len(list(data))


# In[ ]:





# In[13]:


# Scaling the data using Standardization

from sklearn.preprocessing import StandardScaler

# Initialise the Scaler 
scaler = StandardScaler()
  
# To scale data 
data_std = pd.DataFrame(scaler.fit_transform(data), columns = list(data))

data_std.head()


# In[14]:


# Train Test 

y = data.SalePrice

X = data_std.drop(['SalePrice'], axis = 1) 

from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
X_train, X_test, y_train, y_test = train_test_split(X,y, test_size = 0.3, random_state = 42)

print(X_train)
print(X_test)
print(y_train)
print(y_test)


# In[ ]:





# In[ ]:


from sklearn.neighbors import KNeighborsClassifier
model = KNeighborsClassifier()
model.fit(X_train, y_train)

