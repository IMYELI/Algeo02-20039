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

# Fungsi untuk mendapatkan nilai-nilai dan vektor-vektor eigen dari suatu matriks sekaligus
# Input adalah suatu matrix dalan bentuk numpy.array
# Output adalah tuple dengan suatu numpy.array berisi nilai-nilai eigen dan suatu numpy.array berisi array vektor-vektor eigen
# Metode yang digunakan adalah Orthogonal Iteration, suatu ekstensi dari Power Method
def get_eigen(mat):
    # Menyimpan ukuran matriks
    n, m = mat.shape
    # Inisialisasi matriks Q sesuai ukuran dan berisi random
    q = np.random.rand(n, m)
    # Lakukan QR decomposition terhadap matriks random untuk mendapat initial Q matrix yang sesuai
    q, r = np.linalg.qr(q)
    # Menyimpan dimensi matriks terbesar
    max_shape = max(n,m)
    # Menentukan toleransi error dari hasil untuk mengehentikan iterasi di saat yang tepat
    # Error dihitung berdasarkan ukuran matriks dimana berlaku 4*e^max_shape untuk < 1000 dan 10^(max_shape/1000) untuk sisanya.
    # Error ini sangat krusial untuk mengoptimalkan algoritma agar tidak melakukan terlalu sedikit atau terlalu banyak iterasi.
    error = (2 * np.exp(0.01 * max_shape)) if (max_shape <= 1000) else (10 ** (4 + (max_shape / 1000)))
    # Menyimpan Matriks r untuk perbandingan
    r_prev = r
    # Melakukan iterasi pertama
    dot = np.dot(mat, q)
    q, r = np.linalg.qr(dot)
    # Bandingkan matriks R yang berisi nilai eigen dengan iterasi sebelumnya
    diff = np.abs((r - r_prev).sum())
    # Bandingkan selisih dengan error yang ditoleransi
    while (diff > error) :
        # Melakukan iterasi selanjutnya
        r_prev = r
        dot = np.dot(mat, q)
        q, r = np.linalg.qr(dot)
        # Bandingkan kembali dengan iterasi sebelumnya
        diff = np.abs((r - r_prev).sum())
    # Mengembalikan nilai eigen dalam diagonal matriks R dan vektor eigen yang merupakan kolom-kolom matriks Q
    return np.diag(r), q