import tensorflow as tf
import sdfparse as p

# x will be the input matrix flattened (28x29)
x = tf.placeholder(tf.float32, [None, 812])

# Define the weights (initial value doesn't matter since these will be learned)
# W = tf.Variable(tf.random_uniform([812, 812], minval=0, dtype=tf.float32))
W1 = tf.Variable(tf.truncated_normal([812, 784], stddev=0.1))
b1 = tf.Variable(tf.truncated_normal([784], stddev=0.1))
W2 = tf.Variable(tf.truncated_normal([784, 784], stddev=0.1))
b2 = tf.Variable(tf.truncated_normal([784], stddev=0.1))
W3 = tf.Variable(tf.truncated_normal([784, 784], stddev=0.1))
b3 = tf.Variable(tf.truncated_normal([784], stddev=0.1))
W = tf.Variable(tf.truncated_normal([784, 784], stddev=0.1))
b = tf.Variable(tf.truncated_normal([784], stddev=0.1))

# Predict output matrix
# y = tf.nn.softmax(tf.nn.l2_normalize(tf.matmul(x, W) + b, dim= 0, epsilon=1e-12))
# y = tf.nn.sigmoid(tf.matmul(x, W) + b)
# y = tf.nn.relu(tf.nn.sigmoid(tf.matmul(x, W) + b))
layer1 = tf.add(tf.matmul(x, W1), b1)
layer1 = tf.nn.relu(layer1)

layer2 = tf.add(tf.matmul(layer1, W2), b2)
layer2 = tf.nn.relu(layer2)

layer3 = tf.add(tf.matmul(layer2, W3), b3)
layer3 = tf.nn.relu(layer3)

y = tf.add(tf.matmul(layer3, W), b)
y = tf.nn.sigmoid(y)

# Actual output matrix from the training set
y_ = tf.placeholder(tf.float32, [None, 784])

# Calculate loss and optimize
cross_entropy = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(labels=y_, logits=y))
# cross_entropy = tf.reduce_sum(tf.abs(y - y_))
train_step = tf.train.AdamOptimizer(0.001).minimize(cross_entropy)

sess = tf.InteractiveSession()
tf.global_variables_initializer().run()

a, b = p.get_batch()
train_len = len(a)

correct_prediction = tf.equal(y_, y)
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

# Training
for i in range(train_len):
    batch_xs = a[i]
    batch_ys = b[i]
    _, loss, acc, pred = sess.run([train_step, cross_entropy, accuracy, correct_prediction], feed_dict={x: batch_xs, y_: batch_ys})
    print("Loss= " + "{:.6f}".format(loss) + " Accuracy= " + "{:.5f}".format(acc))
    #print(batch_ys)
    #print(y.eval({x: batch_xs}))

# Test trained model
cumulative_accuracy = 0.0
for i in range(train_len):
    acc_batch_xs = a[i]
    acc_batch_ys = b[i]
    cumulative_accuracy += accuracy.eval(feed_dict={x: acc_batch_xs, y_: acc_batch_ys})
    print_correct_pred = correct_prediction.eval(feed_dict={x: acc_batch_xs, y_: acc_batch_ys})
    print(print_correct_pred)
print("Test Accuracy= {}".format(cumulative_accuracy / train_len))
