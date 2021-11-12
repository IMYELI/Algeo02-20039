import numpy as np
import base64
from PIL import Image
import eigen
import io
from imageio import imread

def openImage(imgOriginal):
    #imgOriginal = Image.open(imgPath)
    #im = np.array(imgOriginal)
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
    decodedImage = base64.b64decode(image)
    imageInput = Image.open(io.BytesIO(decodedImage))
    channels, alpha, hasAlpha, original, bands = openImage(imageInput)
    r = int(np.linalg.matrix_rank(channels[0]) * (percentage * 0.01))

    print(f"r = {r}")

    compressedChannels = []
    for channel in channels:
        compressedChannels.append(compressSingleChannel(channel, r))


    compressedImageChannels = []
    for compressedChannel in compressedChannels:
        compressedImageChannels.append(Image.fromarray(compressedChannel, mode=None))

    #if hasAlpha:
        #compressedImageChannels.append(alpha)

    
    newImage = Image.merge('RGB', tuple(compressedImageChannels))
    #newImage.save(imageName +"compressed"+str(r)+imageExt)
    newImage.save("temp.jpg")
    image_read = open("temp.jpg", "rb").read()
    
    return str(base64.b64encode(image_read)).split('\'')[1]


if __name__ == "__main__":
    with open('Cgokngocok.txt') as f:
        lines = f.readlines()
    base64img = lines[0]
    splitedbase64img = base64img.split(',', 1)
    img = splitedbase64img[1]
    #print(img)
    newImage = compressImage(img, 20)
    
    print(splitedbase64img[0], end="")
    print(',', end="")
    print(newImage)

    f = open("b64.txt", "w")
    f.write(str(newImage))
    f.close()

    decodedImage = base64.b64decode(newImage)
    imageInput = Image.open(io.BytesIO(decodedImage))
    imageInput.save("zzz.jpg")
