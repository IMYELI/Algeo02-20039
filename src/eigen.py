# Library untuk menghitung nilai-nilai dan vektor-vektor eigen sebuah matrix

# Mengimport library numpy untuk berbagai fungsi matrix
# Juga fungsi hessenberg dan invert matrix dari scipy
import numpy as np
from scipy.linalg import hessenberg, inv

# Fungsi untuk mendapatkan nilai-nilai eigen dari suatu matriks
# Input adalah suatu matrix dalan bentuk numpy.array
# Output adalah numpy.array berisi nilai-nilai eigen
# Perhitungan dilakukan dengan menggunakan algoritma QR
def get_eigen_values(matrix):
    # Untuk mempercepat algoritma, matrix diubah ke bentuk hessenberg terlebih dahulu
    hess_mat = hessenberg(matrix)
    # Simpan ukuran matrix
    m_size, a = hess_mat.shape
    # Iterasi algoritma QR dimana matrix A didekomposisi menjadi QR, lalu A = R*Q
    # Iterasi dilakukan (10000/(ukuran matrix)) kali
    a_mat = hess_mat
    for i in range(np.rint(10000/m_size).astype(int)):
        (q, r) = np.linalg.qr(a_mat)    # Dekomposisi QR
        a_mat = np.dot(r, q)            # Iterasi matrix = R*Q
    # Nilai-Nilai eigen berada pada diagonal hasil iterasi QR
    eigen_vals_raw = np.diag(a_mat)
    # Nilai-Nilai eigen diurut dari besar ke kecil
    eigen_vals = eigen_vals_raw[np.argsort(-eigen_vals_raw)]
    # Mengembalikan np.array berisi nilai-nilai eigen
    return eigen_vals

# Fungsi untuk mendapatkan vektor-vektor eigen dari suatu matriks
# Input adalah suatu matrix dalan bentuk numpy.array dan numpy.array nilai-nilai eigen matrix tsb.
# Output adalah numpy.array berisi array vektor-vektor eigen
# Vektor eigen didapatkan dengan memasukkan nilai eigen ke dalam shifted inverse power method
def get_eigen_vectors(matrix, eig_vals):
    # Menyimpan ukuran matrix
    m_size, m_size = matrix.shape
    # Membuat list python untuk menampung hasil
    eig_vectors_py = []
    # Membuat matriks 1D b sepanjang matrix yang berisi angka 1
    b = np.ones(m_size)
    # Membuat matriks identitas sebesar matrix
    identity = np.identity(m_size)
    # Mencari vektor eigen untuk setiap nilai eigen matrix
    for eig_val in eig_vals:
        # Rumus shifted inverse power method
        elmt = np.dot(inv(matrix - (eig_val * identity)), b)
        eig_vector = elmt / np.linalg.norm(elmt)
        # Menambahkan vektor eigen ke dalam list hasil
        eig_vectors_py.append(eig_vector)
    # Convert list python hasil menjadi numpy.array
    eig_vectors = np.array(eig_vectors_py)
    # Mengembalikan np.array berisi vektor-vektor eigen
    return eig_vectors

