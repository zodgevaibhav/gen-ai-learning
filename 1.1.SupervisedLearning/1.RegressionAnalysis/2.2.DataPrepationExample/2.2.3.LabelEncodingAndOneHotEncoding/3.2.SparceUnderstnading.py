from sklearn.preprocessing import OneHotEncoder
import numpy as np

data = np.array([["A"], ["B"], ["C"], ["A"]])

# Sparse output
enc_sparse = OneHotEncoder(sparse_output=True)
X_sparse = enc_sparse.fit_transform(data)
print(type(X_sparse)) 
print(X_sparse)

# Dense output
enc_dense = OneHotEncoder(sparse_output=False)
X_dense = enc_dense.fit_transform(data)
print(type(X_dense)) 
print(X_dense)
