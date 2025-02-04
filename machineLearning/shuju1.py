# import numpy as np
# import pandas
#
# x=np.array(["a",4,True,"b"])
# print(x.argmax())
# x.sort()
# print(x)
# b=pandas.Series([8,9,2,1],index=["one","two","three","four"])
# print (b)
# b.describe()
# print(b.describe())
# import matplotlib.pylab as pyl
# x=[1,2,3,4,8]
# y=[5,7,2,1,5]
# z=[1,1,1,1,1]
# pyl.plot(x,y,'om')
# pyl.show()
# data=numpy.random.random_integers(1,25,1000)
# data2=numpy.random.normal(5.0,2.0,10)
# print(data2)
# pyl.hist(data2)
# data=numpy.arange(1,10,2)
# print(data)
# pyl.show()


import tensorflow as tf
import numpy as np
# 使用 NumPy 生成假数据(phony data), 总共 100 个点.
x_data = np.float32(np.random.rand(2, 100)) # 随机输入
y_data = np.dot([0.100, 0.200], x_data) + 0.300

# # 构造一个线性模型
# #
b = tf.Variable(tf.zeros([1]))
W = tf.Variable(tf.random_uniform([1, 2], -1.0, 1.0))
y = tf.matmul(W, x_data) + b

# # 最小化方差
loss = tf.reduce_mean(tf.square(y - y_data))
print(loss.shape)
optimizer = tf.train.GradientDescentOptimizer(0.5)
train = optimizer.minimize(loss)

# 初始化变量
init = tf.initialize_all_variables()

# 启动图 (graph)
sess = tf.Session()
sess.run(init)
print(sess.run(loss))
# 拟合平面
for step in range(0, 201):
    sess.run(train)
    if step % 20 == 0:
        print (step, sess.run(W), sess.run(b))



