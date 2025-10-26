import numpy as np

def to_decimal(x):
    s = np.asarray(x, dtype='float64')
    return np.where(s>20, 1.0 + s/100.0, np.where(s<=1.0, 1.0/np.clip(s,1e-9,None), s))
