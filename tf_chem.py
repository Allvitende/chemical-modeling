import tensorflow as tf

input_data =
# x will be the input matrix flattened (28x29)
x = tf.placeholder(tf.float32, [None, 812])

# Define the weights (initial value doesn't matter since these will be learned)
W = tf.Variable(tf.zeros([812, 812]))
b = tf.Variable(tf.zeros([812]))

# Predict output matrix
y = tf.nn.softmax(tf.matmul(x, W) + b)

# Actual output matrix from the training set
y_ = tf.placeholder(tf.float32, [None, 812])

# Calculate loss and optimize
cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=y_, logits=y))
train_step = tf.train.GradientDescentOptimizer(0.01).minimize(cross_entropy)

sess = tf.InteractiveSession()
tf.global_variables_initializer().run()

# Training
for _ in range(1000):
    batch_xs, batch_ys = input_data.train.next_batch(100)
    sess.run(train_step, feed_dict={x: batch_xs, y_: batch_ys})

# Test trained model
correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
print(sess.run(accuracy, feed_dict={x: input_data.test.distance_table,
                                    y_: input_data.test.connection_table}))
