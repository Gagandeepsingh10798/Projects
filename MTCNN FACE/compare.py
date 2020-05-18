import cv2
import sys
from skimage.metrics import structural_similarity as ssim
import matplotlib.pyplot as plt
import numpy as np
import warnings
from skimage.measure import compare_ssim
from skimage.transform import resize
from scipy.stats import wasserstein_distance
import imageio


warnings.filterwarnings('ignore')

# specify resized image sizes
height = 2**10
width = 2**10

##
# Functions
##

def get_img(path, norm_size=True, norm_exposure=False):
  '''
  Prepare an image for image processing tasks
  '''
  # flatten returns a 2d grayscale array
  img = imageio.imread(path)
  # resizing returns float vals 0:255; convert to ints for downstream tasks
  if norm_size:
    img = resize(img, (height, width), anti_aliasing=True, preserve_range=True)
  if norm_exposure:
    img = normalize_exposure(img)
  return img


def get_histogram(img):
  '''
  Get the histogram of an image. For an 8-bit, grayscale image, the
  histogram will be a 256 unit vector in which the nth value indicates
  the percent of the pixels in the image with the given darkness level.
  The histogram's values sum to 1.
  '''
  h, w = img.shape
  hist = [0.0] * 256
  for i in range(h):
    for j in range(w):
      hist[img[i, j]] += 1
  return np.array(hist) / (h * w) 


def normalize_exposure(img):
  '''
  Normalize the exposure of an image.
  '''
  img = img.astype(int)
  hist = get_histogram(img)
  # get the sum of vals accumulated by each position in hist
  cdf = np.array([sum(hist[:i+1]) for i in range(len(hist))])
  # determine the normalization values for each unit of the cdf
  sk = np.uint8(255 * cdf)
  # normalize each position in the output image
  height, width = img.shape
  normalized = np.zeros_like(img)
  for i in range(0, height):
    for j in range(0, width):
      normalized[i, j] = sk[img[i, j]]
  return normalized.astype(int)


def earth_movers_distance(path_a, path_b):
  '''
  Measure the Earth Mover's distance between two images
  @args:
    {str} path_a: the path to an image file
    {str} path_b: the path to an image file
  @returns:
    TODO
  '''
  img_a = get_img(path_a, norm_exposure=True)
  img_b = get_img(path_b, norm_exposure=True)
  hist_a = get_histogram(img_a)
  hist_b = get_histogram(img_b)
  return wasserstein_distance(hist_a, hist_b)


def structural_sim(path_a, path_b):
  '''
  Measure the structural similarity between two images
  @args:
    {str} path_a: the path to an image file
    {str} path_b: the path to an image file
  @returns:
    {float} a float {-1:1} that measures structural similarity
      between the input images
  '''
  img_a = get_img(path_a)
  img_b = get_img(path_b)
  sim, diff = compare_ssim(img_a, img_b, full=True)
  return sim


def pixel_sim(path_a, path_b):
  '''
  Measure the pixel-level similarity between two images
  @args:
    {str} path_a: the path to an image file
    {str} path_b: the path to an image file
  @returns:
    {float} a float {-1:1} that measures structural similarity
      between the input images
  '''
  img_a = get_img(path_a, norm_exposure=True)
  img_b = get_img(path_b, norm_exposure=True)
  return np.sum(np.absolute(img_a - img_b)) / (height*width) / 255


def sift_sim(path_a, path_b):
  '''
  Use SIFT features to measure image similarity
  @args:
    {str} path_a: the path to an image file
    {str} path_b: the path to an image file
  @returns:
    TODO
  '''
  # initialize the sift feature detector
  orb = cv2.ORB_create()

  # get the images
  img_a = cv2.imread(path_a)
  img_b = cv2.imread(path_b)

  # find the keypoints and descriptors with SIFT
  kp_a, desc_a = orb.detectAndCompute(img_a, None)
  kp_b, desc_b = orb.detectAndCompute(img_b, None)

  # initialize the bruteforce matcher
  bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

  # match.distance is a float between {0:100} - lower means more similar
  matches = bf.match(desc_a, desc_b)
  similar_regions = [i for i in matches if i.distance < 70]
  if len(matches) == 0:
    return 0
  return len(similar_regions) / len(matches)

def mse(imageA, imageB):
    # the 'Mean Squared Error' between the two images is the
    # sum of the squared difference between the two images;
    # NOTE: the two images must have the same dimension
    # tuplu = imageA.shape
    # if tuplu[0] > tuplu[1]:
        # imageB = imageB.reshape(tuplu[1],tuplu[1])
    # else:
        # imageB = imageB.reshape(tuplu[0],tuplu[0])
    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])
    # return the MSE, the lower the error, the more "similar"
    # the two images are
    return err
 
def compare_images(imageA, imageB, img_as, img_bs,title):
	# compute the mean squared error and structural similarity
	# index for the images
    shape_of_A = imageA.shape
    shape_of_B = imageB.shape
    print(shape_of_A,shape_of_B)
    if shape_of_A[0] > shape_of_B[0]:
        print("a x is larger")
        columnss = []
        for i in range(shape_of_B[0],shape_of_A[0]):
            columnss.append(i)
        print(columnss)
        imageA = np.delete(imageA, columnss, axis=0)
        print(imageA.shape,imageB.shape)
    if shape_of_A[0] < shape_of_B[0]:
        print("b x is larger")
        columnss = []
        for i in range(shape_of_A[0],shape_of_B[0]):
            columnss.append(i)
        print(columnss)
        imageB = np.delete(imageB, columnss, axis=0)
        print(imageA.shape,imageB.shape)
    if shape_of_A[1] < shape_of_B[1]:
        print("b y is larger")
        columnss = []
        for i in range(shape_of_A[1],shape_of_B[1]):
            columnss.append(i)
        print(columnss)
        imageB = np.delete(imageB, columnss, axis=1)
        print(imageA.shape,imageB.shape)
    if shape_of_A[1] > shape_of_B[1]:
        print("a y is larger")
        columnss = []
        for i in range(shape_of_B[1],shape_of_A[1]):
            columnss.append(i)
        print(columnss)
        imageA = np.delete(imageA, columnss, axis=1)
        print(imageA.shape,imageB.shape)
    ss = structural_sim(img_as, img_bs)
    ps = pixel_sim(img_as, img_bs)
    sift = sift_sim(img_as, img_bs)
    emd = earth_movers_distance(img_as, img_bs)
    m = mse(imageA, imageB)
    s = ssim(imageA, imageB)
	# setup the figure
    fig = plt.figure(title)
    plt.suptitle("MSE: %.2f, SSIM: %.2f , ss: %.4f, ps: %.4f, sifts: %.4f,emd: %.4f" % (m, s*100,ss*100,ps*100,sift*100,emd*100))
    print(m,ss,"(1 honi chahiye) ", ps,"(0 honi chahiye)  ", sift,"(1 honi chahiye)  ", emd,"(0 honi chahiye)    ")
    # show first image
    ax = fig.add_subplot(1, 2, 1)
    plt.imshow(imageA, cmap = plt.cm.gray)
    plt.axis("off")
    # show the second image
    ax = fig.add_subplot(1, 2, 2)
    plt.imshow(imageB, cmap = plt.cm.gray)
    plt.axis("off")
    # show the images
    plt.show()



# load the images -- the original, the original + contrast,
# and the original + photoshop
img_as = 'face1.jpg'
img_bs = 'face1.jpg'
image1 = cv2.imread(img_as)
image2 = cv2.imread(img_bs)
image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
 
# compare the images
compare_images(image1, image2, img_as,img_bs,"a vs. b")