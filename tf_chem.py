import tensorflow as tf

# x will be the input matrix flattened (28x28)
x = tf.placeholder(tf.float32, [None, 784])

# Define the weights (initial value doesn't matter since these will be learned)
W = tf.Variable(tf.zeros([784, 784]))
b = tf.Variable(tf.zeros([784]))

# Predict output matrix
y = tf.nn.softmax(tf.matmul(x, W) + b)

# Actual output matrix from the training set
y_ = tf.placeholder(tf.float32, [None, 784])

# Calculate loss and optimize
cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=y_, logits=y))
train_step = tf.train.GradientDescentOptimizer(0.05).minimize(cross_entropy)
