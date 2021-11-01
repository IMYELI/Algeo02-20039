import src.eigen as eig
import eigen_backup as eigb
import numpy as np
import time

A = np.array([[3,1,1],[-1,3,1]])
A = np.random.randint(0, 255, (1000, 1000))

start_time = time.time()
mat = np.dot(A, A.T)

eig_vals = eig.get_eigen_values(mat)
eig_val_time = time.time() - start_time
print(eig_val_time, "seconds for eigen values")

eig_vecs = eig.get_eigen_vectors(mat, eig_vals)
print(time.time() - start_time - eig_val_time, "seconds for eigen vectors")

np.savetxt("real_eig_vecs.txt", np.linalg.eig(mat)[1].T[1])
#np.savetxt("null_eig_vecs.txt", eigb.get_eigen_vectors_backup(mat, eig_vals)[4])
np.savetxt("results.txt", eig_vecs[1])
