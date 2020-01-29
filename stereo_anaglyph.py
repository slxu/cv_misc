# code copy and modified from
# https://groups.google.com/d/msg/hive76-discussion/oM2H0v-I9xo/MHrJsI7HoVUJ
#
import numpy as np
import cv2

# declare various color blending algorithms to mix te pixels
# from different perspectives so that red/blue lens glasses
# make the image look 3D
color_blending = {
    'true': [ [ 0.299, 0.587, 0.114, 0, 0, 0, 0, 0, 0 ], [ 0, 0, 0, 0, 0, 0, 0.299, 0.587, 0.114 ] ],
    'mono': [ [ 0.299, 0.587, 0.114, 0, 0, 0, 0, 0, 0 ], [ 0, 0, 0, 0.299, 0.587, 0.114, 0.299, 0.587, 0.114 ] ],
    'color': [ [ 1, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, 0, 0, 0, 1, 0, 0, 0, 1 ] ],
    'halfcolor': [ [ 0.299, 0.587, 0.114, 0, 0, 0, 0, 0, 0 ], [ 0, 0, 0, 0, 1, 0, 0, 0, 1 ] ],
    'optimized': [ [ 0, 0.7, 0.3, 0, 0, 0, 0, 0, 0 ], [ 0, 0, 0, 0, 1, 0, 0, 0, 1 ] ],
}

# make_anaglyph_BGR is a routine that blends two
# perspectives into a single image that will be perceived as
# 3d when using red/blue glasses
# it accepts:
#   leftImage -- an image that corresponds to the left eye
#   rightImage -- an image that corresponds to the right eye
#   color -- a string that specifies a blending strategy by indexing into color_blending
#   result -- an image buffer that will hold the resulting image
# Note that make_make_anaglyph_BGR presumes that the image is in BGR format
def make_anaglyph_BGR(leftImage, rightImage, color, result):
    # use the color argument to select a color separation formula from color_blending
    m = color_blending[color]

    # split the left and right images into separate blue, green and red images
    lb,lg,lr = cv2.split(np.asarray(leftImage[:,:]))
    rb,rg,rr = cv2.split(np.asarray(rightImage[:,:]))
    resultArray = np.asarray(result[:,:])
    resultArray[:,:,0] = lb*m[0][6] + lg*m[0][7] + lr*m[0][8] + rb*m[1][6] + rg*m[1][7] + rr*m[1][8]
    resultArray[:,:,1] = lb*m[0][3] + lg*m[0][4] + lr*m[0][5] + rb*m[1][3] + rg*m[1][4] + rr*m[1][5]
    resultArray[:,:,2] = lb*m[0][0] + lg*m[0][1] + lr*m[0][2] + rb*m[1][0] + rg*m[1][1] + rr*m[1][2]

def main():
  # create to camera capture objects
  left = cv2.imread("data/tsukuba_left.png", cv2.IMREAD_COLOR)
  right = cv2.imread("data/tsukuba_right.png", cv2.IMREAD_COLOR)

  # make a named window to hold the resulting anaglyphic image
  cv2.namedWindow ("anaglyph")

  anaglyph = np.zeros(left.shape, np.uint8)

  # select an anaglyph color separation strategy
  colorMatrix = 'optimized'

  # make an anaglyph (note that we presume the image is in BGR format)
  make_anaglyph_BGR(left, right, colorMatrix, anaglyph)

  cv2.imwrite('data/tsukuba_anaglyph.png', np.asarray(anaglyph[:,:]))

  # display the anaglyph image
  cv2.imshow("anaglyph", anaglyph);
  cv2.waitKey()

if __name__=="__main__":
  main()

