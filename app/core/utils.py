import os
from contextlib import contextmanager
from PIL import Image


@contextmanager
def ignored(*exceptions):
    try:
        yield
    except exceptions:
        pass


def delete_file(image):
    # if we have an old image; delete it
    with ignored(OSError):
        if image and image.path is not None:
            os.remove(image.path)


def image_resize(*, path: str, width: int, height, by_wdith=False):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    img = Image.open(path)
    w, h = img.size

    # return if the img's width and height is smaller than
    # the desired width and height
    if w <= width and h <= height:
        return

    # check to see if we should calculate ratio for width
    if by_wdith:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)

    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    if img.mode != 'RGB':
        img = img.convert('RGB')

    # resize the image
    img = img.resize(dim, Image.ANTIALIAS)
    img.save(path, format='JPEG', quality=100)


def get_first_matching_attr(obj, *attrs, default=None):
    for attr in attrs:
        if hasattr(obj, attr):
            return getattr(obj, attr)

    return default


def get_error_message(exc):
    if hasattr(exc, "message_dict"):
        return exc.message_dict
    error_msg = get_first_matching_attr(exc, "message", "messages")

    if isinstance(error_msg, list):
        error_msg = ", ".join(error_msg)

    if error_msg is None:
        error_msg = str(exc)

    return error_msg
