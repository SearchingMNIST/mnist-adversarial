import tensorflow as tf


def weight_variable(shape):
  return tf.get_variable(
      "weights", shape, initializer=tf.truncated_normal_initializer(stddev=0.1))


def bias_variable(shape):
  return tf.get_variable(
      "bias", shape, initializer=tf.constant_initializer(0.1))


def conv2d(x, W):
  return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')


def max_pool_2x2(x):
  return tf.nn.max_pool(
      x, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')


def deepnn(x, logits=False, training=True):
  with tf.variable_scope('conv1'):
    try:
      W_conv1 = weight_variable([5, 5, 1, 32])
      b_conv1 = bias_variable([32])
    except ValueError:  # deal with this bug https://github.com/tensorflow/tensorflow/issues/1325   
      W_conv1 = tf.get_default_graph().get_tensor_by_name(
          "model/conv1/weights:0")
      b_conv1 = tf.get_default_graph().get_tensor_by_name("model/conv1/bias:0")

    x_image = tf.reshape(x, [-1, 28, 28, 1])

    h_conv1 = tf.nn.relu(conv2d(x_image, W_conv1) + b_conv1)
    h_pool1 = max_pool_2x2(h_conv1)

  with tf.variable_scope('conv2'):
    try:
      W_conv2 = weight_variable([5, 5, 32, 64])
      b_conv2 = bias_variable([64])
    except ValueError:  # deal with this bug https://github.com/tensorflow/tensorflow/issues/1325   
      W_conv2 = tf.get_default_graph().get_tensor_by_name(
          "model/conv2/weights:0")
      b_conv2 = tf.get_default_graph().get_tensor_by_name("model/conv2/bias:0")

    h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2)
    h_pool2 = max_pool_2x2(h_conv2)

  with tf.variable_scope('fc1'):
    try:
      W_fc1 = weight_variable([7 * 7 * 64, 1024])
      b_fc1 = bias_variable([1024])
    except ValueError:  # deal with this bug https://github.com/tensorflow/tensorflow/issues/1325   
      W_fc1 = tf.get_default_graph().get_tensor_by_name("model/fc1/weights:0")
      b_fc1 = tf.get_default_graph().get_tensor_by_name("model/fc1/bias:0")

    h_pool2_flat = tf.reshape(h_pool2, [-1, 7 * 7 * 64])
    h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)

  with tf.variable_scope('dropout'):
    h_fc1_drop = tf.layers.dropout(
        h_fc1, rate=0.5, training=training, name='dropout')
  with tf.variable_scope('fc2'):
    try:
      W_fc2 = weight_variable([1024, 10])
      b_fc2 = bias_variable([10])
    except ValueError:  # deal with this bug https://github.com/tensorflow/tensorflow/issues/1325   
      W_fc2 = tf.get_default_graph().get_tensor_by_name("model/fc2/weights:0")
      b_fc2 = tf.get_default_graph().get_tensor_by_name("model/fc2/bias:0")

  logits_ = tf.add(tf.matmul(h_fc1_drop, W_fc2), b_fc2, name="y")
  y = tf.nn.softmax(logits_, name='ybar')

  if logits:
    return y, logits_

  return y
