#!/usr/bin/env python
# coding:utf-8


import numpy as np
from image_cropper import *  # noqa
# import sys


class DataLoader(object):

    def __init__(self):
        pass

    def load_with_subtraction_of_mean(self, path, mean_path, in_size):
        image_count = self.count_images(path)
        cropped_size = in_size
        xs = np.zeros((image_count, 3, cropped_size, cropped_size)).astype(np.float32)
        ys = np.zeros((image_count)).astype(np.int32)
        # print("> x shape: {s}".format(s=xs.shape))
        # print("> y shape: {s}".format(s=ys.shape))
        image_cropper = ImageCropper(in_size)
        mean_image = np.load(mean_path)  # (3, 256, 256)
        cropped_mean_image = image_cropper.crop_center_image(mean_image, is_scaled=False)  # (3, 227, 227)

        for i, (path, label) in enumerate(self.data_generator(path)):
            img = image_cropper.crop_center(path, is_scaled=False) - cropped_mean_image
            xs[i, :, :, :] = img
            ys[i] = label
        return xs, ys

    def load(self, path, in_size):
        image_count = self.count_images(path)
        cropped_size = in_size
        xs = np.zeros((image_count, 3, cropped_size, cropped_size)).astype(np.float32)
        ys = np.zeros((image_count)).astype(np.int32)
        # print("> x shape: {s}".format(s=xs.shape))
        # print("> y shape: {s}".format(s=ys.shape))
        image_cropper = ImageCropper(in_size)

        for i, (path, label) in enumerate(self.data_generator(path)):
            img = image_cropper.crop_center(path, is_scaled=True)
            xs[i, :, :, :] = img
            ys[i] = label
        return xs, ys

    def data_generator(self, path):
        head, tail = os.path.split(path)
        for line in open(path):
            tokens = line.strip().split()
            yield os.path.join(head, tokens[0]), tokens[1]

    def count_images(self, path):
        return sum([1 for _ in open(path)])


if __name__ == "__main__":
    import os

    MEAN_IMAGE_PATH = "/home/ubuntu/libs/caffe-master/python/caffe/imagenet/ilsvrc_2012_mean.npy"
    DATA_ROOT_DIR_PATH = "/home/ubuntu/data/devise/selected_images_256"
    TRAINING_DATA_PATH = os.path.join(DATA_ROOT_DIR_PATH, "train_valid.txt")
    TESTING_DATA_PATH = os.path.join(DATA_ROOT_DIR_PATH, "test.txt")

    data_loader = DataLoader()
    in_size = 227
#    for (p, l) in data_loader.data_generator(TRAINING_DATA_PATH):
#        print(p, l)
    xs, ys = data_loader.load_with_subtraction_of_mean(TRAINING_DATA_PATH, MEAN_IMAGE_PATH, in_size)
#    (xs, ys) = data_loader.load(TRAINING_DATA_PATH, in_size)
