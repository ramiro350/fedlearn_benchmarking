# Copyright (C) 2020-2024 Intel Corporation
# SPDX-License-Identifier: Apache-2.0

"""You may copy this file as the starting point of your own model."""

from openfl.federated import PyTorchDataLoader
from torchvision import datasets
from torchvision import transforms
import numpy as np
from logging import getLogger
import pdb
logger = getLogger(__name__)


class PyTorchCIFAR10InMemory(PyTorchDataLoader):
    """PyTorch data loader for CIFAR-10 dataset."""

    def __init__(self, data_path, batch_size, **kwargs):
        """Instantiate the data object.

        Args:
            data_path: The file path to the data
            batch_size: The batch size of the data loader
            **kwargs: Additional arguments, passed to super
             init and load_cifar10_shard
        """
        super().__init__(batch_size, **kwargs)

        # num_classes, X_train, y_train, X_valid, y_valid = load_cifar10_shard(
        #     shard_num=int(data_path), **kwargs
        # )
        # pdb.set_trace()
        _, num_classes, X_train, y_train, X_valid, y_valid = load_cifar10_shard(
            shard_num=int(data_path), collaborator_count=2, categorical=False, channels_last=False
        )

        self.X_train = X_train
        self.y_train = y_train
        self.train_loader = self.get_train_loader()

        self.X_valid = X_valid
        self.y_valid = y_valid
        self.val_loader = self.get_valid_loader()

        self.num_classes = num_classes


# def load_cifar10_shard(
#     shard_num, collaborator_count, categorical=False, channels_last=True, **kwargs
# ):
#     """
#     Load the CIFAR-10 dataset.

#     Args:
#         shard_num (int): The shard to use from the dataset
#         collaborator_count (int): The number of collaborators in the
#                                   federation
#         categorical (bool): True = convert the labels to one-hot encoded
#                             vectors (Default = True)
#         channels_last (bool): True = The input images have the channels
#                               last (Default = True)
#         **kwargs: Additional parameters to pass to the function

#     Returns:
#         list: The input shape
#         int: The number of classes
#         numpy.ndarray: The training data
#         numpy.ndarray: The training labels
#         numpy.ndarray: The validation data
#         numpy.ndarray: The validation labels
#     """
#     num_classes = 10
#     (X_train, y_train), (X_valid, y_valid) = _load_raw_datashards(
#         shard_num, collaborator_count, transform=transforms.Compose([
#             transforms.ToTensor(),
#             transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)),
#         ])
#     )
#     # pdb.set_trace()

#     logger.info(f"CIFAR-10 > X_train Shape : {X_train.shape}")
#     logger.info(f"CIFAR-10 > y_train Shape : {y_train.shape}")
#     logger.info(f"CIFAR-10 > Train Samples : {X_train.shape[0]}")
#     logger.info(f"CIFAR-10 > Valid Samples : {X_valid.shape[0]}")

#     if categorical:
#         # convert class vectors to binary class matrices
#         y_train = one_hot(y_train, num_classes)
#         y_valid = one_hot(y_valid, num_classes)

#     return num_classes, X_train, y_train, X_valid, y_valid


def one_hot(labels, classes):
    """
    One Hot encode a vector.

    Args:
        labels (list):  List of labels to onehot encode
        classes (int): Total number of categorical classes

    Returns:
        np.array: Matrix of one-hot encoded labels
    """
    return np.eye(classes)[labels]


def _load_raw_datashards(shard_num, collaborator_count, transform=None):
    """
    Load the raw data by shard.

    Returns tuples of the dataset shard divided into training and validation.

    Args:
        shard_num (int): The shard number to use
        collaborator_count (int): The number of collaborators in the federation
        transform: torchvision.transforms.Transform to apply to images

    Returns:
        2 tuples: (image, label) of the training, validation dataset
    """
    train_data, val_data = (
        datasets.CIFAR10("data", train=train, download=True, transform=transform)
        for train in (True, False)
    )
    X_train_tot, y_train_tot = train_data.data, np.array(train_data.targets)
    X_valid_tot, y_valid_tot = val_data.data, np.array(val_data.targets)

    # create the shards
    shard_num = int(shard_num)
    X_train = X_train_tot[shard_num::collaborator_count]
    y_train = y_train_tot[shard_num::collaborator_count]

    X_valid = X_valid_tot[shard_num::collaborator_count]
    y_valid = y_valid_tot[shard_num::collaborator_count]

    # pdb.set_trace()
    return (X_train, y_train), (X_valid, y_valid)

def load_cifar10_shard(shard_num, collaborator_count, categorical=True,
                       channels_last=True):
    """
    Load the CIFAR-10 dataset.

    Args:
        shard_num (int): The shard to use from the dataset
        collaborator_count (int): The number of collaborators in the federation
        categorical (bool): True = convert the labels to one-hot encoded
                            vectors (Default = True)
        channels_last (bool): True = The input images have the channels
                              last (Default = True)
        **kwargs: Additional parameters to pass to the function

    Returns:
        tuple: The input shape
        int: The number of classes
        numpy.ndarray: The training data
        numpy.ndarray: The training labels
        numpy.ndarray: The validation data
        numpy.ndarray: The validation labels
    """
    img_rows, img_cols = 32, 32
    num_classes = 10

    # Load raw dataset shards
    (X_train, y_train), (X_valid, y_valid) = _load_raw_datashards(
        shard_num, collaborator_count
    )

    if channels_last:
        X_train = X_train.reshape(X_train.shape[0], img_rows, img_cols, 3)
        X_valid = X_valid.reshape(X_valid.shape[0], img_rows, img_cols, 3)
        input_shape = (img_rows, img_cols, 3)
    else:
        X_train = X_train.reshape(X_train.shape[0], 3, img_rows, img_cols)
        X_valid = X_valid.reshape(X_valid.shape[0], 3, img_rows, img_cols)
        input_shape = (3, img_rows, img_cols)

    X_train = X_train.astype('float32') / 255.0
    X_valid = X_valid.astype('float32') / 255.0

    logger.info(f'CIFAR-10 > X_train Shape : {X_train.shape}')
    logger.info(f'CIFAR-10 > y_train Shape : {y_train.shape}')
    logger.info(f'CIFAR-10 > Train Samples : {X_train.shape[0]}')
    logger.info(f'CIFAR-10 > Valid Samples : {X_valid.shape[0]}')

    if categorical:
        # Convert class vectors to one-hot encoded matrices
        y_train = one_hot(y_train, num_classes)
        y_valid = one_hot(y_valid, num_classes)

    return input_shape, num_classes, X_train, y_train, X_valid, y_valid

