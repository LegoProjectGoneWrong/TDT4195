from PIL import Image
from math import sqrt

# Takes a matrix of 3-tuples.
def to_gray_scale(pixels):
    return _to_gray_scale(pixels, lambda r, g, b: round((r+g+b) / 3))

def to_gray_scale_weighted(pixels):
    return _to_gray_scale(pixels, lambda r, g, b: round(0.2126*r + 0.7152 * g + 0.0722 * b))

def _to_gray_scale(pixels, averaging_function):
    return [[averaging_function(*pixel) for pixel in row] for row in pixels]

# Takes PIL Image, returns 2D list of pixels
def _image_to_matrix(img):
    return [[img.getpixel( (x, y)) for x in range(img.size[0])] for y in range(img.size[1])]

# Takes 2D list, returns by default gray scale image
def _matrix_to_image(pixels, mode = "P"):
    img = Image.new(mode, (len(pixels[0]), len(pixels)))

    for y in range(len(pixels[0])):
        for x in range(len(pixels)):
            img.putpixel((x,y), pixels[y][x])
    return img


def invert_image(img):
    pixels = _image_to_matrix(img)
    pixels_inverted = _simple_transformation(pixels, lambda p : 255 - p)

    img_inverted = _matrix_to_image(pixels_inverted)

    return img_inverted

def _simple_transformation(pixels, T):
    for y in range(len(pixels)):
        for x in range(len(pixels[y])):
            pixels[y][x] = T(pixels[y][x])
    return pixels

def normalize(pixels):
    return [[pixel / 255 for pixel in row] for row in pixels]

def to_spatial(pixels):
    return [[round(value * 255) for value in row] for row in pixels]

def gamma_transform(pixels, gamma):
    return _simple_transformation(pixels, lambda p : p ** gamma)

def convolution(pixels, kernel):
    get_pixel = lambda x, y : pixels[y][x] if 0 <= x < len(pixels[0]) and 0 <= y < len(pixels)  else 0
    dx = (len(kernel[0]) - 1) // 2
    dy = (len(kernel) - 1) // 2

    width = len(pixels[0])
    height = len(pixels)

    return [[int(sum(get_pixel(x-dx+j, y-dy+i)*kernel[i][j] for i in range(2*dy+1) for j in range(2*dx+1))) for x in range(width)] for y in range(height)]

if __name__ == "__main__":

    for filename in ["images/4.1.07-jelly-beans.tiff", "images/4.2.06-lake.tiff"]:
        # Task 2-1
        img = Image.open(filename)
        pixels = _image_to_matrix(img)

        pixels_gray = to_gray_scale(pixels)
        pixels_gray_weighted = to_gray_scale_weighted(pixels)

        img_gray = _matrix_to_image(pixels_gray)
        img_gray_weighted = _matrix_to_image(pixels_gray_weighted)

        img_gray.save(filename + " gray scale.bmp", "bmp")
        img_gray_weighted.save(filename + " gray scale weighted.bmp", "bmp")

        # Task 2-2a
        img_inverted = invert_image(img_gray_weighted)
        img_inverted.save(filename + " inverted.bmp", "bmp")

        # Task 2-3b
        h_a = [
                [1, 1, 1],
                [1, 1, 1],
                [1, 1, 1]]

        h_g = [
                [1, 4, 6, 4, 1],
                [4, 16, 24, 16, 4],
                [6, 24, 36, 24, 6],
                [4, 16, 24, 15, 4],
                [1, 4, 6, 4, 1]]

        h_a = [[1 / 9 * value for value in row] for row in h_a]
        h_g = [[1 / 256 * value for value in row] for row in h_g]

        pixels_red = [[pixel[0] for pixel in row] for row in pixels]
        pixels_green = [[pixel[1] for pixel in row] for row in pixels]
        pixels_blue = [[pixel[2] for pixel in row] for row in pixels]

        for kernel, name in zip([h_a, h_g], ['h_a', 'h_g']):

            pixels_red_convoluted = convolution(pixels_red, kernel)
            pixels_green_convoluted = convolution(pixels_green, kernel)
            pixels_blue_convoluted = convolution(pixels_blue, kernel)

            pixels_convoluted = [[(r, g, b) for r,g,b in zip(row1, row2, row3)] for row1, row2, row3 in zip(pixels_red_convoluted, pixels_green_convoluted, pixels_blue_convoluted)]

            img_convoluted = _matrix_to_image(pixels_convoluted, mode = "RGB")
            img_convoluted.save(filename + " convoluted " + name + ".bmp", "bmp")

        # Task 2-3c

        s_x = [
                [1, 0, -1],
                [2, 0, -2],
                [1, 0, -1]]

        s_y = [
                [1, 2, 1],
                [0, 0, 0],
                [-1, -2, -1]]

        gradient_x = convolution(pixels_gray, s_x)
        gradient_y = convolution(pixels_gray, s_y)
        magnitude = [[int(sqrt(x**2 + y**2)) for x, y in zip(row1, row2)] for row1, row2 in zip(gradient_x, gradient_y)]

        gradient_x_img = _matrix_to_image(gradient_x)
        gradient_y_img = _matrix_to_image(gradient_y)
        magnitude_img = _matrix_to_image(magnitude)

        gradient_x_img.save(filename + " gradient x.bmp", "bmp")
        gradient_y_img.save(filename + " gradient y.bmp", "bmp")
        magnitude_img.save(filename + " magnitude.bmp", "bmp")


    #Task 2-2b
    for filename in ["images/5.1.10-aerial.tiff", "images/5.2.09-aerial.tiff"]:
        img = Image.open(filename)
        pixels = _image_to_matrix(img)

        pixels = normalize(pixels)

        for gamma in [0.3, 0.6, 1.4, 2, 4]:

            pix = [[pixel for pixel in row] for row in pixels]

            pixels_gamma = gamma_transform(pix, gamma)

            pixels_gamma = to_spatial(pixels_gamma)

            img_gamma = _matrix_to_image(pixels_gamma)

            img_gamma.save(filename + " gamma " + str(gamma) + ".bmp", "bmp")
