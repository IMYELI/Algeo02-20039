import numpy as np
import base64
from PIL import Image
import eigen
import io
from imageio import imread

# Fungsi untuk memecah channel gambar
def openImage(img):
    imgOriginal = img
    imgChannels = []
    bands = imgOriginal.getbands()
    if len(''.join(bands)) == 1:
        imgOriginal = imgOriginal.convert("RGBA")
        bands = imgOriginal.getbands()
    imgAlpha = np.nan
    hasAlphaValue = False

    # Mengambil channel setiap band
    for band in bands:
        if band == 'A':
            imgAlpha = imgOriginal.getchannel("A")
            hasAlphaValue = True
        else:
            imgChannels.append(imgOriginal.getchannel(band))

    return imgChannels, imgAlpha, hasAlphaValue, bands


# Fungsi untuk memecah gambar menggunakan metode SVD
def getSVDMatrices(m, rank):

    # Eksekusi berdasarkan yang lebih lebar di antara baris atau kolom
    mat = np.asarray(m).astype(float)
    r, c = np.shape(mat)
    if r < c:
        sqMat = mat @ mat.T
        AtransposexA = mat.T @ mat
    else :
        sqMat = mat.T @ mat
        AtransposexA = sqMat
    
    # Cari nilai eigen dan vektor eigen untuk matriks v
    eigenValue, eigenVectors = eigen.get_eigen(AtransposexA)
    eigenVectors = np.transpose(eigenVectors)
    s = np.sqrt(np.abs(eigenValue))
    u = []
    
    # Cari vektor eigen untuk matriks u
    for i in range(rank):
        u.append((np.dot(mat,eigenVectors[i].T))/s[i])
    u = np.array(u).T
    vt = eigenVectors

    return u, s, vt

# Fungsi untuk mengompres Matriks
def compressSingleChannel(channel, rank):
    # Eksekusi berdasarkan yang lebih lebar di antara baris atau kolom
    r, c = np.shape(channel)
    if r < c :
        channel = np.transpose(channel)

    # Panggil fungsi getSVDMatrices
    u, s, vt = getSVDMatrices(channel, rank)

    # Jadikan s matriks diagonal
    s = np.diag(s)

    # Komposisikan kembali matriks berdasarkan rank
    compressed = u[:,:rank] @ s[0:rank, :rank] @ vt[:rank, :]
    if r < c :
        compressed = np.transpose(compressed)

    return np.clip(compressed, 0, 255).astype('uint8')


def compressImage(image, percentage,imageName):
    # Ambil ekstensi gambar
    imageExt = '.' + imageName.split('.')[-1]

    # Decode dari base64
    decodedImage = base64.b64decode(image)
    imageInput = Image.open(io.BytesIO(decodedImage))

    # Pisahkan channel gambar
    channels, alpha, hasAlpha, bands = openImage(imageInput)
    r = int(np.linalg.matrix_rank(channels[0]) * (percentage * 0.01))

    print(f"r = {r}")

    # Gabungkan kembali channel gambar
    compressedChannels = []
    for channel in channels:
        compressedChannels.append(compressSingleChannel(channel, r))

    compressedImageChannels = []
    for compressedChannel in compressedChannels:
        compressedImageChannels.append(Image.fromarray(compressedChannel, mode=None))
        
    if len(compressedImageChannels) != 1 :
        if hasAlpha:
            compressedImageChannels.append(alpha)
            newImage = Image.merge(''.join(bands), tuple(compressedImageChannels))
            newImage = newImage.convert("P", palette=Image.ADAPTIVE)
            newImage.save("../vue/src/assets/test"+imageExt)
            return imageExt

        else :
            newImage = Image.merge(''.join(bands), tuple(compressedImageChannels))
            newImage.save("../vue/src/assets/test" + imageExt)
    else :
        newImage = compressedImageChannels[0]
        newImage = newImage.convert(bands[0])
        newImage.save("../vue/src/assets/test"+imageExt)

    return imageExt

    


    