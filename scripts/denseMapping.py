import numpy as np 

def propogateMatches(seeds, radius):
    map = []

    while len(seeds) != 0:
        pass
    return map

def getPatch(img, center, size):
    x, y = center
    pad = int(np.floor(size/2))
    patch = img[y-pad:y+pad+1, x-pad:x+pad+1]
    return np.asarray(patch)


def calcS(pos, img):
    directions = [[1, 0], [-1, 0], [0, 1], [0, -1]]
    gradients = np.empty(4)
    x, y = pos

    # calc gradients in 4 directions
    i = 0
    for dirr in directions:
        dX, dY = pos + dirr
        gradients[i] = img[x][y] - img[dX][dY]
        i += 1
    return np.max(gradients) # return the biggest gradient

def zncc(window1, window2):
    win1 = window1.flatten()
    win2 = window2.flatten()

    # compute avgs
    avg1 = np.mean(win1)
    avg2 = np.mean(win2)
    
    # compute std
    std1 = np.std(win1)
    std2 = np.std(win2)

    corr = 0
    for i in range(win1.shape[0]):
        corr += (win1[i] - avg1)*(win2[i] - avg2)
    
    corr /= (std1*std2)
    return corr 

if __name__ == "__main__":
    arr = [[1,2,3], [4,5,6], [7,8,9]]

    patch = getPatch(np.asarray(arr), (1,1), 3)
    print(patch)
    pass