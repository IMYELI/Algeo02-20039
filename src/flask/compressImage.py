import numpy as np
import base64
from PIL import Image
import eigen

def openImage(imgPath):
    imgOriginal = Image.open(imgPath)
    im = np.array(imgOriginal)
    imgChannels = []
    bands = imgOriginal.getbands()
    imgAlpha = np.nan
    hasAlphaValue = False
    for band in bands:
        if band == 'A':
            imgAlpha = imgOriginal.getchannel("A")
            hasAlphaValue = True
        else:
            imgChannels.append(imgOriginal.getchannel(band))

    return imgChannels, imgAlpha, hasAlphaValue, imgOriginal, bands


def getSVDMatrices(m, rank):
    mat = np.asarray(m).astype(float)
    r, c = np.shape(mat)
    if r < c:
        sqMat = mat @ mat.T
        AtransposexA = mat.T @ mat
    else :
        sqMat = mat.T @ mat
        AtransposexA = sqMat
    eigenValue, eigenVectors = eigen.get_eigen(AtransposexA)
    eigenVectors = np.transpose(eigenVectors)
    s = np.sqrt(np.abs(eigenValue))
    u = []
    
    for i in range(rank):
        u.append((np.dot(mat,eigenVectors[i].T))/s[i])
    u = np.array(u).T
    vt = eigenVectors

    return u, s, vt

def compressSingleChannel(channel, rank):
    r, c = np.shape(channel)
    if r < c :
        channel = np.transpose(channel)
    u, s, vt = getSVDMatrices(channel, rank)
    s = np.diag(s)
    compressed = u[:,:rank] @ s[0:rank, :rank] @ vt[:rank, :]
    if r < c :
        compressed = np.transpose(compressed)
    return np.clip(compressed, 0, 255).astype('uint8')


def compressImage(image, percentage):
    #imageInput = "misaka10032.jpg"
    #imageName = ''.join(imageInput.split('.')[:-1])
    #imageExt = '.' + imageInput.split('.')[-1]
    decodedImage = base64.decodebytes(image)
    imageInput = np.frombuffer(decodedImage, dtype=np.float64)
    channels, alpha, hasAlpha, original, bands = openImage(imageInput)
    row, col = np.shape(channels[0])
    r = min(row, col) // (percentage * 0.01)

    print(f"r = {r}")

    compressedChannels = []
    for channel in channels:
        compressedChannels.append(compressSingleChannel(channel, r))


    compressedImageChannels = []
    for compressedChannel in compressedChannels:
        compressedImageChannels.append(Image.fromarray(compressedChannel, mode=None))

    if hasAlpha:
        compressedImageChannels.append(alpha)

    
    newImage = Image.merge(''.join(bands), tuple(compressedImageChannels))
    #newImage.save(imageName +"compressed"+str(r)+imageExt)
    encodedImage = np.arange(newImage, dtype=np.float64)
    return base64.b64encode(encodedImage)

    