import imutils
import cv2


def pyramid(image, scale=1.5, min_size=(30, 30)):
    '''Image pyramid - iterable function

    Params:
        image > Original image to resize
        scale > Resize scale (default 1.5)
        min_size > Minimum image scale (default (30,30))

    Yield:
        img > Resized image

    '''

    # First return the original image
    yield image

    # Iterate over the pyramid
    while True:
        # New image size
        new_size = int(image.shape[1] / scale)

        # Resize image
        resized_image = imutils.resize(image, width=new_size)
                                             
        # Stop the iteration if the image is smaller than the minimum size
        if resized_image.shape[0] < min_size[1] or resized_image.shape[1] < min_size[0]:
            break
                                                               
        # Return the image
        yield resized_image


def slidingWindow(image, step, window_size):
    ''' Sliding Window over image - iterable function

    Params:
        image > Image to be processed
        step > Sliding Window step
        windows_size> Sliding Window size
    '''

    # Iterate windows 
    for y in range(0, image.shape[0], step):
        for x in range(0, image.shape[1], step):
            # Return current window
            yield (x, y, image[y:y + window_size[1], x:x + window_size[0]])


if __name__ == "__main__":
    # Load a test image
    image = cv2.imread('test.jpg')
    (window_w, window_h) = (128, 128)

    count = 0
    # Loop over the pyramid
    for resized in pyramid(image):
        # Loop over the sliding windows
        for (x, y, window) in slidingWindow(resized, step=32, window_size=(window_w, window_h)):
            #TODO Use the image, for this test we save it in a file
            cv2.imwrite('images/{}.jpg'.format(count), window)
            count += 1
            

