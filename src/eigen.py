import numpy as np
from scipy.linalg import hessenberg

def getEigenValues(matrix) :
    hess_mat = hessenberg(matrix)
    m_size, a = hess_mat.shape

    a_mat = hess_mat
    for i in range(np.rint(10000/m_size).astype(int)):
        (q, r) = np.linalg.qr(a_mat)
        a_mat = np.dot(r, q)
    
    eigen_vals_raw = np.diag(a_mat)
    eigen_vals = eigen_vals_raw[np.argsort(-eigen_vals_raw)]

    return eigen_vals

