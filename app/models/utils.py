import os


def delete_old_image(image):
    # if we have an old image; delete it
    if image and os.path.isfile(image.path):
        # Get full path to old image
        os.remove(image.path)