# Copyright 2015 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""Functions for downloading and reading MNIST data."""
# from __future__ import absolute_import
# from __future__ import division
# from __future__ import print_function
# import gzip
# import os
# # import tensorflowtest.python.platform
# import numpy
# from six.moves import urllib
# from six.moves import xrange  # pylint: disable=redefined-builtin
# import tensorflow as tf
# SOURCE_URL = 'http://yann.lecun.com/exdb/mnist/'
# def maybe_download(filename, work_directory):
#   """Download the data from Yann's website, unless it's already here."""
#   if not os.path.exists(work_directory):
#     os.mkdir(work_directory)
#   filepath = os.path.join(work_directory, filename)
#   if not os.path.exists(filepath):
#     filepath, _ = urllib.request.urlretrieve(SOURCE_URL + filename, filepath)
#     statinfo = os.stat(filepath)
#     print('Successfully downloaded', filename, statinfo.st_size, 'bytes.')
#   return filepath
# def _read32(bytestream):
#   dt = numpy.dtype(numpy.uint32).newbyteorder('>')
#   return numpy.frombuffer(bytestream.read(4), dtype=dt)[0]
# def extract_images(filename):
#   """Extract the images into a 4D uint8 numpy array [index, y, x, depth]."""
#   print('Extracting', filename)
#   with gzip.open(filename) as bytestream:
#     magic = _read32(bytestream)
#     if magic != 2051:
#       raise ValueError(
#           'Invalid magic number %d in MNIST image file: %s' %
#           (magic, filename))
#     num_images = _read32(bytestream)
#     rows = _read32(bytestream)
#     cols = _read32(bytestream)
#     buf = bytestream.read(rows * cols * num_images)
#     data = numpy.frombuffer(buf, dtype=numpy.uint8)
#     data = data.reshape(num_images, rows, cols, 1)
#     return data
# def dense_to_one_hot(labels_dense, num_classes=10):
#   """Convert class labels from scalars to one-hot vectors."""
#   num_labels = labels_dense.shape[0]
#   index_offset = numpy.arange(num_labels) * num_classes
#   labels_one_hot = numpy.zeros((num_labels, num_classes))
#   labels_one_hot.flat[index_offset + labels_dense.ravel()] = 1
#   return labels_one_hot
# def extract_labels(filename, one_hot=False):
#   """Extract the labels into a 1D uint8 numpy array [index]."""
#   print('Extracting', filename)
#   with gzip.open(filename) as bytestream:
#     magic = _read32(bytestream)
#     if magic != 2049:
#       raise ValueError(
#           'Invalid magic number %d in MNIST label file: %s' %
#           (magic, filename))
#     num_items = _read32(bytestream)
#     buf = bytestream.read(num_items)
#     labels = numpy.frombuffer(buf, dtype=numpy.uint8)
#     if one_hot:
#       return dense_to_one_hot(labels)
#     return labels
# class DataSet(object):
#   def __init__(self, images, labels, fake_data=False, one_hot=False,
#                dtype=tf.float32):
#     """Construct a DataSet.
#     one_hot arg is used only if fake_data is true.  `dtype` can be either
#     `uint8` to leave the input as `[0, 255]`, or `float32` to rescale into
#     `[0, 1]`.
#     """
#     dtype = tf.as_dtype(dtype).base_dtype
#     if dtype not in (tf.uint8, tf.float32):
#       raise TypeError('Invalid image dtype %r, expected uint8 or float32' %
#                       dtype)
#     if fake_data:
#       self._num_examples = 10000
#       self.one_hot = one_hot
#     else:
#       assert images.shape[0] == labels.shape[0], (
#           'images.shape: %s labels.shape: %s' % (images.shape,
#                                                  labels.shape))
#       self._num_examples = images.shape[0]
#       # Convert shape from [num examples, rows, columns, depth]
#       # to [num examples, rows*columns] (assuming depth == 1)
#       assert images.shape[3] == 1
#       images = images.reshape(images.shape[0],
#                               images.shape[1] * images.shape[2])
#       if dtype == tf.float32:
#         # Convert from [0, 255] -> [0.0, 1.0].
#         images = images.astype(numpy.float32)
#         images = numpy.multiply(images, 1.0 / 255.0)
#     self._images = images
#     self._labels = labels
#     self._epochs_completed = 0
#     self._index_in_epoch = 0
#   @property
#   def images(self):
#     return self._images
#   @property
#   def labels(self):
#     return self._labels
#   @property
#   def num_examples(self):
#     return self._num_examples
#   @property
#   def epochs_completed(self):
#     return self._epochs_completed
#   def next_batch(self, batch_size, fake_data=False):
#     """Return the next `batch_size` examples from this data set."""
#     if fake_data:
#       fake_image = [1] * 784
#       if self.one_hot:
#         fake_label = [1] + [0] * 9
#       else:
#         fake_label = 0
#       return [fake_image for _ in xrange(batch_size)], [
#           fake_label for _ in xrange(batch_size)]
#     start = self._index_in_epoch
#     self._index_in_epoch += batch_size
#     if self._index_in_epoch > self._num_examples:
#       # Finished epoch
#       self._epochs_completed += 1
#       # Shuffle the data
#       perm = numpy.arange(self._num_examples)
#       numpy.random.shuffle(perm)
#       self._images = self._images[perm]
#       self._labels = self._labels[perm]
#       # Start next epoch
#       start = 0
#       self._index_in_epoch = batch_size
#       assert batch_size <= self._num_examples
#     end = self._index_in_epoch
#     return self._images[start:end], self._labels[start:end]
# def read_data_sets(train_dir, fake_data=False, one_hot=False, dtype=tf.float32):
#   class DataSets(object):
#     pass
#   data_sets = DataSets()
#   if fake_data:
#     def fake():
#       return DataSet([], [], fake_data=True, one_hot=one_hot, dtype=dtype)
#     data_sets.train = fake()
#     data_sets.validation = fake()
#     data_sets.test = fake()
#     return data_sets
#   TRAIN_IMAGES = 'train-images-idx3-ubyte.gz'
#   TRAIN_LABELS = 'train-labels-idx1-ubyte.gz'
#   TEST_IMAGES = 't10k-images-idx3-ubyte.gz'
#   TEST_LABELS = 't10k-labels-idx1-ubyte.gz'
#   VALIDATION_SIZE = 5000
#   local_file = maybe_download(TRAIN_IMAGES, train_dir)
#   train_images = extract_images(local_file)
#   local_file = maybe_download(TRAIN_LABELS, train_dir)
#   train_labels = extract_labels(local_file, one_hot=one_hot)
#   local_file = maybe_download(TEST_IMAGES, train_dir)
#   test_images = extract_images(local_file)
#   local_file = maybe_download(TEST_LABELS, train_dir)
#   test_labels = extract_labels(local_file, one_hot=one_hot)
#   validation_images = train_images[:VALIDATION_SIZE]
#   validation_labels = train_labels[:VALIDATION_SIZE]
#   train_images = train_images[VALIDATION_SIZE:]
#   train_labels = train_labels[VALIDATION_SIZE:]
#   data_sets.train = DataSet(train_images, train_labels, dtype=dtype)
#   data_sets.validation = DataSet(validation_images, validation_labels,
#                                  dtype=dtype)
#   data_sets.test = DataSet(test_images, test_labels, dtype=dtype)
#   return data_sets
# import tensorflow as tf

# a = tf.constant([
#     [[1.0, 2.0, 3.0, 4.0],
#      [5.0, 6.0, 7.0, 8.0],
#      [8.0, 7.0, 6.0, 5.0],
#      [4.0, 3.0, 2.0, 1.0]],
#     [[4.0, 3.0, 2.0, 1.0],
#      [8.0, 7.0, 6.0, 5.0],
#      [1.0, 2.0, 3.0, 4.0],
#      [5.0, 6.0, 7.0, 8.0]]
# ])
# print(a.shape)
# # reshape a,get the feature map [batch:1 height:2 width:2 channels:8]
# a = tf.reshape(a, [1, 2, 2, 8])
#
# normal_a = tf.nn.local_response_normalization(a, 2, 0, 1, 1)
# with tf.Session() as sess:
#     print("feature map:")
#     image = sess.run(a)
#     print(image)
#     print("normalized feature map:")
#     normal = sess.run(normal_a)
#     print(normal)