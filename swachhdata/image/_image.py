import numpy as np

import os
from bs4 import BeautifulSoup
import requests
import urllib

import cv2

from tqdm.auto import tqdm
import random


class ImageNet:
    """Fetch Images and Labels from ImageNet:
    
    Parameters
    ----------
    img_shape: tuple (rows, cols, colors)
    total_img = int, default=None
    img_per_cat = int, default=None
    verbose: int (0, 1, -1), default=0

    Attributes
    ----------
    images_ : numpy.array of images
    labels_ : list of labels
    
    Examples
    --------
    >>> from swachhdata.image import ImageNet
    >>> indt = {'Automobile': 'n02814533'}
    >>> imgnet = ImageNet(img_shape=(32, 32, 3), total_img=100, verbose=1)
    >>> images, labels = imgnet.fetch(indt)
    """

    def __init__(self, img_shape, total_img=None, img_per_cat=None, verbose=0):
        self.__nos = total_img
        self.__nos_cat = img_per_cat
        self.__shape = img_shape
        self.__verbose = verbose
        self.__verbose_status = True
        if self.__verbose == -1:
            self.__verbose_status = False
        self.__urls = None
        self.images_ = None
        self.labels_ = []
    
    def __url_to_image(self, url):
        resp = urllib.request.urlopen(url)
        image = np.asarray(bytearray(resp.read()), dtype='uint8')
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
        return image
    
    def __get_imagelist(self, wnid):
        img_list = requests.get(f'http://www.image-net.org/api/text/imagenet.synset.geturls?wnid={wnid}')
        img_soup = BeautifulSoup(img_list.content, 'html.parser')
        img_str = str(img_soup)
        self.__urls = img_str.split('\r\n')

    def __count_nos_images(self, INdict):
        if self.__nos == None:
            try:
                self.__nos == self.__nos_cat * len(INdict)
            except:
                print(f'total_img and img_per_cat missing from arguments!, Please enter any one')
        else:
            self.__nos_cat = self.__nos // len(INdict)
        
        self.images_ = np.zeros((self.__nos, self.__shape[0], self.__shape[1], self.__shape[2]))
    
    def fetch(self, INdict):
        """Fetches Images from ImageNet
        Parameters
        ----------
        INdict : python dictionary

        Returns
        -------
        images : numpy.array of images
        labels : list of labels
        """
        id = 0
        self.__count_nos_images(INdict)
        for synset, wnid in INdict.items():
            self.__get_imagelist(wnid)
            snum = i = 0
            if self.__verbose in [-1, 1]:
                progress = tqdm(total=self.__nos_cat, position=0, leave=self.__verbose_status)
                progress.set_postfix({f'{synset}': wnid})
            while snum < self.__nos_cat:
                try:
                    img = self.__url_to_image(self.__urls[i])
                    img = cv2.resize(img, (self.__shape[0], self.__shape[1]))
                    self.images_[id] = img
                    self.labels_.append(synset)
                    id, snum = id + 1, snum + 1
                    if self.__verbose in [-1, 1]:
                        progress.update(1)
                except:
                    None
                i += 1
        return self.images_, self.labels_


class ImageReader:

    def __init__(self, image_size=(256, 256), color_mode='rgb', interpolation=cv2.INTER_AREA):
        
        self._image_size = image_size
        if color_mode == 'rgb':
            self._color_mode = cv2.COLOR_BGR2RGB
            self._color_shape = 3
        elif color_mode == 'grayscale':
            self._color_mode = 0
            self._color_shape = 1
        else:
            self._color_mode = cv2.COLOR_BGR2RGB
            self._color_shape = 3
        self._interpolation = interpolation

    def __labeled_directory(self, directory):
        ulabels = os.listdir(directory)
        nos = len([os.path.join(root, name) for root, dirs, files in os.walk(directory) for name in files])
        images = np.zeros((nos, self._image_size[0], self._image_size[1], self._color_shape))
        labels, id = [], 0
        for label in ulabels:
            image_paths = os.listdir(os.path.join(directory, label))
            for image in image_paths:
                try:
                    img = cv2.imread(image, self._color_mode)
                    labels.append(label)
                    img = cv2.resize(img, self._image_size, interpolation=self._interpolation)
                    images[id] = img.astype('float32')
                except Exception as e:
                    pass
        return images, labels
    
    def __unlabeled_directory(self, directory):
        ulabels = os.listdir(directory)
        nos = len([os.path.join(root, name) for root, dirs, files in os.walk(directory) for name in files])
        images = np.zeros((nos, self._image_size[0], self._image_size[1], self._color_shape))
        id = 0
        image_paths = os.listdir(directory)
        for image in image_paths:
            try:
                img = cv2.imread(image, self._color_mode)
                img = cv2.resize(img, self._image_size, interpolation=self._interpolation)
                images[id] = img.astype('float32')
            except Exception as e:
                pass
        return images

    def read(self, directory, name, labeled=False):
        if labeled:
            images, labels = self.__labeled_directory(directory)
            setattr(self, name, images)
            setattr(self, f'{name}_labels_', labels)
        
        if not labeled:
            images = self.__unlabeled_directory(directory)
            setattr(self, name, images)


def image_split(images, labels, split_size=0.5, random_state=None):
    """Split Images and Labels
    Returns in format (train, test, train_label, test_label)
    Where train > test
    
    Parameters
    ----------
    images: numpy.array
    labels: list
    split_size: float, default=0.5
    random_state: int, default=None

    Examples
    --------
    >>> from swachhdata.image import image_split
    >>> train, test, train_label, test_label = image_split(images, labels, split_size=0.3, random_state=123)
    """

    random.seed(random_state)
    unq = list(set(labels))
    unq_c = len(unq)
    ind1, ind2 = [], []

    for cat in unq:
        ind = [i for i, x in enumerate(labels) if x == cat]
        ind_c = len(ind)
        random.shuffle(ind)
        if split_size >= 0.5:
            ind1.append(ind[0:round(ind_c*split_size)])
            ind2.append(ind[round(ind_c*(split_size)):])
        else:
            ind2.append(ind[0:round(ind_c*split_size)])
            ind1.append(ind[round(ind_c*(split_size)):])
    
    ind1 = [item for sublist in ind1 for item in sublist]
    ind2 = [item for sublist in ind2 for item in sublist]

    label1 = np.take(labels, ind1)
    label2 = np.take(labels, ind2)

    image1 = np.zeros((len(label1), images.shape[1], images.shape[2], images.shape[3]))
    image2 = np.zeros((len(label2), images.shape[1], images.shape[2], images.shape[3]))

    i, j = 0, 0
    for ind in ind1:
        image1[i] = images[ind]
        i += 1
    for ind in ind2:
        image2[j] = images[ind]
        j += 1

    return image1, image2, label1, label2